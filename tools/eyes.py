"""
Split a single-eyed creature into the layers a live gaze needs.

  body   the creature cut out of its background, with the iris removed
         and the white of the eye rebuilt underneath it
  iris   the iris + pupil as its own disc, catchlights taken out
  mask   the eye opening — where the iris is allowed to show; the lids
         are everything outside it, so a moving iris slides under them
  shade  the lid shadow inside the opening, multiplied over the iris so
         it sits *in* the eye instead of on top of it
  hl     the corneal catchlights, which stay put while the iris moves:
         a reflection belongs to the light, not to the pupil

Geometry goes into a small JSON record so the page can place everything.
"""
import sys, json, math, numpy as np, cv2

def load(p, cap=1400):
    im = cv2.imread(p, cv2.IMREAD_COLOR)
    if im is None: raise SystemExit(f"cannot read {p}")
    # nothing on the page is drawn larger than this, and the radial and
    # region steps are quadratic in size — 2048px sources took minutes
    h, w = im.shape[:2]
    if max(h, w) > cap:
        s = cap / max(h, w)
        im = cv2.resize(im, (round(w*s), round(h*s)), interpolation=cv2.INTER_AREA)
    return im

def cutout(bgr, bg_hint=None):
    """Alpha from colour distance to the plate, sampled on the border.
    The largest component survives, holes are filled, and edge pixels
    are un-mixed from the plate colour so there is no grey fringe."""
    h, w = bgr.shape[:2]
    f = bgr.astype(np.float32)
    border = np.concatenate([f[:6].reshape(-1,3), f[-6:].reshape(-1,3),
                             f[:, :6].reshape(-1,3), f[:, -6:].reshape(-1,3)])
    bg = np.median(border, 0) if bg_hint is None else np.array(bg_hint, np.float32)
    # the plate is rarely perfectly flat — model it as a smooth surface
    # over the border so a slight gradient is not read as foreground
    ys, xs = np.mgrid[0:h, 0:w]
    X = xs / (w-1) * 2 - 1; Y = ys / (h-1) * 2 - 1
    B = np.stack([np.ones_like(X), X, Y, X*X, X*Y, Y*Y], -1).reshape(-1, 6)
    edge = np.zeros((h, w), bool); edge[:6] = edge[-6:] = True; edge[:, :6] = edge[:, -6:] = True
    plate = np.zeros_like(f)
    for c in range(3):
        coef = np.linalg.lstsq(B[edge.ravel()], f[..., c][edge], rcond=None)[0]
        plate[..., c] = (B @ coef).reshape(h, w)
    d = np.abs(f - plate).max(2)
    a = np.clip((d - 6) / 22.0, 0, 1)
    solid = (a > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(solid, 8)
    keep = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    body = (lab == keep).astype(np.uint8)
    # fill holes (the bright sclera can read as "background" on a light plate)
    ff = body.copy(); m = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(ff, m, (0, 0), 1)
    enclosed = (ff == 0).astype(np.uint8)
    # An enclosed region is either part of the creature that happens to
    # match the plate (a bright sclera) or real background seen through a
    # loop (the gap inside a ring, between an arm and the body). The plate
    # is flat and untextured; skin and sclera are neither.
    grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    nh, hl_ = cv2.connectedComponents(enclosed, 8)
    lab1 = hl_.ravel()
    cnt = np.bincount(lab1, minlength=nh).astype(np.float64)
    md = np.bincount(lab1, weights=d.ravel(), minlength=nh) / np.maximum(cnt, 1)
    g1 = grey.ravel().astype(np.float64)
    mg = np.bincount(lab1, weights=g1, minlength=nh) / np.maximum(cnt, 1)
    vg = np.bincount(lab1, weights=g1*g1, minlength=nh) / np.maximum(cnt, 1) - mg*mg
    background_gap = (md < 14) & (np.sqrt(np.maximum(vg, 0)) < 7)
    background_gap[0] = True
    holes = ~background_gap[hl_]
    body[holes] = 1
    grow = cv2.dilate(body, np.ones((5,5), np.uint8))
    a = np.where(body == 1, np.maximum(a, (holes).astype(np.float32)), a) * grow
    a[holes] = 1.0
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    a = np.clip(a, 0, 1)
    # un-mix the plate from semi-transparent edge pixels
    af = np.maximum(a, 1e-3)[..., None]
    fg = np.clip((f - (1 - af) * plate) / af, 0, 255)
    fg = np.where(a[..., None] > 0.98, f, fg)
    return fg.astype(np.uint8), a, plate

def find_iris(bgr, alpha):
    """Pupil first: in these renders it is the darkest, roundest blob on
    the creature — hair is dark too, but it is neither compact nor round.
    The iris is then measured outward from the pupil centre: the limbus is
    where brightness climbs fastest from iris to sclera."""
    g = cv2.GaussianBlur(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), (0, 0), 1.5)
    H, W = g.shape
    ys_, xs_ = np.where(alpha > 0.9)
    S = max(xs_.max() - xs_.min(), ys_.max() - ys_.min())
    best, bs = None, -1
    for thr in (28, 38, 50, 64):
        dark = ((g < thr) & (alpha > 0.9)).astype(np.uint8)
        n, lab, st, cen = cv2.connectedComponentsWithStats(dark, 8)
        for i in range(1, n):
            A = st[i, cv2.CC_STAT_AREA]
            if A < 150: continue
            # dark iris fibres can join the pupil; an opening sized to the
            # blob strips them and leaves the round core
            x0_, y0_, w_, h_ = st[i, :4]
            blob = (lab[y0_:y0_+h_, x0_:x0_+w_] == i).astype(np.uint8)
            kk = max(3, int(0.28 * min(w_, h_)) | 1)
            core = cv2.morphologyEx(blob, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kk, kk)))
            m2, l2, s2, c2 = cv2.connectedComponentsWithStats(core, 8)
            if m2 < 2: continue
            j = 1 + int(np.argmax(s2[1:, cv2.CC_STAT_AREA]))
            A2 = s2[j, cv2.CC_STAT_AREA]; w2, h2 = s2[j, 2], s2[j, 3]
            fill = A2 / float(w2 * h2); aspect = min(w2, h2) / max(w2, h2)
            if aspect < 0.8 or fill < 0.66 or A2 < 150: continue
            rp_ = np.sqrt(A2 / np.pi)
            # a pupil is a known fraction of the creature: this rejects the
            # small dark gaps between fingers and toes
            if not (0.018 * S <= rp_ <= 0.12 * S): continue
            score = aspect * (1 - abs(fill - 0.785)) * np.sqrt(rp_)
            if score > bs:
                bs = score
                best = (float(x0_ + c2[j][0]), float(y0_ + c2[j][1]), float(np.sqrt(A2 / np.pi)))
    if not best: raise SystemExit("no pupil found")
    cx, cy, rp = best
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - cx, yy - cy)
    lo, hi = rp * 1.5, rp * 3.8
    sel = (alpha > 0.9) & (d >= lo) & (d < hi)
    ri = (d[sel] - lo).astype(np.int32)
    cnt = np.bincount(ri); sm = np.bincount(ri, weights=g[sel].astype(np.float64))
    prof = cv2.GaussianBlur((sm / np.maximum(cnt, 1)).reshape(1, -1).astype(np.float32), (0, 0), 2).ravel()
    gr = np.gradient(prof)
    # the limbus is the steepest rise: these irises have a dark limbal ring
    # right at the edge, so the halfway point overshoots into the sclera
    k = int(np.argmax(gr))
    r = float(lo + k)
    return cx, cy, r

