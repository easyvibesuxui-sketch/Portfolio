/* ============================================================
   NK · VARIANT B — GLASS
   Motion system: Lenis + GSAP/ScrollTrigger, canvas gradient
   field, refracting tile grid, scroll-dwell pacing.
   ============================================================ */
(() => {
  'use strict';

  const { gsap } = window;
  gsap.registerPlugin(window.ScrollTrigger);
  const ST = window.ScrollTrigger;

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = matchMedia('(hover: none)').matches || innerWidth < 901;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  const setVH = () => document.documentElement.style.setProperty('--vh', innerHeight * 0.01 + 'px');
  setVH(); addEventListener('resize', setVH);

  /* ==========================================================
     0 · SCROLL DWELL ENGINE
     Instead of mapping scroll linearly, we build a density
     curve that peaks at each content anchor. Scroll "almost
     stops" there, then accelerates between sections.
     ========================================================== */
  function makeDwell(centers, width = 0.05, peak = 3.2, N = 1400) {
    const dens = (x) => 1 + centers.reduce(
      (a, c) => a + (peak - 1) * Math.exp(-((x - c) ** 2) / (2 * width * width)), 0);
    const cum = new Float32Array(N + 1);
    for (let i = 1; i <= N; i++) cum[i] = cum[i - 1] + dens(i / N);
    const total = cum[N];
    for (let i = 0; i <= N; i++) cum[i] /= total;   // forward: raw -> effective
    return (raw) => {                               // invert by binary search
      const t = clamp(raw, 0, 1);
      let lo = 0, hi = N;
      while (lo < hi) { const m = (lo + hi) >> 1; if (cum[m] < t) lo = m + 1; else hi = m; }
      return lo / N;
    };
  }

  /* ==========================================================
     1 · SMOOTH SCROLL + VELOCITY SKEW
     ========================================================== */
  let lenis = null;
  function scroll() {
    if (reduce || !window.Lenis) return;
    lenis = new window.Lenis({
      duration: 1.1,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true, touchMultiplier: 1.6,
    });
    lenis.on('scroll', ST.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    window.__lenis = lenis;

    // subtle skew driven by scroll velocity — the trionn "weight"
    if (isTouch) return;
    const skewer = gsap.quickTo('.skewable', 'skewY', { duration: .5, ease: 'power3' });
    let v = 0;
    ST.create({
      onUpdate(self) { v = clamp(self.getVelocity() / -420, -3.2, 3.2); skewer(v); },
    });
  }

  /* ==========================================================
     2 · TEXT SPLITTING
     ========================================================== */
  function splitChars(el) {
    if (el.dataset.split) return $$('.ch', el);
    const words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    const out = [];
    words.forEach((w, i) => {
      const wrap = document.createElement('span');
      wrap.className = 'ww';
      [...w].forEach((c) => {
        const s = document.createElement('span');
        s.className = 'ch'; s.textContent = c;
        wrap.appendChild(s); out.push(s);
      });
      el.appendChild(wrap);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    el.dataset.split = '1';
    return out;
  }
  function maskLines(el) {
    return $$(':scope > *', el).map((c) => {
      const m = document.createElement('span');
      m.className = 'reveal-line';
      c.parentNode.insertBefore(m, c); m.appendChild(c);
      return c;
    });
  }

  /* ==========================================================
     3 · PRELOADER — slot-reel odometer
     ========================================================== */
  function buildReel() {
    const reel = $('.reel');
    if (!reel) return null;
    reel.innerHTML = '';
    const strips = [];
    for (let d = 0; d < 3; d++) {
      const slot = document.createElement('span'); slot.className = 'slot';
      const strip = document.createElement('span'); strip.className = 'strip';
      for (let n = 0; n <= 10; n++) {           // 0..9 then 0 again for a clean roll
        const i = document.createElement('i'); i.textContent = String(n % 10);
        strip.appendChild(i);
      }
      slot.appendChild(strip); reel.appendChild(slot); strips.push(strip);
    }
    return strips;
  }

  function preload() {
    const pre = $('#pre');
    if (!pre) {
      // the v198 loader replaced this one; wait for it to lift so the
      // hero's entrance is seen rather than played behind a cover
      return new Promise((res) => {
        if (!document.getElementById('preload')) return res();
        addEventListener('nk:preloaded', () => res(), { once: true });
        setTimeout(res, 6000);
      });
    }

    // the full loader is a first-impression, not a toll booth — show it
    // once per session, then let page transitions carry the navigation
    let seen = false;
    try { seen = sessionStorage.getItem('nk-seen') === '1'; } catch {}
    if (seen) {
      pre.style.display = 'none';
      document.body.dataset.preSkipped = '1';
      gsap.set('.curtain i', { scaleY: 0 });
      gsap.from('.marks i', { scale: 0, opacity: 0, duration: .7, ease: 'back.out(2)', stagger: .05 });
      return Promise.resolve();
    }
    try { sessionStorage.setItem('nk-seen', '1'); } catch {}

    const strips = buildReel();
    const bar = $('.pre-line i');
    document.body.classList.add('is-locked');

    const setReel = (v) => {
      if (!strips) return;
      const d = String(Math.round(v)).padStart(3, '0');
      strips.forEach((s, i) => { s.style.transform = `translateY(${-parseInt(d[i], 10)}em)`; });
    };

    const st = { v: 0 };
    const tl = gsap.timeline();

    tl.from('.marks i', { scale: 0, opacity: 0, duration: .8, ease: 'back.out(2)', stagger: .06 })
      .from('.pre-card', { scale: .82, opacity: 0, duration: 1.1, ease: 'expo.out' }, 0)
      .to(st, {
        v: 100, duration: reduce ? .2 : 2.3, ease: 'power2.inOut',
        onUpdate() { setReel(st.v); if (bar) bar.style.width = st.v + '%'; },
      }, .15)
      .to('.pre-foot, .pre-line', { opacity: 0, duration: .35, ease: 'power2.in' }, '-=.2')
      .to('.pre-card', { scale: 1.25, opacity: 0, filter: 'blur(18px)', duration: .85, ease: 'power3.inOut' }, '-=.1')
      .to('.curtain i', {
        scaleY: 0, duration: reduce ? .2 : 1, ease: 'expo.inOut',
        stagger: { each: .055 },
      }, '-=.4')
      .set(pre, { display: 'none' })
      .add(() => { document.body.classList.remove('is-locked'); ST.refresh(); });

    return tl.then();
  }

  /* ==========================================================
     4 · CURSOR + MAGNETIC
     ========================================================== */
  function cursor() {
    if (isTouch) return;
    const dot = $('#cur'), ring = $('#ring'), label = $('#ring b');
    if (!dot) return;
    const p = { x: innerWidth / 2, y: innerHeight / 2 }, r = { ...p };
    const dx = gsap.quickSetter(dot, 'x', 'px'), dy = gsap.quickSetter(dot, 'y', 'px');
    const rx = gsap.quickSetter(ring, 'x', 'px'), ry = gsap.quickSetter(ring, 'y', 'px');
    addEventListener('pointermove', (e) => { p.x = e.clientX; p.y = e.clientY; }, { passive: true });
    gsap.ticker.add(() => {
      dx(p.x - 3.5); dy(p.y - 3.5);
      r.x += (p.x - r.x) * .16; r.y += (p.y - r.y) * .16;
      rx(r.x - 20); ry(r.y - 20);
    });
    $$('a, button, .wcard, [data-cur]').forEach((el) => {
      const t = el.dataset.cur || '';
      el.addEventListener('pointerenter', () => {
        gsap.to(ring, { scale: t ? 2 : 1.55, duration: .45, ease: 'power3.out' });
        gsap.to(dot, { scale: t ? 0 : .6, duration: .3 });
        if (t) { label.textContent = t; gsap.to(label, { opacity: 1, duration: .3 }); }
      });
      el.addEventListener('pointerleave', () => {
        gsap.to(ring, { scale: 1, duration: .45, ease: 'power3.out' });
        gsap.to(dot, { scale: 1, duration: .3 });
        gsap.to(label, { opacity: 0, duration: .2 });
      });
    });
    /* The pull was unbounded: displacement is (cursor - centre) * s, and
       the cursor can sit half a button's width from the centre, so a
       175px button at s=.28 travelled 24px — twice the gap to the button
       beside it, which is why the two hero buttons climbed on top of
       each other. The travel is capped now, and the cap is derived from
       the real gap between siblings rather than guessed, so it stays
       correct if the spacing changes. */
    $$('[data-mag]').forEach((el) => {
      const s = parseFloat(el.dataset.mag) || .32;
      const cap = () => {
        const par = el.parentElement;
        const g = par ? parseFloat(getComputedStyle(par).columnGap) : NaN;
        // leave a third of the gap as clearance, and never travel more
        // than 16px whatever the layout allows
        return Math.min(16, Math.max(4, (g || 14) * 0.66));
      };
      el.addEventListener('pointermove', (e) => {
        const b = el.getBoundingClientRect(), m = cap();
        const clamp = (v) => Math.max(-m, Math.min(m, v));
        gsap.to(el, { x: clamp((e.clientX - (b.left + b.width / 2)) * s),
                      y: clamp((e.clientY - (b.top + b.height / 2)) * s),
                      duration: .6, ease: 'power3.out' });
      });
      el.addEventListener('pointerleave', () =>
        gsap.to(el, { x: 0, y: 0, duration: .9, ease: 'elastic.out(1,.4)' }));
    });
  }

  /* ==========================================================
     5 · GRADIENT FIELD
     Low-res canvas of soft radial blobs. Rendered small and
     upscaled by the browser — cheap enough to sit under
     backdrop-filter tiles without dropping frames.
     ========================================================== */
  function field() { $$('.fieldcv').forEach(makeField); }

  function makeField(cv) {
    if (!cv) return null;
    const ctx = cv.getContext('2d');
    const SCALE = 0.16;                       // render resolution
    let W = 0, H = 0, alive = true;
    const pointer = { x: .5, y: .5, tx: .5, ty: .5 };

    const blobs = [
      { r: .70, c: [120,118,116], ox: .30, oy: .62, sx: .00021, sy: .00017, ax: .16, ay: .12 },
      { r: .52, c: [140,138,136], ox: .62, oy: .34, sx: .00016, sy: .00025, ax: .20, ay: .16 },
      { r: .60, c: [ 90, 88, 86], ox: .82, oy: .80, sx: .00012, sy: .00019, ax: .18, ay: .14 },
      { r: .38, c: [160,158,156],ox: .18, oy: .20, sx: .00024, sy: .00013, ax: .14, ay: .18 },
    ];

    function size() {
      const b = cv.getBoundingClientRect();
      W = Math.max(2, Math.round(b.width * SCALE));
      H = Math.max(2, Math.round(b.height * SCALE));
      cv.width = W; cv.height = H;
    }

    addEventListener('pointermove', (e) => {
      pointer.tx = e.clientX / innerWidth; pointer.ty = e.clientY / innerHeight;
    }, { passive: true });

    function draw(t) {
      if (alive) {
        pointer.x += (pointer.tx - pointer.x) * .04;
        pointer.y += (pointer.ty - pointer.y) * .04;

        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = '#0a0a0b';
        ctx.fillRect(0, 0, W, H);
        ctx.globalCompositeOperation = 'lighter';

        for (const b of blobs) {
          const x = (b.ox + Math.sin(t * b.sx) * b.ax + (pointer.x - .5) * .10) * W;
          const y = (b.oy + Math.cos(t * b.sy) * b.ay + (pointer.y - .5) * .10) * H;
          const rad = b.r * Math.max(W, H);
          const g = ctx.createRadialGradient(x, y, 0, x, y, rad);
          g.addColorStop(0,   `rgba(${b.c[0]},${b.c[1]},${b.c[2]},.85)`);
          g.addColorStop(.42, `rgba(${b.c[0]},${b.c[1]},${b.c[2]},.28)`);
          g.addColorStop(1,   `rgba(${b.c[0]},${b.c[1]},${b.c[2]},0)`);
          ctx.fillStyle = g;
          ctx.beginPath(); ctx.arc(x, y, rad, 0, 6.2832); ctx.fill();
        }
      }
      requestAnimationFrame(draw);
    }

    size();
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(size, 160); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((e) => { alive = e[0].isIntersecting; }, { threshold: 0 }).observe(cv);
    }
    requestAnimationFrame(draw);
  }

  /* ==========================================================
     6 · TILE GRID
     Frosted tiles refract the field. They assemble on load,
     lift under the cursor, blow apart on hold, and dissolve
     tile-by-tile as the hero scrolls away.
     ========================================================== */
  function tiles() {
    const wrap = $('.tiles');
    if (!wrap) return;

    let cells = [];
    function build() {
      const cols = innerWidth < 861 ? 6 : innerWidth < 1300 ? 9 : 12;
      const size = wrap.clientWidth / cols;
      const rows = Math.max(3, Math.ceil(wrap.clientHeight / size));
      wrap.style.setProperty('--tc', cols);
      wrap.innerHTML = '';
      const frag = document.createDocumentFragment();
      cells = [];
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const d = document.createElement('div');
          d.className = 'tile';
          frag.appendChild(d);
          // outward direction from grid centre, precomputed for the dissolve
          const nx = (c + .5) / cols - .5;
          const ny = (r + .5) / rows - .5;
          const m = Math.hypot(nx, ny) || 1;
          cells.push({ el: d, c, r, cols, rows,
            ux: nx / m, uy: ny / m,
            spin: (Math.random() - .5) * 2,
            // distance from bottom-left focal point, used for staggering
            d: Math.hypot(c / cols - .15, r / rows - .85) });
        }
      }
      wrap.appendChild(frag);
      cells.sort((a, b) => a.d - b.d);
    }

    build();
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { build(); intro(0); }, 200); });

    function intro(delay = 2.15) {
      if (reduce) return;
      gsap.fromTo(cells.map(c => c.el),
        { opacity: 0, scale: .3, rotateX: -55, y: 40 },
        { opacity: 1, scale: 1, rotateX: 0, y: 0,
          duration: 1.15, ease: 'expo.out', delay,
          stagger: { each: .008, from: 'start' } });
    }
    intro();

    // THE moment: the grid comes apart as the hero scrolls away.
    // Tiles release one wave at a time from the bottom-left, drift
    // outward from the centre, tumble, and thin out.
    if (!reduce) {
      const ease = (t) => t * t * (3 - 2 * t);          // smoothstep
      ST.create({
        trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .55,
        onUpdate(self) {
          const p = self.progress;
          const n = cells.length;
          for (let i = 0; i < n; i++) {
            const c = cells[i];
            // staggered release — later tiles hold on longer
            const t = ease(clamp((p - (i / n) * .48) / .52, 0, 1));
            if (t <= 0) {
              c.el.style.opacity = '1';
              c.el.style.transform = 'translate3d(0,0,0)';
              continue;
            }
            const drift = t * t * 340;                   // accelerating spread
            c.el.style.opacity = String(1 - t);
            c.el.style.transform =
              `translate3d(${(c.ux * drift).toFixed(1)}px, ${(c.uy * drift - t * 120).toFixed(1)}px, 0)` +
              ` scale(${(1 - t * .62).toFixed(3)})` +
              ` rotate(${(t * c.spin * 26).toFixed(1)}deg)`;
          }
        },
      });
    }

    // cursor proximity lift
    if (!isTouch && !reduce) {
      let raf = 0, mx = -1e4, my = -1e4;
      addEventListener('pointermove', (e) => {
        mx = e.clientX; my = e.clientY;
        if (!raf) raf = requestAnimationFrame(() => {
          raf = 0;
          const b = wrap.getBoundingClientRect();
          if (my < b.top || my > b.bottom) return;
          for (const c of cells) {
            const t = c.el.getBoundingClientRect();
            const dist = Math.hypot(t.left + t.width / 2 - mx, t.top + t.height / 2 - my);
            const k = clamp(1 - dist / 260, 0, 1);
            c.el.style.background = `rgba(255,246,240,${(.045 + k * .10).toFixed(3)})`;
            c.el.style.borderColor = `rgba(255,240,230,${(.10 + k * .30).toFixed(3)})`;
          }
        });
      }, { passive: true });
    }

  }

  /* ==========================================================
     7 · AMBIENT DUST
     ========================================================== */
  function dust() {
    const cv = $('#dust');
    if (!cv || reduce) return;
    const ctx = cv.getContext('2d');
    let W, H, ps = [];
    const size = () => {
      W = cv.width = innerWidth; H = cv.height = innerHeight;
      ps = Array.from({ length: 44 }, () => ({
        x: Math.random() * W, y: Math.random() * H,
        r: .3 + Math.random() * 1.4,
        vx: (Math.random() - .5) * .16, vy: (Math.random() - .5) * .16,
        a: .05 + Math.random() * .3,
      }));
    };
    size();
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(size, 200); });
    (function loop() {
      ctx.clearRect(0, 0, W, H);
      for (const p of ps) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
        if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
        ctx.fillStyle = `rgba(255,226,200,${p.a})`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fill();
      }
      requestAnimationFrame(loop);
    })();
  }

  /* ==========================================================
     8 · REVEALS + LINE DRAW
     ========================================================== */
  function reveals() {
    $$('[data-chars]').forEach((el) => {
      const ch = splitChars(el);
      gsap.set(ch, { yPercent: 115, opacity: 0 });
      ST.create({ trigger: el, start: 'top 88%', once: true,
        onEnter: () => gsap.to(ch, { yPercent: 0, opacity: 1, duration: 1.1,
          ease: 'expo.out', stagger: { each: .016 } }) });
    });

    $$('[data-lines]').forEach((el) => {
      const ln = maskLines(el);
      gsap.set(ln, { yPercent: 104 });
      ST.create({ trigger: el, start: 'top 88%', once: true,
        onEnter: () => gsap.to(ln, { yPercent: 0, duration: 1.05, ease: 'expo.out', stagger: .07 }) });
    });

    $$('[data-rise]').forEach((el) => {
      const d = parseFloat(el.dataset.rise) || 0;
      // hero items sit at the bottom edge on load — a scroll trigger there
      // would never fire, so play them off the preloader timeline instead
      const inHero = !!el.closest('.hero');
      gsap.fromTo(el, { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 1, ease: 'expo.out',
          delay: inHero ? 2.5 + d : d,
          scrollTrigger: inHero ? undefined : { trigger: el, start: 'top 91%', once: true } });
    });

    // blur-in glass panels
    $$('[data-glass-in]').forEach((el) => {
      gsap.fromTo(el, { opacity: 0, y: 46, filter: 'blur(14px)' },
        { opacity: 1, y: 0, filter: 'blur(0px)', duration: 1.2, ease: 'expo.out',
          scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
    });

    // borders drawing themselves in
    $$('.lined').forEach((el) => {
      ['t h','b h','l v','r v'].forEach((k) => {
        const i = document.createElement('i');
        i.className = 'ln ' + k.split(' ')[1] + ' ' + k.split(' ')[0];
        el.appendChild(i);
      });
      ST.create({ trigger: el, start: 'top 90%', once: true,
        onEnter: () => gsap.to($$('.ln', el), {
          scaleX: 1, scaleY: 1, duration: .9, ease: 'expo.out', stagger: .07 }) });
    });

    $$('[data-par]').forEach((el) => {
      const a = parseFloat(el.dataset.par) || 10;
      gsap.fromTo(el, { yPercent: -a }, { yPercent: a, ease: 'none',
        scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  }

  /* ==========================================================
     9 · MARQUEES + LOGO ROWS
     ========================================================== */
  function marquees() {
    $$('.mq, .logos').forEach((wrap) => {
      const track = $('.mq-track, .logos-track', wrap);
      if (!track) return;
      const base = parseFloat(wrap.dataset.speed) || .55;
      const dir = wrap.dataset.dir === 'right' ? 1 : -1;
      const seed = track.innerHTML;
      let guard = 0;
      while (track.scrollWidth < wrap.offsetWidth * 2 && guard++ < 12) track.innerHTML += seed;
      const half = track.scrollWidth / 2;
      let x = dir === 1 ? -half : 0, extra = 0;

      ST.create({ trigger: wrap, start: 'top bottom', end: 'bottom top',
        onUpdate(self) { extra = self.getVelocity() * -.0055; } });

      gsap.ticker.add(() => {
        x += (base + Math.min(Math.abs(extra), 24)) * dir;
        extra *= .92;
        if (x <= -half) x += half;
        if (x >= 0) x -= half;
        track.style.transform = `translate3d(${x}px,0,0)`;
      });
    });
  }

  /* ==========================================================
     10 · VERTICAL WORD COLUMNS
     ========================================================== */
  function columns() {
    const host = $('.cols');
    if (!host) return;
    const words = (host.dataset.words || 'Research,Design,Systems,Ship').split(',');
    host.innerHTML = '';
    const strips = [];
    for (let i = 0; i < 4; i++) {
      const col = document.createElement('div'); col.className = 'col';
      const strip = document.createElement('div'); strip.className = 'col-strip';
      for (let k = 0; k < 14; k++) {
        const s = document.createElement('span');
        s.textContent = words[(k + i) % words.length];
        if ((k + i) % words.length === i % words.length) s.className = 'on';
        strip.appendChild(s);
      }
      col.appendChild(strip); host.appendChild(col);
      strips.push({ strip, speed: (i % 2 ? -1 : 1) * (0.35 + i * 0.16), y: -strip.scrollHeight / 3 });
    }
    requestAnimationFrame(() => {
      strips.forEach((s) => { s.h = s.strip.scrollHeight / 2; });
      if (reduce) return;
      gsap.ticker.add(() => {
        strips.forEach((s) => {
          s.y += s.speed;
          if (s.y <= -s.h) s.y += s.h;
          if (s.y >= 0) s.y -= s.h;
          s.strip.style.transform = `translate3d(0,${s.y}px,0)`;
        });
      });
    });
  }

  /* ==========================================================
     11 · HORIZONTAL RAIL (dwell-paced)
     ========================================================== */
  let railST = null;
  function rail() {
    if (isTouch) return;
    const sec = $('.railsec'), track = $('.rail-track'), bar = $('.rail-bar i');
    if (!sec || !track) return;
    const dist = () => Math.max(1, track.scrollWidth - innerWidth + 80);

    // dwell anchors — recomputed on refresh so filtering re-paces the rail
    let dwell = (x) => x;
    const rebuild = () => {
      const n = $$('.wcard:not(.is-out)', track).length || 1;
      dwell = makeDwell(Array.from({ length: n }, (_, i) => (i + .5) / n), .055, 2.1);
    };
    rebuild();

    railST = ST.create({
      trigger: sec, start: 'top top', end: () => '+=' + dist() * 1.35,
      pin: true, scrub: .8, invalidateOnRefresh: true, anticipatePin: 1,
      onRefresh: rebuild,
      onUpdate(self) {
        const p = reduce ? self.progress : dwell(self.progress);
        track.style.transform = `translate3d(${-p * dist()}px,0,0)`;
        if (bar) bar.style.width = (self.progress * 100).toFixed(2) + '%';
      },
    });
  }

  /* ==========================================================
     12 · STICKY STACKED SERVICE CARDS
     ========================================================== */
  function stack() {
    const cards = $$('.scard');
    if (!cards.length || reduce) return;
    cards.forEach((card, i) => {
      if (i === cards.length - 1) return;
      gsap.to(card, {
        scale: 1 - (cards.length - i) * .022,
        opacity: .45,
        ease: 'none',
        scrollTrigger: {
          trigger: cards[i + 1],
          start: 'top 80%',
          end: 'top 20%',
          scrub: true,
        },
      });
    });
  }

  /* ==========================================================
     13 · TAG BAR — filters the work rail
     Built from the data-tags on each card, so counts can never
     drift out of sync with the actual projects.
     ========================================================== */
  function tagbar() {
    const host = $('.tagbar');
    const track = $('[data-cards]');
    if (!host || !track) return;

    const cards = $$('.wcard', track);
    const order = ['Fintech', 'SaaS', 'Mobile', 'AI', 'Data viz', 'E-commerce', 'Brand & Web'];
    const counts = new Map();
    cards.forEach((c) => (c.dataset.tags || '').split('|').map((s) => s.trim()).filter(Boolean)
      .forEach((t) => counts.set(t, (counts.get(t) || 0) + 1)));

    const tags = ['All', ...order.filter((t) => counts.has(t))];
    const note = $('.tagbar-note');
    host.innerHTML = '';

    const apply = (tag) => {
      let shown = 0;
      cards.forEach((c) => {
        const list = (c.dataset.tags || '').split('|').map((s) => s.trim());
        const hit = tag === 'All' || list.includes(tag);
        c.classList.toggle('is-out', !hit);
        if (hit) shown++;
      });
      $$('.tag', host).forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.tag === tag)));
      if (note) note.textContent = tag === 'All'
        ? `Showing all ${shown} projects`
        : `Showing ${shown} ${tag} project${shown === 1 ? '' : 's'}`;

      // rewind the rail (home only), then let ScrollTrigger recompute
      if (track.classList.contains('rail-track')) {
        track.style.transform = 'translate3d(0,0,0)';
        const barFill = $('.rail-bar i'); if (barFill) barFill.style.width = '0%';
      }
      ST.refresh();
    };

    tags.forEach((t) => {
      const b = document.createElement('button');
      b.className = 'tag';
      b.type = 'button';
      b.dataset.tag = t;
      b.setAttribute('aria-pressed', String(t === 'All'));
      b.setAttribute('aria-label', t === 'All' ? 'Show all projects' : `Filter work by ${t}`);
      b.innerHTML =
        `<span class="fill"></span>` +
        `<span class="cnt">${t === 'All' ? cards.length : counts.get(t)}</span>` +
        `<span class="lbl">${t}</span>`;
      b.addEventListener('click', () => apply(t));
      host.appendChild(b);
    });

    apply('All');

    // roving arrow-key navigation across the bar
    host.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      const all = $$('.tag', host);
      const i = all.indexOf(document.activeElement);
      if (i < 0) return;
      e.preventDefault();
      all[(i + (e.key === 'ArrowRight' ? 1 : all.length - 1)) % all.length].focus();
    });
  }

  /* ==========================================================
     14 · COUNTERS
     ========================================================== */
  function counters() {
    $$('[data-count]').forEach((el) => {
      const target = parseFloat(el.dataset.count);
      const suf = el.dataset.suffix || '';
      const o = { v: 0 };
      ST.create({ trigger: el, start: 'top 90%', once: true,
        onEnter: () => gsap.to(o, { v: target, duration: 1.8, ease: 'power3.out',
          onUpdate: () => { el.textContent = Math.round(o.v) + suf; } }) });
    });
  }

  /* ==========================================================
     15 · CHAPTER MARKERS
     ========================================================== */
  function chapters() {
    // dot markers on the home page and the case-study section nav share
    // the same scroll-spy — whichever exists on this page gets wired up
    const links = $$('.chapters a, .casenav a');
    if (!links.length) return;
    links.forEach((a) => {
      // only in-page anchors are chapters; the section nav also carries a
      // plain link back to /work/, which is not a selector at all
      const h = a.getAttribute('href') || '';
      if (h[0] !== '#' || h.length < 2) return;
      const t = $(h);
      if (!t) return;
      ST.create({
        trigger: t, start: 'top 45%', end: 'bottom 45%',
        onToggle(self) {
          a.classList.toggle('on', self.isActive);
          // keep the active pill in view on narrow screens
          if (self.isActive && a.closest('.casenav') && a.scrollIntoView) {
            a.scrollIntoView({ block: 'nearest', inline: 'nearest' });
          }
        },
      });
    });
  }

  /* ==========================================================
     16 · FULLSCREEN MENU
     ========================================================== */
  function menu() {
    const btn = $('.burger'), panel = $('#menu');
    if (!btn || !panel) return;
    const links = maskLines($('.mlinks'));
    gsap.set(links, { yPercent: 110 });
    let open = false;

    const toggle = (want = !open) => {
      open = want;
      btn.classList.toggle('x', open);
      btn.setAttribute('aria-expanded', String(open));
      panel.classList.toggle('open', open);
      panel.setAttribute('aria-hidden', String(!open));
      if (lenis) open ? lenis.stop() : lenis.start();
      gsap.to(panel, { clipPath: open ? 'inset(0 0 0% 0)' : 'inset(0 0 100% 0)',
        duration: .8, ease: 'expo.inOut' });
      gsap.to(links, { yPercent: open ? 0 : 110, duration: .8,
        ease: 'expo.out', delay: open ? .18 : 0, stagger: .05 });
    };

    btn.addEventListener('click', () => toggle());
    $$('a', panel).forEach((a) => a.addEventListener('click', () => toggle(false)));
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && open) toggle(false); });
  }

  /* ==========================================================
     16b · EXPERIENCE PAGE
     Expandable roles, certification filter, language bars.
     ========================================================== */
  function experience() {
    // ── roles that open ────────────────────────────────────
    $$('.xrow[data-expand]').forEach((row) => {
      const detail = $('.xdetail', row);
      const head = $('.xhead', row);
      if (!detail || !head) return;

      // make the header itself the control, so it is keyboard reachable
      head.setAttribute('role', 'button');
      head.setAttribute('tabindex', '0');
      head.setAttribute('aria-expanded', 'false');

      const toggle = () => {
        const open = row.hasAttribute('data-open');
        if (open) {
          row.removeAttribute('data-open');
          gsap.to(detail, { height: 0, duration: .45, ease: 'expo.inOut' });
        } else {
          row.setAttribute('data-open', '');
          gsap.set(detail, { height: 'auto' });
          gsap.from(detail, { height: 0, duration: .55, ease: 'expo.out' });
        }
        head.setAttribute('aria-expanded', String(!open));
      };

      head.addEventListener('click', toggle);
      head.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
      });
    });

    // ── certification filter ───────────────────────────────
    const bar = $('.certbar');
    if (bar) {
      const cards = $$('.cert');
      const note = $('.tagbar-note');
      const apply = (g) => {
        let shown = 0;
        cards.forEach((c) => {
          const hit = g === 'All' || c.dataset.cgroup === g;
          c.classList.toggle('is-out', !hit);
          if (hit) shown++;
        });
        $$('button', bar).forEach((b) =>
          b.setAttribute('aria-pressed', String(b.dataset.cgroup === g)));
        if (note) note.textContent = g === 'All'
          ? `Showing all ${shown} certifications`
          : `Showing ${shown} from ${g.replace(/&amp;/g, '&')}`;
      };
      $$('button', bar).forEach((b) => b.addEventListener('click', () => apply(b.dataset.cgroup)));
      apply('All');

      bar.addEventListener('keydown', (e) => {
        if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
        const all = $$('button', bar);
        const i = all.indexOf(document.activeElement);
        if (i < 0) return;
        e.preventDefault();
        all[(i + (e.key === 'ArrowRight' ? 1 : all.length - 1)) % all.length].focus();
      });
    }

    // ── language proficiency bars ──────────────────────────
    $$('.lang .bar i').forEach((el) => {
      const pct = el.dataset.fill || 0;
      ST.create({
        trigger: el, start: 'top 92%', once: true,
        onEnter: () => gsap.to(el, { width: pct + '%', duration: 1.3, ease: 'expo.out' }),
      });
    });
  }

  /* ==========================================================
     17 · ANCHORS
     ========================================================== */
  function anchors() {
    $$('a[href^="#"]').forEach((a) => {
      a.addEventListener('click', (e) => {
        const t = $(a.getAttribute('href'));
        if (!t) return;
        e.preventDefault();
        lenis ? lenis.scrollTo(t, { duration: 1.4 }) : t.scrollIntoView({ behavior: 'smooth' });
      });
    });
  }

  /* ==========================================================
     18 · PAGE TRANSITIONS
     Real multi-page site, but navigation still feels continuous:
     a curtain wipes up on click, the browser loads the next
     document, and the curtain wipes away on arrival.
     ========================================================== */
  function transitions() {
    const cur = $('#trans');
    if (!cur) return;
    const label = $('#trans span');

    // arriving: wipe the curtain away
    const arrive = () => {
      gsap.set(cur, { clipPath: 'inset(0 0 0% 0)' });
      gsap.set(label, { opacity: 1 });
      gsap.timeline()
        .to(label, { opacity: 0, duration: .3, ease: 'power2.in' })
        .to(cur, { clipPath: 'inset(0 0 100% 0)', duration: .85, ease: 'expo.inOut' }, '-=.1');
    };

    const internal = (a) => {
      const href = a.getAttribute('href');
      if (!href || a.target === '_blank' || a.hasAttribute('download')) return false;
      if (/^(#|mailto:|tel:|https?:\/\/)/.test(href)) {
        // same-origin absolute links still count
        if (!/^https?:\/\//.test(href)) return false;
        try { if (new URL(href).origin !== location.origin) return false; } catch { return false; }
      }
      return true;
    };

    $$('a[href]').forEach((a) => {
      if (!internal(a)) return;
      a.addEventListener('click', (e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        const url = a.href;
        if (url === location.href) { e.preventDefault(); return; }
        e.preventDefault();
        if (reduce) { location.href = url; return; }
        gsap.timeline({ onComplete: () => { location.href = url; } })
          .set(label, { textContent: a.dataset.trans || a.textContent.trim().slice(0, 18) })
          .to(cur, { clipPath: 'inset(0 0 0% 0)', duration: .7, ease: 'expo.inOut' })
          .to(label, { opacity: 1, duration: .3 }, '-=.35');
      });
    });

    // bfcache restore (browser back) — make sure we never stay covered
    addEventListener('pageshow', (e) => { if (e.persisted) arrive(); });
    return arrive;
  }

  /* ==========================================================
     19 · CASE STUDY TABS
     Real tabs: arrow keys move between them, only the open
     panel is in the accessibility tree.
     ========================================================== */
  function tabs() {
    const list = $('.tablist');
    if (!list) return;
    const btns = $$('button', list);
    const panels = $$('.tabpanel');

    const open = (i, focus = false) => {
      btns.forEach((b, k) => {
        const on = k === i;
        b.setAttribute('aria-selected', String(on));
        b.tabIndex = on ? 0 : -1;
      });
      panels.forEach((p, k) => {
        if (k === i) { p.setAttribute('data-open', ''); p.removeAttribute('hidden'); }
        else { p.removeAttribute('data-open'); p.setAttribute('hidden', ''); }
      });
      if (focus) btns[i].focus();
      const live = panels[i];
      if (live && !reduce) gsap.fromTo(live, { opacity: 0, y: 14 },
        { opacity: 1, y: 0, duration: .55, ease: 'expo.out' });
    };

    btns.forEach((b, i) => b.addEventListener('click', () => open(i)));
    list.addEventListener('keydown', (e) => {
      const i = btns.indexOf(document.activeElement);
      if (i < 0) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); open((i + 1) % btns.length, true); }
      if (e.key === 'ArrowLeft')  { e.preventDefault(); open((i - 1 + btns.length) % btns.length, true); }
      if (e.key === 'Home')       { e.preventDefault(); open(0, true); }
      if (e.key === 'End')        { e.preventDefault(); open(btns.length - 1, true); }
    });
    open(0);
  }

  /* ==========================================================
     20 · SHOWCASE PARALLAX
     ========================================================== */
  function showcase() {
    $$('.showcase img').forEach((img) => {
      gsap.fromTo(img, { yPercent: -12 }, {
        yPercent: 0, ease: 'none',
        scrollTrigger: { trigger: img.closest('.showcase'), start: 'top bottom', end: 'bottom top', scrub: true },
      });
    });
  }

  /* ==========================================================
     21 · CONTACT FORM
     No backend: composes a pre-filled email so nothing the
     visitor typed can be silently swallowed.
     ========================================================== */
  function contactForm() {
    const form = $('#enquiry');
    if (!form) return;
    const err = (name) => $(`[data-err="${name}"]`, form);

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      let ok = true;

      const fail = (name, msg) => { ok = false; const el = err(name); if (el) el.textContent = msg; };
      ['name', 'email', 'message'].forEach((k) => { const el = err(k); if (el) el.textContent = ''; });

      if (!data.name?.trim()) fail('name', 'Please add your name.');
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email || '')) fail('email', 'That email address looks incomplete.');
      if ((data.message || '').trim().length < 10) fail('message', 'A sentence or two about the project, please.');
      if (!ok) { form.querySelector('.err:not(:empty)')?.closest('.field')?.querySelector('input,textarea')?.focus(); return; }

      const subject = `Project enquiry — ${data.name}${data.company ? ' · ' + data.company : ''}`;
      const body =
        `Name: ${data.name}\n` +
        `Email: ${data.email}\n` +
        (data.company ? `Company: ${data.company}\n` : '') +
        (data.budget ? `Budget: ${data.budget}\n` : '') +
        `\n${data.message}\n`;
      location.href = `mailto:contact@khomeriki.design?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

      const note = $('.form-note', form);
      if (note) note.textContent = 'Opening your mail app — if nothing happens, write to contact@khomeriki.design directly.';
    });
  }

  /* ==========================================================
     AURORA — the colour field the glass refracts
     Each blob drifts on its own slow cycle and parallaxes with
     scroll, so no two panels ever frost the same thing twice.
     ========================================================== */
  function aurora() {
    const layer = $('.aurora');
    if (!layer) return;
    const blobs = $$('i', layer);
    if (!blobs.length) return;

    if (reduce) { gsap.set(blobs, { opacity: .4 }); return; }

    // independent drift — prime-ish durations keep them out of phase
    const drift = [
      { x: 120, y: -90,  d: 34 }, { x: -140, y: 110, d: 41 },
      { x: 90,  y: 130,  d: 47 }, { x: -110, y: -80, d: 29 },
      { x: 150, y: -60,  d: 53 },
    ];
    blobs.forEach((b, i) => {
      const s = drift[i % drift.length];
      gsap.to(b, {
        xPercent: s.x / 6, yPercent: s.y / 6,
        duration: s.d, ease: 'sine.inOut',
        repeat: -1, yoyo: true,
      });
    });

    // parallax: the field slides slower than the page, so scrolling
    // continuously changes what sits behind each panel
    gsap.to(layer, {
      yPercent: -14,
      ease: 'none',
      scrollTrigger: { trigger: document.body, start: 'top top', end: 'bottom bottom', scrub: 1.2 },
    });
  }

  /* ==========================================================
     GLASS SPECULAR — cursor-tracked highlight on every panel
     Writes --mx/--my only for the panel under the pointer, and
     only on rAF, so this stays off the scroll critical path.
     ========================================================== */
  function specular() {
    if (isTouch || reduce) return;
    const panels = $$('.glass');
    if (!panels.length) return;

    let active = null, px = 0, py = 0, queued = false;

    const paint = () => {
      queued = false;
      if (!active) return;
      const r = active.getBoundingClientRect();
      active.style.setProperty('--mx', `${((px - r.left) / r.width) * 100}%`);
      active.style.setProperty('--my', `${((py - r.top) / r.height) * 100}%`);
    };

    addEventListener('pointermove', (e) => {
      const el = e.target.closest?.('.glass');
      if (el !== active && active) { active.style.removeProperty('--mx'); active.style.removeProperty('--my'); }
      active = el;
      if (!active) return;
      px = e.clientX; py = e.clientY;
      if (!queued) { queued = true; requestAnimationFrame(paint); }
    }, { passive: true });
  }

  /* ==========================================================
     BOOT
     ========================================================== */
  const started = preload();

  (async () => {
    if (document.fonts?.ready) {
      try { await Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 2500))]); } catch {}
    }
    try {
      scroll(); cursor(); aurora(); specular(); field(); tiles();
      reveals(); marquees(); columns(); rail(); stack();
      tagbar(); counters(); chapters(); menu(); anchors();
      showcase(); experience(); contactForm();
      const arrive = transitions();
      // wipe the arrival curtain once the page is actually ready
      const noLoader = !$('#pre') || document.body.dataset.preSkipped === '1';
      if (arrive && noLoader) arrive();
      ST.refresh();
    } catch (err) {
      console.error('[nk-glass] init failed:', err);
      document.body.classList.remove('is-locked');
      const p = $('#pre'); if (p) p.style.display = 'none';
      gsap.set('.curtain i', { scaleY: 0 });
    }
    started.then(() => ST.refresh());
    addEventListener('load', () => ST.refresh());
  })();
})();

/* ══════════════════════════════════════════════════════════════════
   HOME — the two scroll mechanics the reference is built on.
   Both read scroll once per frame off the existing rAF loop rather
   than binding their own listeners, so they cost nothing when the
   home page is not the page being viewed.
   ══════════════════════════════════════════════════════════════════ */
(function () {
  if (document.body.dataset.page !== 'home') return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 1. the headline fills word by word as it crosses the screen ──
     Each word turns on when the scroll has carried the block past its
     own share of the reveal. It is the reference's one piece of
     scroll-linked typography and it is what makes the section feel
     read rather than displayed. */
  const fillEl = document.querySelector('[data-wordfill]');
  const words = fillEl ? [...fillEl.querySelectorAll('.w')] : [];
  function runFill() {
    if (!fillEl || !words.length) return;
    if (reduce) { words.forEach(w => w.classList.add('on')); return; }
    const r = fillEl.getBoundingClientRect();
    const vh = innerHeight;
    // 0 when the block's top reaches 78% of the viewport, 1 at 26%
    const p = Math.max(0, Math.min(1, (vh * 0.78 - r.top) / (vh * 0.52)));
    const n = Math.round(p * words.length);
    words.forEach((w, i) => w.classList.toggle('on', i < n));
  }

  /* ── 2. the ribbon ───────────────────────────────────────────────
     One strip, several screens wide, sliding left across the section's
     scroll. The strip is position:sticky so the browser does the pin;
     JS only supplies the horizontal offset, which keeps the whole thing
     on the compositor and off the main thread. */
  const pin   = document.querySelector('.s34');
  const strip = document.querySelector('[data-hstrip]');
  const bar   = document.querySelector('.hs-bar i');
  const lead  = strip && strip.querySelector('.hs-lead');
  let travel = 0;
  function measure() {
    if (!strip) return;
    // scrollWidth already includes the trailing pad that leaves the last
    // plate centred at the end of the travel, so this needs no extra maths
    travel = Math.max(0, strip.scrollWidth - innerWidth);
  }
  function runTrain() {
    if (!pin || !strip) return;
    if (matchMedia('(max-width: 860px)').matches) {
      strip.style.transform = '';
      if (lead) { lead.style.transform = ''; lead.classList.remove('is-pinned'); }
      return;
    }
    const r = pin.getBoundingClientRect();
    const total = pin.offsetHeight - innerHeight;
    const p = Math.max(0, Math.min(1, -r.top / (total || 1)));
    strip.style.transform = `translate3d(${-p * travel}px,0,0)`;
    if (bar) bar.style.width = (p * 100).toFixed(2) + '%';
    // the statement stops at the left edge and the screens slide on
    // underneath it, instead of the heading being carried off-screen
    // half-read while the cards pass
    if (lead) {
      const over = Math.max(0, -(lead.offsetLeft - p * travel));
      lead.style.transform = over ? `translate3d(${over}px,0,0)` : '';
      lead.classList.toggle('is-pinned', over > 0);
    }
  }

  measure();
  addEventListener('resize', measure, { passive: true });
  // images arriving change the track width
  addEventListener('load', measure);

  let ticking = false;
  function frame() { runFill(); runTrain(); ticking = false; }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── 3. the film: pause it when it is off screen ─────────────────
     A looping background video that keeps decoding behind four
     screens of content is the most expensive thing on a page like
     this, and nobody is watching it. */
  document.querySelectorAll('.gfilm-v, .gcta-v').forEach(v => {
    if (reduce) { v.removeAttribute('autoplay'); v.pause(); return; }
    new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { const p = v.play(); if (p) p.catch(() => {}); }
      else v.pause();
    }), { threshold: .01 }).observe(v);
  });
})();

/* ══════════════════════════════════════════════════════════════════════
   v182 · the hero film, scrubbed by the pointer
   ----------------------------------------------------------------------
   120 stills instead of a <video>. A video element cannot be seeked
   frame-exact at pointer speed — currentTime assignments queue up and
   the decoder stalls — so the film is decoded once into images and the
   pointer just picks which one is on screen.

   The pointer's position across the viewport maps to a position in the
   film, so moving left rewinds and moving right runs it on. That is
   reversible and learnable in about a second, which accumulating total
   travel is not. A lerp sits between the target and the drawn frame so
   a flick of the wrist reads as momentum rather than a jump cut.

   With no pointer — touch, or someone who has asked for less motion —
   it falls back to playing gently on its own, or to a single frame.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  const cv = document.getElementById('s1film');
  if (!cv) return;

  const N      = +cv.dataset.frames || 120;
  const BASE   = cv.dataset.src || '/assets/home/hero-frames/';
  const poster = document.querySelector('.s1-poster');
  const ctx    = cv.getContext('2d', { alpha: false });
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine   = matchMedia('(pointer: fine)').matches;

  const pad    = (n) => String(n).padStart(3, '0');
  const frames = new Array(N);
  let ready = 0, first = null;

  /* Load in two passes: every eighth frame first, so the film is
     scrubbable end to end within a few hundred milliseconds, then the
     rest to fill in. Loading 1..120 in order would leave the right half
     of the screen dead while the left was already interactive. */
  const order = [];
  for (let step = 8; step >= 1; step >>= 1)
    for (let i = 0; i < N; i += step) if (!order.includes(i)) order.push(i);

  order.forEach((i) => {
    const im = new Image();
    im.decoding = 'async';
    im.onload = () => {
      frames[i] = im; ready++;
      if (first === null) { first = im; size(); draw(); }
      if (ready > 6 && poster) poster.classList.add('is-off');
    };
    im.src = `${BASE}f${pad(i + 1)}.webp`;
  });

  /* nearest loaded frame, so a gap never blanks the canvas */
  function pick(i) {
    i = Math.max(0, Math.min(N - 1, Math.round(i)));
    if (frames[i]) return frames[i];
    for (let d = 1; d < N; d++) {
      if (frames[i - d]) return frames[i - d];
      if (frames[i + d]) return frames[i + d];
    }
    return null;
  }

  let dpr = 1, cw = 0, ch = 0;
  function size() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    cw  = cv.clientWidth; ch = cv.clientHeight;
    cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr);
    drawn = -1;                      // force a repaint at the new size
  }

  let cur = 0, target = 0, drawn = -1;
  function draw() {
    const im = pick(cur);
    if (!im || !cw) return;
    // cover, centred — the same geometry object-fit:cover would give
    const s = Math.max(cv.width / im.width, cv.height / im.height);
    const w = im.width * s, h = im.height * s;
    ctx.drawImage(im, (cv.width - w) / 2, (cv.height - h) / 2, w, h);
  }

  if (fine && !reduce) {
    addEventListener('pointermove', (e) => {
      const r = cv.getBoundingClientRect();
      if (r.bottom < 0) return;                   // hero is off screen
      const p = Math.max(0, Math.min(1, (e.clientX - r.left) / (r.width || 1)));
      target = p * (N - 1);
    }, { passive: true });
  }

  let t0 = performance.now();
  function tick(now) {
    const dt = Math.min(64, now - t0); t0 = now;
    if (!fine && !reduce) target = (target + dt * 0.018) % (N - 1);  // ~18fps drift
    // frame-rate independent easing: same feel at 60Hz and 120Hz
    cur += (target - cur) * (1 - Math.pow(0.001, dt / 1000));
    if (Math.abs(cur - drawn) > 0.4) { drawn = cur; draw(); }
    requestAnimationFrame(tick);
  }
  if (!reduce) requestAnimationFrame(tick);

  addEventListener('resize', () => { size(); draw(); }, { passive: true });
})();

/* ══════════════════════════════════════════════════════════════════════
   v191 · the hero field, drawn
   ----------------------------------------------------------------------
   A lens-shaped cloud of dots suspended over nothing, rolling slowly,
   graphite on #EBEBEB, turning red under the pointer.

   Drawn rather than filmed for three reasons. Generative video could not
   hold the geometry — asked for an undulating dot surface it produced a
   polka-dot floor in perspective. Two clips, one graphite and one red,
   could never have matched frame for frame, so the hover would have read
   as a dissolve between two different animations rather than as one
   thing changing colour. And here the colour is a single variable the
   renderer interpolates, so the transition is exact by construction and
   costs nothing to ship.

   Shape: a parametric sheet. u runs along the length, v across it. The
   width tapers as sqrt(1 - u^2), which is what gives the pointed tips at
   both ends instead of a rectangular slab. Height is two sine waves at
   different frequencies crossing each other, damped by the same envelope
   so the edges settle flat rather than flapping.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  const cv = document.getElementById('s1field');
  if (!cv) return;   // retired at v198 — the hero is the space field below

  const ctx    = cv.getContext('2d', { alpha: false });
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const GROUND  = '#ebebeb';
  const CALM    = [ 63,  63,  63];     // --paper
  const HOT     = [255,   0,  92];     // --ember, the site's one hot colour
  const NU = 132, NV = 34;             // dots along the length / across it

  /* ---- the sprite ---------------------------------------------------
     4,488 arc() calls a frame is not free, and every dot is the same
     circle at a different size. One cached bitmap drawn 4,488 times is
     an order of magnitude cheaper. The heat ramp is quantised into 24
     bitmaps built once at start-up rather than tinted per dot — at 60fps
     nobody can see the step, and it keeps the inner loop to one
     drawImage with no per-dot allocation. */
  const STEPS = 24;
  const SPRITES = [];
  for (let k = 0; k <= STEPS; k++) {
    const h = k / STEPS;
    const c = document.createElement('canvas');
    c.width = c.height = 24;
    const g = c.getContext('2d');
    g.fillStyle = 'rgb(' +
      Math.round(CALM[0] + (HOT[0] - CALM[0]) * h) + ',' +
      Math.round(CALM[1] + (HOT[1] - CALM[1]) * h) + ',' +
      Math.round(CALM[2] + (HOT[2] - CALM[2]) * h) + ')';
    g.beginPath(); g.arc(12, 12, 10, 0, Math.PI * 2); g.fill();
    SPRITES.push(c);
  }

  let dpr = 1, W = 0, H = 0;
  function size() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
  }

  /* pointer: distance-weighted, so the field warms where the cursor is
     rather than flipping the whole thing at once — the shape stays one
     object with a hot spot on it, which is more legible than a switch. */
  let px = .5, py = .5, heat = 0, wantHeat = 0;
  cv.parentElement.addEventListener('pointermove', (e) => {
    const r = cv.getBoundingClientRect();
    px = (e.clientX - r.left) / (r.width  || 1);
    py = (e.clientY - r.top)  / (r.height || 1);
    wantHeat = 1;
  }, { passive: true });
  cv.parentElement.addEventListener('pointerleave', () => { wantHeat = 0; }, { passive: true });

  const TILT = 0.52, DIST = 3.1;
  const RADIUS = 0.17;                 // of viewport height
  const RAD2   = RADIUS * RADIUS;
  let t = 0, last = performance.now();

  function frame(now) {
    const dt = Math.min(64, now - last); last = now;
    t += dt * 0.00038;
    heat += (wantHeat - heat) * (1 - Math.pow(0.004, dt / 1000));

    ctx.fillStyle = GROUND;
    ctx.fillRect(0, 0, cv.width, cv.height);

    const cx = cv.width / 2, cy = cv.height / 2;
    const aspect = cv.width / cv.height;
    const scale = Math.min(cv.width / 2.45, cv.height / 1.15);
    const ct = Math.cos(TILT), st = Math.sin(TILT);

    // v back-to-front: with a tilt about X the depth order along v is
    // monotonic, so the rows can be drawn in order and no per-frame sort
    // of 4,488 points is needed.
    for (let j = 0; j < NV; j++) {
      const v = (j / (NV - 1)) * 2 - 1;
      for (let i = 0; i < NU; i++) {
        const u = (i / (NU - 1)) * 2 - 1;
        const env = Math.sqrt(Math.max(0, 1 - u * u));   // the taper
        if (env < 0.02) continue;

        const x =  u * 1.32;
        const z =  v * 0.52 * env;
        const y = (Math.sin(u * 3.4 + t * 2.1) * 0.5 +
                   Math.sin(v * 2.2 - t * 1.5) * 0.34 +
                   Math.sin((u + v) * 1.8 + t * 1.1) * 0.16) * 0.42 * env;

        // rotate about X, then perspective
        const yr = y * ct - z * st;
        const zr = y * st + z * ct;
        const p  = DIST / (DIST - zr);
        const sx = cx + x  * scale * p;
        const sy = cy - yr * scale * p * 1.02;

        const r = Math.max(0.6, 2.05 * p * dpr * (scale / 700));
        if (sx < -20 || sx > cv.width + 20) continue;

        // depth and envelope both fade the dot out, so the cloud has an
        // edge instead of stopping at a hard boundary
        const a = Math.min(1, (p - 0.72) * 2.1) * Math.min(1, env * 3.4);
        if (a <= 0.02) continue;

        // A tight pool under the cursor rather than the whole field.
        // The distance is measured in height units — x is scaled by the
        // aspect ratio first — so the pool is a circle on screen instead
        // of the ellipse a raw normalised distance would give on a wide
        // viewport. RADIUS is a fraction of the viewport height.
        let h = 0;
        if (heat > 0.001) {
          const dx = (sx / cv.width  - px) * aspect;
          const dy =  sy / cv.height - py;
          h = heat * Math.exp(-(dx * dx + dy * dy) / RAD2);
        }
        ctx.globalAlpha = a;
        ctx.drawImage(SPRITES[(h * STEPS + 0.5) | 0], sx - r, sy - r, r * 2, r * 2);
      }
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(frame);
  }

  size();
  addEventListener('resize', size, { passive: true });
  if (reduce) { last = performance.now(); frame(last); }   // one still frame
  else requestAnimationFrame(frame);
})();

/* ══════════════════════════════════════════════════════════════════════
   v198 · preloader, and the hero as space
   ----------------------------------------------------------------------
   The reference is a parallax starfield: it answers the pointer, drifts
   on its own, and has depth. None of that can be filmed — a clip cannot
   know where the cursor is — so generation was never the right tool
   here, and with colour-on-hover it is the same registration problem
   that killed the two-clip idea earlier.

   Graphite at rest. Colour arrives in a pool under the pointer, the same
   behaviour the previous hero had, so the site has one gesture rather
   than two.
   ═══════════════════════════════════════════════════════════════════ */
(function () {

  /* ---- 1 · the preloader --------------------------------------------
     Gated on real work — fonts parsed and the window loaded — not on a
     timer, with a floor so a warm cache does not make it flash and a
     ceiling so a stalled asset cannot trap anyone behind it. */
  const pre = document.getElementById('preload');
  // once per session: a first impression, not a toll booth on every return
  let seen = false;
  try { seen = sessionStorage.getItem('nk-seen') === '1'; } catch (e) {}
  if (pre && seen) { pre.remove(); dispatchEvent(new Event('nk:preloaded')); }
  else if (pre && pre.dataset.mode === 'reveal') {
    /* The reveal: black, light comes up, the creatures come at you and
       settle. Its last frame is the hero's first, so when it ends the
       overlay is simply taken away. Click, scroll, a key or a swipe skips
       it — six seconds is a lot to ask of someone who came to look at
       work. If the video ends before the creatures have decoded, it holds
       on its last frame, which is the same picture, until they have. */
    try { sessionStorage.setItem('nk-seen', '1'); } catch (e) {}
    const v = pre.querySelector('video');
    let eyesReady = !document.getElementById('s1eyes'), ended = false, gone = false;
    const lift = () => {
      if (gone) return; gone = true;
      pre.classList.add('is-gone');
      document.documentElement.classList.add('is-loaded');
      dispatchEvent(new Event('nk:preloaded'));
      ['click', 'wheel', 'keydown', 'touchstart'].forEach((ev) => removeEventListener(ev, skip, true));
      setTimeout(() => pre.remove(), 400);
    };
    const tryLift = () => { if (ended && eyesReady) lift(); };
    const skip = () => { if (v) v.pause(); ended = true; eyesReady = true; lift(); };
    addEventListener('nk:eyes-ready', () => { eyesReady = true; tryLift(); });
    if (v) {
      v.addEventListener('ended', () => { ended = true; tryLift(); });
      v.addEventListener('error', skip);
      const p = v.play(); if (p) p.catch(skip);        // autoplay refused: go straight in
    } else { ended = true; }
    ['click', 'wheel', 'keydown', 'touchstart'].forEach((ev) => addEventListener(ev, skip, { capture: true, passive: true }));
    setTimeout(skip, 12000);                            // never trap anyone
  }
  else if (pre) {
    try { sessionStorage.setItem('nk-seen', '1'); } catch (e) {}
    const num  = pre.querySelector('.preload-num i');
    const bar  = pre.querySelector('.preload-bar i');
    const cv   = document.getElementById('preloadcv');   // absent when the video is used
    const ctx  = cv && cv.getContext('2d');
    const FLOOR = 900, CEIL = 5000;
    const t0 = performance.now();
    let shown = 0, done = false;

    /* a few points of light finding each other — the same vocabulary the
       hero opens in, so the loader is the first beat of it rather than a
       spinner borrowed from somewhere else */
    let pw = 0, ph = 0, dots = [];
    function psize() {
      const d = Math.min(devicePixelRatio || 1, 2);
      pw = cv.width  = Math.round(innerWidth  * d);
      ph = cv.height = Math.round(innerHeight * d);
      dots = [];
      for (let i = 0; i < 90; i++) {
        dots.push({ x: Math.random(), y: Math.random(),
                    r: Math.random() * 1.6 + 0.4, p: Math.random() * 6.28 });
      }
    }
    if (ctx) { psize(); addEventListener('resize', psize, { passive: true }); }

    function real() {                      // 0..1 of the work actually done
      const fonts = document.fonts && document.fonts.status === 'loaded' ? 1 : 0;
      const load  = document.readyState === 'complete' ? 1 : 0;
      return (fonts + load) / 2;
    }

    function ptick(now) {
      const held = now - t0;
      // never runs backwards, never reaches 100 before the work does
      const target = Math.min(1, Math.max(real(), Math.min(0.92, held / CEIL)));
      shown += (target - shown) * 0.08;
      const pc = Math.round(shown * 100);
      if (num) num.textContent = pc;
      if (bar) bar.style.transform = 'scaleX(' + shown.toFixed(3) + ')';

      if (ctx) {
        ctx.fillStyle = '#ebebeb';
        ctx.fillRect(0, 0, pw, ph);
        const tt = now * 0.0006;
        for (const d of dots) {
          const a = (0.25 + 0.75 * (0.5 + 0.5 * Math.sin(tt + d.p))) * shown;
          ctx.globalAlpha = a;
          ctx.fillStyle = '#3f3f3f';
          ctx.beginPath();
          ctx.arc(d.x * pw, d.y * ph, d.r * (devicePixelRatio > 1 ? 2 : 1), 0, 6.283);
          ctx.fill();
        }
        ctx.globalAlpha = 1;
      }

      const ready = real() === 1 && held > FLOOR;
      if (!done && (ready || held > CEIL)) {
        done = true;
        if (num) num.textContent = '100';
        if (bar) bar.style.transform = 'scaleX(1)';
        setTimeout(() => {
          pre.classList.add('is-gone');
          document.documentElement.classList.add('is-loaded');
          dispatchEvent(new Event('nk:preloaded'));
          setTimeout(() => pre.remove(), 900);
        }, 260);
        return;
      }
      requestAnimationFrame(ptick);
    }
    requestAnimationFrame(ptick);
  }

  /* ---- 2 · the hero ------------------------------------------------- */
  const cv = document.getElementById('s1space');
  if (!cv) return;

  const ctx    = cv.getContext('2d', { alpha: false });
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const SKY  = '#ebebeb';
  const STAR = [ 63,  63,  63];
  const HOT  = [255,   0,  92];     // the site's one hot colour
  const WARM = [255, 150,  90];     // planets take a warmer light

  let W = 0, H = 0, dpr = 1;
  function size() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.width  = Math.round(cv.clientWidth  * dpr);
    H = cv.height = Math.round(cv.clientHeight * dpr);
  }

  /* three depth layers. Depth drives parallax, size and brightness
     together, which is what makes it read as distance rather than as
     three separate effects. */
  const stars = [];
  for (let i = 0; i < 420; i++) {
    const z = Math.random();
    stars.push({ x: Math.random(), y: Math.random(), z,
                 r: 0.35 + z * 1.5, tw: Math.random() * 6.283 });
  }

  /* Minimal planets: flat discs with a terminator, no texture. A drawn
     texture at this size reads as noise; the crescent is what says
     "planet" in one shape. */
  const planets = [
    { x: .18, y: .30, r: .085, z: .35, lit: -0.55, spin: .00006 },
    { x: .80, y: .22, r: .045, z: .62, lit:  0.70, spin: .00009 },
    { x: .66, y: .76, r: .130, z: .18, lit:  0.35, spin: .00004, ring: true },
    { x: .36, y: .82, r: .028, z: .85, lit: -0.30, spin: .00012 },
  ];

  let px = .5, py = .5, mx = .5, my = .5, heat = 0, want = 0;
  const host = cv.parentElement;
  host.addEventListener('pointermove', (e) => {
    const r = cv.getBoundingClientRect();
    px = (e.clientX - r.left) / (r.width  || 1);
    py = (e.clientY - r.top)  / (r.height || 1);
    want = 1;
  }, { passive: true });
  host.addEventListener('pointerleave', () => { want = 0; }, { passive: true });

  const RADIUS = 0.22, RAD2 = RADIUS * RADIUS;   // of viewport height
  let t = 0, last = performance.now();

  const mix = (a, b, k) => [a[0] + (b[0] - a[0]) * k,
                            a[1] + (b[1] - a[1]) * k,
                            a[2] + (b[2] - a[2]) * k];
  const rgb = (c, a) => 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + a + ')';

  function frame(now) {
    const dt = Math.min(64, now - last); last = now;
    t += dt;
    heat += (want - heat) * (1 - Math.pow(0.004, dt / 1000));
    mx += (px - mx) * (1 - Math.pow(0.02, dt / 1000));   // the parallax lags
    my += (py - my) * (1 - Math.pow(0.02, dt / 1000));

    ctx.fillStyle = SKY;
    ctx.fillRect(0, 0, W, H);

    const aspect = W / H;
    const ox = (mx - .5), oy = (my - .5);

    /* stars */
    for (const s of stars) {
      const par = 0.06 * (1 - s.z);
      const sx = (s.x + ox * par) * W;
      const sy = (s.y + oy * par) * H;
      if (sx < -8 || sx > W + 8) continue;
      const tw = 0.55 + 0.45 * Math.sin(t * 0.0012 + s.tw);
      let h = 0;
      if (heat > 0.001) {
        const dx = (sx / W - px) * aspect, dy = sy / H - py;
        h = heat * Math.exp(-(dx * dx + dy * dy) / RAD2);
      }
      const a = (0.22 + 0.78 * (1 - s.z)) * tw;
      ctx.fillStyle = rgb(mix(STAR, HOT, h * 0.9), a.toFixed(3));
      const r = s.r * dpr * (1 + h * 0.9);
      ctx.fillRect(sx - r, sy - r, r * 2, r * 2);
    }

    /* planets */
    for (const p of planets) {
      const par = 0.10 * (1 - p.z);
      const cx = (p.x + ox * par) * W;
      const cy = (p.y + oy * par) * H;
      const R  = p.r * H * (0.55 + 0.45 * (1 - p.z));
      const drift = Math.sin(t * p.spin) * 0.04 * H * (1 - p.z);

      let h = 0;
      if (heat > 0.001) {
        const dx = (cx / W - px) * aspect, dy = (cy + drift) / H - py;
        h = heat * Math.exp(-(dx * dx + dy * dy) / RAD2);
      }
      const y = cy + drift;
      const body = mix([66, 66, 70], mix(WARM, HOT, .45), h);

      if (p.ring) {                       // one ringed planet, drawn as an ellipse
        ctx.save();
        ctx.translate(cx, y); ctx.rotate(-0.42);
        ctx.strokeStyle = rgb(mix([96, 96, 102], WARM, h), (0.55 + h * 0.4).toFixed(3));
        ctx.lineWidth = Math.max(1, 1.6 * dpr);
        ctx.beginPath(); ctx.ellipse(0, 0, R * 1.72, R * 0.42, 0, 0, 6.283); ctx.stroke();
        ctx.restore();
      }

      ctx.fillStyle = rgb(body, 1);
      ctx.beginPath(); ctx.arc(cx, y, R, 0, 6.283); ctx.fill();

      // terminator: a second disc offset to carve the crescent
      ctx.fillStyle = SKY;
      ctx.globalAlpha = 0.86;
      ctx.beginPath(); ctx.arc(cx + p.lit * R * 0.92, y - R * 0.18, R * 0.99, 0, 6.283); ctx.fill();
      ctx.globalAlpha = 1;

      // rim light on the lit side
      ctx.strokeStyle = rgb(mix([128, 128, 134], mix(WARM, HOT, .4), h), (0.5 + h * 0.5).toFixed(3));
      ctx.lineWidth = Math.max(1, 1.2 * dpr);
      ctx.beginPath();
      const a0 = p.lit < 0 ? 0.6 : -2.55;
      ctx.arc(cx, y, R, a0, a0 + 2.0);
      ctx.stroke();
    }

    if (!reduce && !window.__heroVideoLive) requestAnimationFrame(frame);
  }

  size();
  addEventListener('resize', size, { passive: true });
  requestAnimationFrame(frame);
})();

/* ══════════════════════════════════════════════════════════════════════
   v199 · the Kling hero, graphite at rest, colour under the pointer
   ----------------------------------------------------------------------
   One clip, generated in colour. The <video> sits at the bottom with a
   CSS grayscale filter, which is what makes it graphite. Above it, a
   canvas copies the video's current frame in full colour and is masked
   to a soft pool around the cursor.

   Because both layers come from the same decoded frame, they cannot
   drift out of register — which is exactly what would have happened with
   a graphite clip and a red clip generated separately. And #EBEBEB stays
   #EBEBEB in both layers, since grey has no colour to remove.

   The colour copy is only drawn while the pointer is over the hero, so
   at rest the page pays for one video and nothing else.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  const vid = document.getElementById('s1vid');
  const hot = document.getElementById('s1hot');
  if (!vid || !hot) return;

  const g = hot.getContext('2d', { alpha: true });
  let dpr = 1, W = 0, H = 0;
  function size() {
    dpr = Math.min(devicePixelRatio || 1, 1.5);
    W = hot.width  = Math.round(hot.clientWidth  * dpr);
    H = hot.height = Math.round(hot.clientHeight * dpr);
  }

  // the drawn field was the stand-in; hand over once frames are flowing
  vid.addEventListener('playing', () => {
    window.__heroVideoLive = true;
    document.documentElement.classList.add('hero-video-live');
  }, { once: true });
  const kick = () => { if (vid.paused) vid.play().catch(() => {}); };
  kick();
  document.addEventListener('visibilitychange', () => { if (!document.hidden) kick(); });
  addEventListener('nk:preloaded', kick);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) kick(); else vid.pause();       // no decoding offscreen
    }), { threshold: 0.01 }).observe(vid);
  }

  let px = .5, py = .5, heat = 0, want = 0, last = performance.now(), live = false;
  const host = hot.parentElement;
  host.addEventListener('pointermove', (e) => {
    const r = hot.getBoundingClientRect();
    px = (e.clientX - r.left) / (r.width  || 1);
    py = (e.clientY - r.top)  / (r.height || 1);
    want = 1;
    if (!live) { live = true; requestAnimationFrame(tick); }
  }, { passive: true });
  host.addEventListener('pointerleave', () => { want = 0; }, { passive: true });

  function tick(now) {
    const dt = Math.min(64, now - last); last = now;
    heat += (want - heat) * (1 - Math.pow(0.004, dt / 1000));

    // the mask follows the pointer; its strength follows heat
    hot.style.setProperty('--mx', (px * 100).toFixed(2) + '%');
    hot.style.setProperty('--my', (py * 100).toFixed(2) + '%');
    hot.style.opacity = heat.toFixed(3);

    if (heat > 0.004 && vid.readyState >= 2) {
      // object-fit: cover AND object-position, replicated, so the copy
      // lands exactly on the original — on a phone the video is shifted
      // to keep the ringed planet in frame, and the colour has to follow
      const vw = vid.videoWidth, vh = vid.videoHeight;
      const s = Math.max(W / vw, H / vh);
      const w = vw * s, h = vh * s;
      const op = getComputedStyle(vid).objectPosition.split(' ').map(parseFloat);
      const ox = (W - w) * ((isNaN(op[0]) ? 50 : op[0]) / 100);
      const oy = (H - h) * ((isNaN(op[1]) ? 50 : op[1]) / 100);
      g.clearRect(0, 0, W, H);
      g.drawImage(vid, ox, oy, w, h);
    }

    if (heat > 0.002 || want) requestAnimationFrame(tick);
    else { live = false; g.clearRect(0, 0, W, H); }
  }

  size();
  addEventListener('resize', size, { passive: true });
})();
