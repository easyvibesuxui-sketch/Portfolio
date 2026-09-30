/* ══════════════════════════════════════════════════════════════════════
   peek.js — the small creatures that live around the site
   ----------------------------------------------------------------------
   "Everyone's watching." Any element  <span class="eye" data-eye="d">
   becomes one of the hero's creatures at small size, and it looks at you.

   Same layer trick as the hero (eyes.js): the body is a still with the
   iris removed; only the iris moves, clipped by the lids, shaded by them,
   with a limbal shadow that travels with it and a catchlight that stays
   with the light.

   · layers load only for creatures that come near the viewport
   · only eyes on screen are drawn; nothing is drawn in a hidden tab
   · no pointer for a while (or a touch screen): they look around on
     their own, in short jumps, the way an eye searches
   · data-reach="px"   how far the cursor must be for a full turn (default 220)
   · data-speed="n"    how quickly it follows (default 1)
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  const els = [...document.querySelectorAll('.eye[data-eye]')];
  if (!els.length) return;

  const BASE = '/assets/eyes/';
  const V = (document.querySelector('script[src*="peek.js"]') || {}).src?.split('v=')[1] || '';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const dpr = () => Math.min(devicePixelRatio || 1, 2);

  /* ---- assets -------------------------------------------------------- */
  let man = null;
  const manP = fetch(BASE + 'manifest.json?v=' + V).then((r) => r.json()).then((m) => (man = m));
  const img = (src) => new Promise((res, rej) => {
    const i = new Image(); i.decoding = 'async';
    i.onload = () => res(i); i.onerror = rej; i.src = BASE + src + '?v=' + V;
  });
  const sets = {};
  function layers(id) {
    if (!sets[id]) sets[id] = manP.then(() => {
      const f = man[id].files;
      return Promise.all(['body', 'iris', 'mask', 'shade', 'hl'].map((k) => img(f[k])))
        .then(([body, iris, mask, shade, hl]) => ({ body, iris, mask, shade, hl, geom: man[id].geom }));
    });
    return sets[id];
  }

  /* ---- eyes ---------------------------------------------------------- */
  const eyes = els.map((el, n) => {
    const cv = document.createElement('canvas');
    cv.setAttribute('aria-hidden', 'true');
    el.appendChild(cv);
    const off = document.createElement('canvas');
    return {
      el, cv, ctx: cv.getContext('2d'), off, oc: off.getContext('2d'),
      id: el.dataset.eye, L: null, on: false,
      reach: +el.dataset.reach || 220, speed: +el.dataset.speed || 1,
      phase: (n * 0.618) % 1,
      gx: 0, gy: 0, jx: 0, jy: 0, jtx: 0, jty: 0, jNext: 0,
      lx: 0, ly: 0, lNext: 0,           // look-around target when nobody is there
    };
  });

  const io = new IntersectionObserver((ents) => {
    for (const en of ents) {
      const e = eyes.find((x) => x.el === en.target);
      e.on = en.isIntersecting;
      if (e.on && !e.L) layers(e.id).then((L) => { e.L = L; size(e); e.el.classList.add('is-live'); }).catch(() => {});
    }
  }, { rootMargin: '240px 0px' });
  eyes.forEach((e) => io.observe(e.el));

  function size(e) {
    const r = e.el.getBoundingClientRect(), d = dpr();
    const w = Math.max(1, Math.round(r.width * d)), h = Math.max(1, Math.round(r.height * d));
    if (e.cv.width !== w || e.cv.height !== h) { e.cv.width = w; e.cv.height = h; }
  }
  if ('ResizeObserver' in window) {
    const ro = new ResizeObserver((ents) => ents.forEach((en) => {
      const e = eyes.find((x) => x.el === en.target); if (e && e.L) size(e);
    }));
    eyes.forEach((e) => ro.observe(e.el));
  }

  /* ---- pointer ------------------------------------------------------- */
  let mx = null, my = null, lastMove = -1e9;
  const seen = (x, y) => { mx = x; my = y; lastMove = performance.now(); };
  addEventListener('pointermove', (ev) => seen(ev.clientX, ev.clientY), { passive: true });
  addEventListener('pointerdown', (ev) => seen(ev.clientX, ev.clientY), { passive: true });
  document.addEventListener('pointerleave', () => { lastMove = -1e9; });
  addEventListener('blur', () => { lastMove = -1e9; });

  /* ---- one creature -------------------------------------------------- */
  function draw(e, t, dt) {
    const { L, ctx, cv } = e, g = L.geom, ir = g.iris, ey = g.eye;
    const d = dpr();
    // contain-fit, bottom-centred (so a creature peeking over an edge
    // keeps its eye where the CSS put it)
    const W = cv.width, H = cv.height;
    const k = Math.min(W / L.body.width, H / L.body.height);
    const w = L.body.width * k, h = L.body.height * k;
    const ox = (W - w) / 2, oy = H - h;

    // where it looks
    const rect = cv.getBoundingClientRect();
    const ecx = rect.left + (ox + ir.cx * k) / d, ecy = rect.top + (oy + ir.cy * k) / d;
    let tx, ty;
    const idle = t - lastMove > 3500 || mx === null;
    if (!idle) {
      const vx = mx - ecx, vy = my - ecy, dist = Math.hypot(vx, vy) || 1;
      const reach = dist / (dist + e.reach);
      tx = (vx / dist) * reach * g.travel.x; ty = (vy / dist) * reach * g.travel.y;
    } else if (!reduce) {
      // searching: hold a direction, then jump to another
      if (t > e.lNext) {
        const a = Math.random() * Math.PI * 2, m = 0.35 + Math.random() * 0.6;
        e.lx = Math.cos(a) * m * g.travel.x; e.ly = Math.sin(a) * m * g.travel.y;
        e.lNext = t + 900 + Math.random() * 2200;
      }
      tx = e.lx; ty = e.ly;
    } else { tx = 0; ty = 0; }
    const f = 1 - Math.exp(-dt * e.speed * (idle ? 0.02 : 0.012));
    e.gx += (tx - e.gx) * f; e.gy += (ty - e.gy) * f;
    if (!reduce) {
      if (t > e.jNext) {
        e.jtx = (Math.random() - 0.5) * ir.r * 0.07; e.jty = (Math.random() - 0.5) * ir.r * 0.05;
        e.jNext = t + 350 + Math.random() * 1100;
      }
      const jf = 1 - Math.exp(-dt / 28);
      e.jx += (e.jtx - e.jx) * jf; e.jy += (e.jty - e.jy) * jf;
    }
    const gx = e.gx + e.jx, gy = e.gy + e.jy;

    ctx.clearRect(0, 0, W, H);
    ctx.drawImage(L.body, ox, oy, w, h);

    const ew = Math.max(1, Math.ceil(ey.w * k)), eh = Math.max(1, Math.ceil(ey.h * k));
    if (e.off.width !== ew || e.off.height !== eh) { e.off.width = ew; e.off.height = eh; }
    const o = e.oc;
    o.globalCompositeOperation = 'source-over';
    o.clearRect(0, 0, ew, eh);
    const fx = 1 - 0.14 * Math.min(1, Math.abs(gx) / (g.travel.x || 1));
    const fy = 1 - 0.14 * Math.min(1, Math.abs(gy) / (g.travel.y || 1));
    const isz = ir.size * k;
    const icx = (ir.cx - ey.x + gx) * k, icy = (ir.cy - ey.y + gy) * k;
    o.drawImage(L.iris, icx - isz * fx / 2, icy - isz * fy / 2, isz * fx, isz * fy);
    o.globalCompositeOperation = 'multiply';
    o.drawImage(L.shade, 0, 0, ew, eh);
    o.globalCompositeOperation = 'destination-in';
    o.drawImage(L.iris, icx - isz * fx / 2, icy - isz * fy / 2, isz * fx, isz * fy);
    const R = ir.r * k;
    const hg = o.createRadialGradient(icx, icy, R * 0.95, icx, icy, R * 1.2);
    hg.addColorStop(0, 'rgba(70,35,30,0.28)'); hg.addColorStop(1, 'rgba(70,35,30,0)');
    o.globalCompositeOperation = 'destination-over';
    o.fillStyle = hg; o.fillRect(0, 0, ew, eh);
    o.globalCompositeOperation = 'destination-in';
    o.drawImage(L.mask, 0, 0, ew, eh);
    ctx.drawImage(e.off, ox + ey.x * k, oy + ey.y * k);
    ctx.drawImage(L.hl, ox + ey.x * k, oy + ey.y * k, ew, eh);
  }

  /* ---- loop ---------------------------------------------------------- */
  let last = performance.now();
  function frame(t) {
    const dt = Math.max(0, Math.min(64, t - last)); last = t;
    if (!document.hidden) for (const e of eyes) if (e.on && e.L) draw(e, t, dt);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  // test hook, only with ?eyesdebug in the URL
  if (/[?&]eyesdebug/.test(location.search)) window.__peek = { eyes, draw: (t) => { for (const e of eyes) if (e.L) draw(e, t, 16); } };
})();