def eye_opening(bgr, alpha, cx, cy, r):
    """Flood the sclera from bright points just outside the limbus; it
    stops at the lash line. Then take the convex hull — an eye opening is
    a convex lens between two lid arcs, and the hull also cuts away any
    part of the iris a lid is covering."""
    H, W = alpha.shape
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - cx, yy - cy)
    L = cv2.cvtColor(cv2.GaussianBlur(bgr, (0, 0), max(1.2, r*0.02)), cv2.COLOR_BGR2LAB)[..., 0]
    irisL = np.median(L[(d < r*0.85) & (alpha > 0.9)])
    region = np.zeros((H, W), np.uint8)
    allowed = ((d < r*3.2) & (alpha > 0.9)).astype(np.uint8)
    for ang in np.linspace(0, 2*np.pi, 36, endpoint=False):
        for rr in (1.12, 1.25):
            x = int(cx + r*rr*np.cos(ang)); y = int(cy + r*rr*np.sin(ang))
            if not (0 <= x < W and 0 <= y < H) or not allowed[y, x] or region[y, x]: continue
            if L[y, x] < irisL + 35: continue           # a lid, not sclera
            m = np.zeros((H+2, W+2), np.uint8)
            m[1:-1, 1:-1] = 1 - allowed                  # the fill may not leave the allowed zone
            tmp = L.copy()
            cv2.floodFill(tmp, m, (x, y), 255, loDiff=5, upDiff=5,
                          flags=4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8))
            region |= (m[1:-1, 1:-1] == 255).astype(np.uint8)
    region = cv2.morphologyEx(region, cv2.MORPH_OPEN,
             cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(r*0.08)|1,)*2))
    n, lab_ = cv2.connectedComponents(region, 8)
    ring = ((d > r*1.0) & (d < r*1.35)).ravel()
    touch = np.bincount(lab_.ravel()[ring], minlength=n)
    ok = touch > 30; ok[0] = False
    keep = ok[lab_].astype(np.uint8)
    pts = np.column_stack(np.where(keep > 0))[:, ::-1].astype(np.int32)
    if len(pts) < 10:                                    # fallback: a lens around the iris
        pts = np.array([[cx + r*1.9*np.cos(a), cy + r*1.1*np.sin(a)] for a in np.linspace(0, 6.28, 40)], np.int32)
    hull = cv2.convexHull(pts)
    m = np.zeros((H, W), np.uint8)
    cv2.fillConvexPoly(m, hull, 1)
    m &= (alpha > 0.9).astype(np.uint8)
    mf = cv2.GaussianBlur(m.astype(np.float32), (0, 0), max(1.5, r*0.025))
    return np.clip(mf, 0, 1)


