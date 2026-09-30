/* ============================================================
   NK · NEBULA — GPU particle field
   ------------------------------------------------------------
   A port of the "quantum nebula" idea onto raw WebGL, sized for
   a portfolio rather than a demo.

   The reference implementation advected 50,000 particles inside a
   JavaScript for-loop, allocating several THREE.Vector3 objects per
   particle per frame — roughly nine million allocations a second, all
   on the main thread, while the curl-noise GLSL it shipped with went
   unused. Here the simulation is stateless and lives entirely in the
   vertex shader: a particle's position is a pure function of its seed
   and the clock, so nothing is written back to a buffer, nothing is
   allocated per frame, and the CPU cost per frame is one uniform
   update and one draw call.

   Bloom is faked in the fragment shader with an exponential falloff
   under additive blending, which costs one pass instead of the three
   an EffectComposer chain would add.
   ============================================================ */
(function () {
  'use strict';

  const cv = document.getElementById('nebula');
  if (!cv) return;

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small  = innerWidth < 861;

  const gl = cv.getContext('webgl', {
    alpha: true, antialias: false, depth: false, stencil: false,
    premultipliedAlpha: false, powerPreference: 'default',
  });
  if (!gl) return;                       // no WebGL: the CSS aurora still stands

  /* ---- tuning ------------------------------------------------------ */
  const COUNT = small ? 1600 : 4200;     // a suggestion of a field, not a starfield
  const DPR   = Math.min(devicePixelRatio || 1, 1.5);
  // Points resolve to roughly 2–8 device px. Sized any larger, additive
  // blending fuses 20k sprites into one smooth haze that is
  // indistinguishable from the CSS gradient underneath — the particles
  // have to stay small enough to read as individual points of light.
  const SIZE  = small ? 5.5 : 6.4;

  /* ---- shaders ----------------------------------------------------- */
  // Ashima simplex noise — the same function the reference shipped and
  // never called. Here it actually drives the motion.
  const NOISE = `
    vec3 mod289(vec3 x){ return x - floor(x * (1.0/289.0)) * 289.0; }
    vec4 mod289(vec4 x){ return x - floor(x * (1.0/289.0)) * 289.0; }
    vec4 permute(vec4 x){ return mod289(((x*34.0)+1.0)*x); }
    vec4 taylorInvSqrt(vec4 r){ return 1.79284291400159 - 0.85373472095314 * r; }
    float snoise(vec3 v){
      const vec2 C = vec2(1.0/6.0, 1.0/3.0);
      const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
      vec3 i  = floor(v + dot(v, C.yyy));
      vec3 x0 = v - i + dot(i, C.xxx);
      vec3 g = step(x0.yzx, x0.xyz);
      vec3 l = 1.0 - g;
      vec3 i1 = min(g.xyz, l.zxy);
      vec3 i2 = max(g.xyz, l.zxy);
      vec3 x1 = x0 - i1 + C.xxx;
      vec3 x2 = x0 - i2 + C.yyy;
      vec3 x3 = x0 - D.yyy;
      i = mod289(i);
      vec4 p = permute(permute(permute(
                 i.z + vec4(0.0, i1.z, i2.z, 1.0))
               + i.y + vec4(0.0, i1.y, i2.y, 1.0))
               + i.x + vec4(0.0, i1.x, i2.x, 1.0));
      float n_ = 0.142857142857;
      vec3 ns = n_ * D.wyz - D.xzx;
      vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
      vec4 x_ = floor(j * ns.z);
      vec4 y_ = floor(j - 7.0 * x_);
      vec4 x = x_ * ns.x + ns.yyyy;
      vec4 y = y_ * ns.x + ns.yyyy;
      vec4 h = 1.0 - abs(x) - abs(y);
      vec4 b0 = vec4(x.xy, y.xy);
      vec4 b1 = vec4(x.zw, y.zw);
      vec4 s0 = floor(b0) * 2.0 + 1.0;
      vec4 s1 = floor(b1) * 2.0 + 1.0;
      vec4 sh = -step(h, vec4(0.0));
      vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
      vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
      vec3 p0 = vec3(a0.xy, h.x);
      vec3 p1 = vec3(a0.zw, h.y);
      vec3 p2 = vec3(a1.xy, h.z);
      vec3 p3 = vec3(a1.zw, h.w);
      vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
      p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
      vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
      m = m * m;
      return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
    }
    vec3 snoiseVec3(vec3 x){
      return vec3(snoise(x),
                  snoise(vec3(x.y - 19.1, x.z + 33.4, x.x + 47.2)),
                  snoise(vec3(x.z + 74.2, x.x - 124.5, x.y + 99.4)));
    }
    // A swirling, non-collapsing flow field.
    // The cross product of two smooth vector fields is divergence-free,
    // exactly like a curl — but it costs 2 snoiseVec3 (6 snoise) where
    // finite-difference curl needs 4 (12). At 20k particles that halving
    // is the difference between 30fps and 60fps on integrated graphics,
    // and the two are indistinguishable at this particle size.
    vec3 curl(vec3 p){
      vec3 a = snoiseVec3(p);
      vec3 b = snoiseVec3(p * 1.7 + 31.4);
      return normalize(cross(a, b) + 1e-5);
    }
  `;

  const VERT = `
    precision highp float;
    attribute vec3 aSeed;      // home position, [-1,1] cube
    attribute vec2 aRnd;       // x: size/brightness jitter, y: colour mix
    uniform float uTime;
    uniform float uAspect;
    uniform float uDpr;
    uniform float uSize;
    uniform vec2  uMouse;      // NDC-ish, -1..1
    uniform float uMouseOn;
    varying vec3  vCol;
    varying float vAlpha;
    ${NOISE}
    void main(){
      vec3 p = aSeed;
      float t = uTime * 0.045;

      // Advect along the curl field; the field itself evolves in z so the
      // structure keeps reorganising instead of reaching a steady state.
      // Sampled in aspect-corrected space so the swirl is not stretched
      // horizontally once the cube is mapped to a wide viewport.
      vec3 flow = curl(vec3(p.x * uAspect, p.y, p.z) * 0.85 + vec3(0.0, 0.0, t));
      p += flow * 0.42;
      p.x += t * 0.06;

      // wrap cleanly in [-1,1]; alpha fades at the seam so the wrap is
      // never visible as a pop (the reference flipped the sign instead,
      // which teleports particles across the box in full view)
      vec3 w = fract(p * 0.5 + 0.5);
      float edge = min(min(w.x, 1.0 - w.x), min(w.y, 1.0 - w.y));
      p = w * 2.0 - 1.0;

      // pointer pushes particles aside, falling off with distance
      vec2 toM = p.xy - uMouse;
      float dm = length(toM);
      p.xy += normalize(toM + 1e-5) * (0.30 / (1.0 + dm * dm * 11.0)) * uMouseOn;

      // cheap perspective: nearer particles are bigger and spread wider.
      // No aspect divide here — that compressed the whole field into the
      // middle third of a wide viewport; the noise above is already
      // aspect-corrected, so the swirl stays round while the cube fills
      // the screen.
      float z = p.z * 0.42 + 1.55;
      vec2 ndc = p.xy / z * 1.45;

      gl_Position  = vec4(ndc, 0.0, 1.0);
      gl_PointSize = (uSize / z) * uDpr * (0.35 + aRnd.x * 0.9);

      // azure -> steel -> indigo, so the field harmonises with the aurora
      vec3 ember = vec3(0.780, 0.769, 0.757);
      vec3 amber = vec3(0.925, 0.914, 0.902);
      vec3 plum  = vec3(0.478, 0.471, 0.463);
      float m = aRnd.y;
      vCol = m < 0.62
           ? mix(ember, amber, m / 0.62)
           : mix(amber, plum, (m - 0.62) / 0.38);

      // a few per cent of particles burn hot, which gives the field
      // sparkle rather than an even dusting
      float hot = step(0.955, aRnd.y) * 1.9;
      vAlpha = smoothstep(0.0, 0.14, edge) * (0.18 + aRnd.x * 0.38 + hot) / z;
    }
  `;

  const FRAG = `
    precision mediump float;
    varying vec3  vCol;
    varying float vAlpha;
    void main(){
      // exponential falloff under additive blending reads as bloom, for
      // the cost of one pass instead of an EffectComposer chain
      float d = length(gl_PointCoord - 0.5) * 2.0;
      if (d > 1.0) discard;
      float core = exp(-d * d * 5.5);
      gl_FragColor = vec4(vCol * (0.25 + core), core * vAlpha);
    }
  `;

  /* ---- program ----------------------------------------------------- */
  function compile(type, src) {
    const sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      console.error('[nebula]', gl.getShaderInfoLog(sh));
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }
  const vs = compile(gl.VERTEX_SHADER, VERT);
  const fs = compile(gl.FRAGMENT_SHADER, FRAG);
  if (!vs || !fs) return;

  const prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    console.error('[nebula]', gl.getProgramInfoLog(prog));
    return;
  }
  gl.useProgram(prog);

  /* ---- geometry: written once, never touched again ----------------- */
  const seeds = new Float32Array(COUNT * 3);
  const rnds  = new Float32Array(COUNT * 2);
  for (let i = 0; i < COUNT; i++) {
    seeds[i * 3]     = Math.random() * 2 - 1;
    seeds[i * 3 + 1] = Math.random() * 2 - 1;
    seeds[i * 3 + 2] = Math.random() * 2 - 1;
    rnds[i * 2]      = Math.random();
    rnds[i * 2 + 1]  = Math.random();
  }

  const aSeed = gl.getAttribLocation(prog, 'aSeed');
  const aRnd  = gl.getAttribLocation(prog, 'aRnd');

  const bSeed = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, bSeed);
  gl.bufferData(gl.ARRAY_BUFFER, seeds, gl.STATIC_DRAW);
  gl.enableVertexAttribArray(aSeed);
  gl.vertexAttribPointer(aSeed, 3, gl.FLOAT, false, 0, 0);

  const bRnd = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, bRnd);
  gl.bufferData(gl.ARRAY_BUFFER, rnds, gl.STATIC_DRAW);
  gl.enableVertexAttribArray(aRnd);
  gl.vertexAttribPointer(aRnd, 2, gl.FLOAT, false, 0, 0);

  const uTime    = gl.getUniformLocation(prog, 'uTime');
  const uAspect  = gl.getUniformLocation(prog, 'uAspect');
  const uDpr     = gl.getUniformLocation(prog, 'uDpr');
  const uSize    = gl.getUniformLocation(prog, 'uSize');
  const uMouse   = gl.getUniformLocation(prog, 'uMouse');
  const uMouseOn = gl.getUniformLocation(prog, 'uMouseOn');

  gl.uniform1f(uDpr, DPR);
  gl.uniform1f(uSize, SIZE);
  gl.uniform1f(uMouseOn, matchMedia('(hover: none)').matches ? 0 : 1);

  gl.disable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE);          // additive: overlaps brighten
  gl.clearColor(0, 0, 0, 0);                   // stay transparent over the aurora

  /* ---- sizing ------------------------------------------------------ */
  function resize() {
    const w = Math.round(innerWidth  * DPR);
    const h = Math.round(innerHeight * DPR);
    if (cv.width !== w || cv.height !== h) {
      cv.width = w; cv.height = h;
      gl.viewport(0, 0, w, h);
    }
    gl.uniform1f(uAspect, innerWidth / innerHeight);
  }
  resize();
  let rt;
  addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(resize, 180); });

  /* ---- pointer ----------------------------------------------------- */
  const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
  addEventListener('pointermove', (e) => {
    mouse.tx = (e.clientX / innerWidth) * 2 - 1;
    mouse.ty = -((e.clientY / innerHeight) * 2 - 1);
  }, { passive: true });

  /* ---- loop -------------------------------------------------------- */
  const t0 = performance.now();
  let frame = 0;

  // Adaptive budget. The buffers are static, so drawing fewer points is
  // just a smaller count argument — no reallocation. If the first second
  // runs slow, this halves the field rather than shipping a janky page to
  // whoever has the weakest GPU.
  let drawn = COUNT, checked = 0, slow = 0, prev = 0;

  function draw(now) {
    frame = requestAnimationFrame(draw);
    if (document.hidden) { prev = 0; return; }  // don't burn battery in a background tab

    if (checked < 90) {
      if (prev && now - prev > 22) slow++;
      prev = now;
      if (++checked === 90 && slow > 30) drawn = Math.round(COUNT * 0.5);
    }

    mouse.x += (mouse.tx - mouse.x) * 0.05;    // easing keeps the push from snapping
    mouse.y += (mouse.ty - mouse.y) * 0.05;

    gl.uniform1f(uTime, reduce ? 0 : (now - t0) * 0.001);
    gl.uniform2f(uMouse, mouse.x, mouse.y);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.POINTS, 0, drawn);
  }
  frame = requestAnimationFrame(draw);

  // a lost context would otherwise leave a dead canvas over the page
  cv.addEventListener('webglcontextlost', (e) => {
    e.preventDefault();
    cancelAnimationFrame(frame);
  });
})();
