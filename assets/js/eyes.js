/* ══════════════════════════════════════════════════════════════════════
   eyes.js — the hero's creatures, and the one that follows you down
   ----------------------------------------------------------------------
   Every creature is a still, split into layers by tools/eyes.py:
   body (iris removed, sclera rebuilt), iris, eye-opening mask, lid
   shade and corneal highlight. The page moves only the iris. That is
   the whole trick, and it is why this is not a video: a clip cannot know
   where the cursor is.

   What makes it read as a real eye rather than a sticker:
   · the iris is clipped by the opening, so it slides *under* the lids
   · the lid shadow is multiplied over the iris, so it sits in the socket
   · the catchlight does not move — reflections belong to the light
   · the iris foreshortens as it turns away from you
   · each creature follows at its own speed, and none of them is ever
     perfectly still: small involuntary jumps (micro-saccades) every
     half-second or so are what an eye that is alive actually does

   Layout lives in a 1920×1080 "stage" drawn with the same cover-fit as
   the preloader video, so the video's last frame and this page's first
   frame are the same picture at every window size.

   The central creature is drawn on its own canvas inside a sticky track
   that ends where section two stops pinning, so it holds its place on
   screen through the hero and section two, then leaves with section two.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  const host  = document.querySelector('.s1');
  const stage = document.getElementById('s1eyes');
  const dock  = document.getElementById('dockeye');
  const track = document.querySelector('.dock-track');
  if (!host || !stage) return;

  const BASE   = stage.dataset.base || '/assets/home/eyes/';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine   = matchMedia('(pointer: fine)').matches;

  let man = null, cr = [], ready = false;
  const sctx = stage.getContext('2d');
  const dctx = dock ? dock.getContext('2d') : null;

  /* ---- loading --------------------------------------------------------- */
  const img = (src) => new Promise((res, rej) => {
    const i = new Image(); i.decoding = 'async';
    i.onload = () => (i.decode ? i.decode().catch(() => {}) : Promise.resolve()).then(() => res(i));
    i.onerror = rej; i.src = BASE + src;
  });

  fetch(BASE + 'manifest.json?v=' + (stage.dataset.v || ''))
    .then((r) => r.json())
    .then(async (m) => {
      man = m;
      cr = await Promise.all(m.creatures.map(async (c) => {
        const [body, iris, mask, shade, hl] = await Promise.all(
          ['body', 'iris', 'mask', 'shade', 'hl'].map((k) => img(c.files[k])));
        const o = document.createElement('canvas');
        return Object.assign({}, c, {
          body, iris, mask, shade, hl, off: o, oc: o.getContext('2d'),
          gx: 0, gy: 0,          // current gaze offset, creature px
          jx: 0, jy: 0,          // micro-saccade offset
          jtx: 0, jty: 0, jNext: 0,
        });
      }));
      ready = true;
      layout(); draw(performance.now());
      // the still under the canvas is only a placeholder while layers load;
      // once the canvas has painted it must go, or the central creature —
      // which scrolls on its own sticky canvas — leaves its twin behind
      host.classList.add('eyes-live');
      window.dispatchEvent(new Event('nk:eyes-ready'));
      if (!reduce) requestAnimationFrame(loop);
    })
    .catch(() => {});

  /* ---- geometry -------------------------------------------------------- */
  let W = 0, H = 0, dpr = 1, S = 1, OX = 0, OY = 0;
  function cover() {
    const r = host.getBoundingClientRect();
    W = r.width; H = r.height;
    dpr = Math.min(devicePixelRatio || 1, 2);
    const sw = man ? man.stage.w : 1920, sh = man ? man.stage.h : 1080;
    S = Math.max(W / sw, H / sh);
    const pos = getComputedStyle(stage).getPropertyValue('--stage-pos').trim().split(/\s+/).map(parseFloat);
    const px = isNaN(pos[0]) ? 0.5 : pos[0] / 100, py = isNaN(pos[1]) ? 0.5 : pos[1] / 100;
    OX = (W - sw * S) * px; OY = (H - sh * S) * py;
  }

  // where a creature sits on screen (css px), relative to the hero's box
  function place(c) {
    const k = (c.h * S) / c.body.height;            // creature px → css px
    const w = c.body.width * k, h = c.body.height * k;
    return { k, w, h, x: OX + c.x * S - w / 2, y: OY + c.y * S - h / 2 };
  }

  function layout() {
    if (!ready) return;
    cover();
    stage.width = Math.round(W * dpr); stage.height = Math.round(H * dpr);
    stage.style.width = W + 'px'; stage.style.height = H + 'px';

    const c = cr.find((x) => x.central);
    if (c && dock && track) {
      const p = place(c);
      c._p = p;
      // a margin around the creature so its float and breath never clip
      const PAD = Math.ceil(12 * S + 8); c._pad = PAD;
      dock.width = Math.round((p.w + PAD * 2) * dpr); dock.height = Math.round((p.h + PAD * 2) * dpr);
      dock.style.width = (p.w + PAD * 2) + 'px'; dock.style.height = (p.h + PAD * 2) + 'px';
      // sticky from exactly where the stage puts it
      dock.style.marginLeft = (p.x - PAD) + 'px';
      dock.style.marginTop  = (p.y - PAD) + 'px';
      dock.style.top        = (p.y - PAD) + 'px';
      // release together with section two: the track ends where section
      // two's bottom meets the bottom of this creature on screen
      const s2 = document.querySelector('.s2');
      const mainTop = track.offsetParent ? track.offsetParent.getBoundingClientRect().top + scrollY : 0;
      const hostTop = host.getBoundingClientRect().top + scrollY;
      if (s2) {
        const s2Bottom = s2.getBoundingClientRect().bottom + scrollY;
        const vh = innerHeight;
        track.style.top = (hostTop - mainTop) + 'px';
        track.style.height = Math.max(p.y + p.h + PAD, s2Bottom - hostTop - (vh - (p.y + p.h + PAD))) + 'px';
      }
    }
  }

  /* ---- pointer --------------------------------------------------------- */
  let mx = null, my = null, lastMove = 0;
  addEventListener('pointermove', (e) => { mx = e.clientX; my = e.clientY; lastMove = performance.now(); }, { passive: true });
  document.addEventListener('pointerleave', () => { mx = my = null; });
  addEventListener('blur', () => { mx = my = null; });

  /* ---- one creature ---------------------------------------------------- */
  function drawCreature(ctx, c, x, y, k, t, dt) {
    const g = c.geom, ir = g.iris, e = g.eye;
    // float and breathe — slow, and out of phase with each other
    const bob = reduce ? 0 : Math.sin(t * 0.00055 + c.phase * 6.28) * 5 * S;
    const br  = reduce ? 1 : 1 + 0.006 * Math.sin(t * 0.0009 + c.phase * 9.1);
    const kk = k * br;
    const w = c.body.width * kk, h = c.body.height * kk;
    const ox = x + (c.body.width * k - w) / 2, oy = y + (c.body.height * k - h) / 2 + bob;

    // gaze target, in creature px
    let tx = 0, ty = 0;
    const ecx = ox + ir.cx * kk, ecy = oy + ir.cy * kk;       // eye centre, css px (canvas-local)
    const rect = ctx.canvas.getBoundingClientRect();
    if (mx !== null) {
      const vx = mx - (rect.left + ecx), vy = my - (rect.top + ecy);
      const dist = Math.hypot(vx, vy) || 1;
      const reach = dist / (dist + 240);                     // near the eye: less swing
      tx = (vx / dist) * reach * g.travel.x;
      ty = (vy / dist) * reach * g.travel.y;
    } else if (!reduce) {
      // nobody there: drift, the way an unattended eye does
      tx = Math.sin(t * 0.00031 + c.phase * 4) * g.travel.x * 0.35;
      ty = Math.sin(t * 0.00023 + c.phase * 7) * g.travel.y * 0.25;
    }
    const f = 1 - Math.exp(-dt * c.speed * 0.012);
    c.gx += (tx - c.gx) * f; c.gy += (ty - c.gy) * f;

    // micro-saccades: small, sudden, then held
    if (!reduce) {
      if (t > c.jNext) {
        c.jtx = (Math.random() - 0.5) * ir.r * 0.07;
        c.jty = (Math.random() - 0.5) * ir.r * 0.05;
        c.jNext = t + 350 + Math.random() * 1100;
      }
      const jf = 1 - Math.exp(-dt / 28);
      c.jx += (c.jtx - c.jx) * jf; c.jy += (c.jty - c.jy) * jf;
    }
    const gx = c.gx + c.jx, gy = c.gy + c.jy;

    // 1 · body
    ctx.drawImage(c.body, ox * dpr, oy * dpr, w * dpr, h * dpr);

    // 2 · iris in its own buffer: shade it, trim it to itself, clip to the opening
    const ew = Math.ceil(e.w * kk * dpr), eh = Math.ceil(e.h * kk * dpr);
    if (c.off.width !== ew || c.off.height !== eh) { c.off.width = ew; c.off.height = eh; }
    const o = c.oc;
    o.globalCompositeOperation = 'source-over';
    o.clearRect(0, 0, ew, eh);
    // foreshortening: an iris turned away from you is an ellipse
    const fx = 1 - 0.14 * Math.min(1, Math.abs(gx) / (g.travel.x || 1));
    const fy = 1 - 0.14 * Math.min(1, Math.abs(gy) / (g.travel.y || 1));
    const isz = ir.size * kk * dpr;
    const icx = (ir.cx - e.x + gx) * kk * dpr, icy = (ir.cy - e.y + gy) * kk * dpr;
    o.drawImage(c.iris, icx - isz * fx / 2, icy - isz * fy / 2, isz * fx, isz * fy);
    o.globalCompositeOperation = 'multiply';
    o.drawImage(c.shade, 0, 0, ew, eh);
    o.globalCompositeOperation = 'destination-in';
    o.drawImage(c.iris, icx - isz * fx / 2, icy - isz * fy / 2, isz * fx, isz * fy);
    // limbal shadow behind the iris, travelling with it (same numbers as
    // tools/build_eyes.py, so the first frame matches the preloader's last)
    const R = ir.r * kk * dpr;
    const hg = o.createRadialGradient(icx, icy, R * 0.95, icx, icy, R * 1.2);
    hg.addColorStop(0, 'rgba(70,35,30,0.28)'); hg.addColorStop(1, 'rgba(70,35,30,0)');
    o.globalCompositeOperation = 'destination-over';
    o.fillStyle = hg; o.fillRect(0, 0, ew, eh);
    o.globalCompositeOperation = 'destination-in';
    o.drawImage(c.mask, 0, 0, ew, eh);
    ctx.drawImage(c.off, (ox + e.x * kk) * dpr, (oy + e.y * kk) * dpr);

    // 3 · the catchlight stays where the light is
    ctx.drawImage(c.hl, (ox + e.x * kk) * dpr, (oy + e.y * kk) * dpr, ew, eh);
  }

  /* ---- frame ----------------------------------------------------------- */
  let last = performance.now();
  function draw(t) {
    // clamp both ways: a timestamp from the past (tab switch, test stepping)
    // must never make the easing run backwards and blow up
    const dt = Math.max(0, Math.min(64, t - last)); last = t;
    sctx.clearRect(0, 0, stage.width, stage.height);
    for (const c of cr) {
      if (c.central && dock) continue;
      const p = place(c);
      if (p.x > W || p.x + p.w < 0) continue;              // off the crop: skip
      drawCreature(sctx, c, p.x, p.y, p.k, t, dt);
    }
    const c = cr.find((x) => x.central);
    if (c && dock && c._p) {
      dctx.clearRect(0, 0, dock.width, dock.height);
      drawCreature(dctx, c, c._pad, c._pad, c._p.k, t, dt);
    }
  }
  function loop(t) { if (!document.hidden) draw(t); requestAnimationFrame(loop); }

  // test hook, only with ?eyesdebug in the URL: lets a hidden tab step
  // frames by hand, since a hidden tab gets no animation frames
  if (/[?&]eyesdebug/.test(location.search)) window.__eyes = { draw, get creatures() { return cr; } };

  // the hero copy steps aside as the creature scrolls over it, rather
  // than the two fighting for the same spot
  const copy = host.querySelector('.s1-in'), foot = host.querySelector('.s1-foot');
  function fadeCopy() {
    const k = Math.min(1, Math.max(0, scrollY / (innerHeight * 0.32)));
    const o = String(1 - k);
    for (const el of [copy, foot]) if (el) {
      el.style.opacity = o;
      el.style.pointerEvents = k > 0.9 ? 'none' : '';
    }
  }
  addEventListener('scroll', fadeCopy, { passive: true }); fadeCopy();

  addEventListener('resize', () => { layout(); if (reduce) draw(performance.now()); }, { passive: true });
  addEventListener('load', layout);
})();