def lens_mask(H, W, lens, soft=2.5):
    (lx, ly), (rx, ry), (ax, top), (bx, bot) = lens
    def para(p0, p1, p2):
        X = np.array([p0[0], p1[0], p2[0]], np.float64); Y = np.array([p0[1], p1[1], p2[1]], np.float64)
        return np.polyfit(X, Y, 2)
    up = para((lx, ly), (ax, top), (rx, ry))
    lo = para((lx, ly), (bx, bot), (rx, ry))
    xs = np.arange(W, dtype=np.float64)
    yu = np.polyval(up, xs); yl = np.polyval(lo, xs)
    yy = np.arange(H, dtype=np.float64)[:, None]
    inside = (yy >= yu[None, :]) & (yy <= yl[None, :]) & (xs[None, :] >= lx) & (xs[None, :] <= rx)
    m = cv2.GaussianBlur(inside.astype(np.float32), (0, 0), soft)
    return np.clip(m, 0, 1)

def pushpull(img, hole):
    """Fill `hole` with a smooth membrane of the surrounding colour."""
    w = (~hole).astype(np.float32)
    c = img.astype(np.float32) * w[..., None]
    pyr = [(c, w)]
    while min(pyr[-1][1].shape) > 8:
        c2 = cv2.pyrDown(pyr[-1][0]); w2 = cv2.pyrDown(pyr[-1][1])
        pyr.append((c2, w2))
    fc, fw = pyr[-1]
    col = fc / np.maximum(fw, 1e-4)[..., None]
    for c_, w_ in reversed(pyr[:-1]):
        up = cv2.resize(col, (w_.shape[1], w_.shape[0]), interpolation=cv2.INTER_LINEAR)
        a = np.clip(w_ * 4, 0, 1)[..., None]
        col = (c_ / np.maximum(w_, 1e-4)[..., None]) * a + up * (1 - a)
    out = img.astype(np.float32).copy()
    out[hole] = col[hole]
    return np.clip(out, 0, 255).astype(np.uint8)


def split(src, out_prefix, target_h=1024, lens=None, iris=None):
    im = load(src)
    fg, a, plate = cutout(im)
    # a hand-measured circle wins over detection when it is given
    cx, cy, r = iris if iris else find_iris(fg, a)
    mask = lens_mask(*a.shape, lens) if lens else eye_opening(fg, a, cx, cy, r)
    # a bright highlight on the sclera can look like plate and get cleared;
    # inside the opening it is always the creature
    a = np.maximum(a, cv2.dilate(mask, np.ones((5, 5), np.uint8)))
    H, W = a.shape
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - cx, yy - cy)

    # catchlights: near-white, inside the cornea
    lum = fg.astype(np.float32).mean(2)
    irmed = np.median(lum[(d < r*0.9) & (a > 0.9)])
    base = irmed + 30
    f32 = fg.astype(np.float32)
    chroma = f32.max(2) - f32.min(2)
    bright = ((lum > max(172, irmed + 62)) & (chroma < 42) & (d < r*1.06)).astype(np.uint8)
    bright = cv2.morphologyEx(bright, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    nc, lc, sc, _ = cv2.connectedComponentsWithStats(bright, 8)
    inside = np.bincount(lc.ravel()[(d < r*0.97).ravel()], minlength=nc)
    keep = (inside > 12) & (sc[:, cv2.CC_STAT_AREA] > max(30, 0.003 * np.pi * r * r)); keep[0] = False
    hl = keep[lc].astype(np.uint8)
    hl = cv2.dilate(hl, np.ones((5, 5), np.uint8))
    hl_a = cv2.GaussianBlur((hl & (d < r*0.95)).astype(np.float32), (0, 0), 1.2) * ((lum - base) / max(1, 255 - base)).clip(0, 1)
    src = np.where(a[..., None] > 0.98, im, fg).astype(np.uint8)
    iris_src = src.copy()
    # complete the iris where a lid covers it: an iris is close to radially
    # symmetric, so an occluded pixel borrows the visible pixel opposite it.
    # Without this, the lid skin baked into the disc would travel with the
    # iris the moment it moved.
    hl_grown = cv2.dilate(hl, np.ones((5, 5), np.uint8)) > 0
    vis = (mask > 0.6) & (d < r*1.02) & ~hl_grown
    occ = (~vis) & (d < r*1.08)
    if occ.any():
        R = int(np.ceil(r * 1.08)); NA = 720
        center = (float(cx), float(cy))
        pol = cv2.warpPolar(iris_src, (R, NA), center, R, cv2.WARP_POLAR_LINEAR)
        pv = cv2.warpPolar((~occ).astype(np.uint8) * 255, (R, NA), center, R, cv2.WARP_POLAR_LINEAR) > 127
        # per radius row, fill hidden angles from the nearest visible angle,
        # walking around the circle in both directions
        out = pol.copy()
        idx = np.arange(NA)
        for rr in range(R):
            v = pv[:, rr]
            if v.all() or not v.any(): continue
            vis_i = idx[v]
            # distance to nearest visible angle, circularly
            dd = np.abs(idx[:, None] - vis_i[None, :]); dd = np.minimum(dd, NA - dd)
            near = vis_i[np.argmin(dd, 1)]
            # mirror across the gap edge instead of smearing one column
            off = ((idx - near + NA // 2) % NA) - NA // 2
            src_i = (near - off) % NA
            src_i = np.where(v[src_i], src_i, near)
            out[~v, rr] = pol[src_i[~v], rr]
        back = cv2.warpPolar(out, (iris_src.shape[1], iris_src.shape[0]), center, R,
                             cv2.WARP_POLAR_LINEAR | cv2.WARP_INVERSE_MAP)
        iris_src = np.where(occ[..., None], back, iris_src).astype(np.uint8)

    # iris sprite: soft disc
    ia = np.clip((r * 0.965 + 1.5 - d) / 3.0, 0, 1)
    # body: rebuild the sclera under the iris. A plain fill reads as a milky
    # disc, so the fill is two layers: a smooth base colour (push-pull from
    # sclera well clear of the dark limbal ring) plus real sclera *detail*
    # (veins, wet texture) borrowed from nearby sclera — reflected outward
    # across the limbus first, else shifted sideways — so the uncovered
    # white carries the same veins as the white around it.
    body = src.copy()
    H_, W_ = d.shape
    R1 = r * 1.24
    hole = (d < R1) & (mask > 0.02)
    fs = src.astype(np.float32)
    gl = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    okm = (mask > 0.92) & (d > r * 1.28)                     # clean sclera only
    okm &= cv2.erode((gl < 236).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0   # no specular streaks
    # base colour only from clean sclera, never lid skin or iris bleed
    # base colour: sclera left and right of the iris, interpolated across
    # each row. Above and below the iris there is little sclera and a lot of
    # lid, so a radial fill turns beige; the eye's white runs sideways.
    known = (mask > 0.9) & (d > r * 1.26)
    ref = np.percentile(gl[known], 90) if known.any() else 220
    known &= gl > ref * 0.72
    known = cv2.erode(known.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    sm = cv2.GaussianBlur(fs, (0, 0), 4)
    base = sm.copy()
    ys_ = np.where(hole.any(1))[0]
    xs_all = np.arange(W_)
    for y in ys_:
        row = hole[y]; kn = np.where(known[y])[0]
        hx = np.where(row)[0]
        if len(kn) == 0:
            continue
        L = kn[kn < cx]; Rr = kn[kn > cx]
        if len(L) and len(Rr):
            xl = L.max(); xr = Rr.min()
            # average a short run on each side, not a single pixel
            cl = sm[y, max(0, xl - 12):xl + 1].mean(0); cr = sm[y, xr:xr + 13].mean(0)
            t = np.clip((hx - xl) / max(1, xr - xl), 0, 1)[:, None]
            base[y, hx] = cl * (1 - t) + cr * t
        else:
            side = L if len(L) else Rr
            xs0 = side.max() if len(L) else side.min()
            base[y, hx] = sm[y, max(0, xs0 - 6):xs0 + 7].mean(0)
    # rows with no sclera at all (under the lid apex) borrow from neighbours
    base = pushpull(base.clip(0, 255).astype(np.uint8), hole & ~known.any(1)[:, None]).astype(np.float32)
    base = cv2.GaussianBlur(base, (0, 0), r * 0.10)
    detail = fs - cv2.GaussianBlur(fs, (0, 0), 5)
    yy2, xx2 = np.mgrid[0:H_, 0:W_].astype(np.float32)
    ang = np.arctan2(yy2 - cy, xx2 - cx)
    src_x = np.full((H_, W_), -1, np.float32); src_y = np.full((H_, W_), -1, np.float32)
    got = np.zeros((H_, W_), bool)
    cands = []
    refl = []
    for k in (0.9, 0.5, 1.4):                              # outward reflections
        rho2 = R1 * 1.08 + (R1 - np.minimum(d, R1)) * k
        refl.append((cx + rho2 * np.cos(ang), cy + rho2 * np.sin(ang), d > R1 * 0.55))
    cands += refl
    for sh, sv in ((2.3, 0), (-2.3, 0), (1.9, .35), (-1.9, .35), (1.9, -.35), (-1.9, -.35),
                   (2.8, 0), (-2.8, 0), (1.5, 0), (-1.5, 0)):   # sideways copies
        cands.append((xx2 + sh * r, yy2 + sv * r, True))
    # reflections near the rim (veins run on), copies in the middle (no
    # pinch where every radius meets), reflections anywhere as a last resort
    cands += [(a_, b_, True) for a_, b_, _ in refl]
    for sx, sy, zone in cands:
        ix = np.clip(np.round(sx).astype(int), 0, W_ - 1); iy = np.clip(np.round(sy).astype(int), 0, H_ - 1)
        inb = (sx >= 0) & (sx < W_) & (sy >= 0) & (sy < H_)
        v = hole & ~got & inb & okm[iy, ix] & zone
        src_x[v] = sx[v]; src_y[v] = sy[v]; got |= v
    samp = cv2.remap(detail, src_x, src_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    samp[~got] = 0
    # detail fades out toward the centre of the hole only where nothing was found
    filled = np.clip(base + samp * 0.95, 0, 255)
    # full rebuild inside the limbal halo, then a long soft ramp out to the
    # real sclera, so there is no rim where the fill meets the photo
    ramp = np.clip((R1 - d) / (R1 - r * 1.04), 0, 1); ramp = ramp * ramp * (3 - 2 * ramp)
    hm = cv2.GaussianBlur((ramp * hole).astype(np.float32), (0, 0), 1.5)[..., None]
    body = (filled * hm + fs * (1 - hm)).astype(np.uint8)
    body[~(mask > 0.02)] = src[~(mask > 0.02)]

    # lid shadow inside the opening, as a multiply factor for the iris
    sl = cv2.cvtColor(body, cv2.COLOR_BGR2GRAY).astype(np.float32)
    ref = np.percentile(sl[mask > 0.8], 92)
    shade = np.clip(cv2.GaussianBlur(sl, (0, 0), r*0.10) / max(ref, 1), 0.25, 1.0)

    # crop everything to the creature, scale to target height
    ys, xs = np.where(a > 0.02)
    x0, x1, y0, y1 = xs.min(), xs.max()+1, ys.min(), ys.max()+1
    pad = int(0.02 * max(x1-x0, y1-y0))
    x0, y0 = max(0, x0-pad), max(0, y0-pad); x1, y1 = min(W, x1+pad), min(H, y1+pad)
    s = target_h / (y1 - y0)
    def crop(img): return cv2.resize(img[y0:y1, x0:x1], (round((x1-x0)*s), target_h), interpolation=cv2.INTER_AREA)
    B = crop(np.dstack([body, (a*255).astype(np.uint8)]))
    cv2.imwrite(out_prefix + "-body.png", B)

    # eye-local layers live in a square around the eye opening
    ym, xm = np.where(mask > 0.02)
    ex0, ex1, ey0, ey1 = xm.min(), xm.max()+1, ym.min(), ym.max()+1
    def ecrop(img): 
        c = img[ey0:ey1, ex0:ex1]
        return cv2.resize(c, (round((ex1-ex0)*s), round((ey1-ey0)*s)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(out_prefix + "-mask.png", ecrop((mask*255).astype(np.uint8)))
    cv2.imwrite(out_prefix + "-shade.png", ecrop((shade*255).astype(np.uint8)))
    hlimg = np.dstack([np.full_like(lum, 255).astype(np.uint8)]*3 + [(hl_a*255).clip(0,255).astype(np.uint8)])
    cv2.imwrite(out_prefix + "-hl.png", ecrop(hlimg))
    # iris sprite: square around the iris
    ir = int(math.ceil(r*1.1))
    ix0, iy0 = int(cx) - ir, int(cy) - ir
    isq = np.dstack([iris_src, (ia*255).astype(np.uint8)])[max(0,iy0):iy0+2*ir, max(0,ix0):ix0+2*ir]
    isz = round(2*ir*s)
    cv2.imwrite(out_prefix + "-iris.png", cv2.resize(isq, (isz, isz), interpolation=cv2.INTER_AREA))

    rec = dict(
        w=B.shape[1], h=B.shape[0],
        eye=dict(x=round((ex0-x0)*s, 2), y=round((ey0-y0)*s, 2),
                 w=round((ex1-ex0)*s, 2), h=round((ey1-ey0)*s, 2)),
        iris=dict(cx=round((cx-x0)*s, 2), cy=round((cy-y0)*s, 2), r=round(r*s, 2), size=isz),
    )
    # how far the iris can travel before it is fully under a lid: measured
    # along the horizontal and vertical of the opening, not assumed
    open_l = cx - ex0; open_r = ex1 - cx; open_t = cy - ey0; open_b = ey1 - cy
    rec["travel"] = dict(
        x=round(min(r*0.95, max(r*0.40, min(open_l, open_r) - r*0.55)) * s, 2),
        y=round(min(r*0.6, max(r*0.32, min(open_t, open_b) - r*0.55)) * s, 2))
    return rec

if __name__ == "__main__":
    spec = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    if isinstance(spec, list): spec = {"lens": spec}
    rec = split(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1024,
                spec.get("lens"), spec.get("iris"))
    print(json.dumps(rec))
