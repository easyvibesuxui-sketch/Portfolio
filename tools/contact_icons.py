"""Contact-card icons from one Kling render of five eyeball creatures.

    python3 tools/contact_icons.py tools/contact-icons-source.png assets/contact

The render is five creatures in a row on a light studio ground (one job, so
they share a style). Every foreground pixel goes to the nearest creature,
which also hands each prop (phone, briefcase, ball, paper) to its owner.
The creature is cut out on transparency, so the icon sits on any card
colour; the page adds its own shadow.
"""
import os, sys
import numpy as np, cv2
from PIL import Image

NAMES = ["email", "phone", "linkedin", "dribbble", "cv"]
# where each body sits in this render, as fractions of width / height
CENTRES = [(.113, .55), (.333, .55), (.512, .55), (.702, .55), (.875, .55)]

# The envelope and the CV sheet are white on a ground of the same
# brightness, so no threshold or GrabCut finds them. Their corners are
# read off this render (pixels, full size) and filled as polygons.
PROPS = {
    "email": [(186, 685), (524, 685), (524, 873), (186, 873)],
    "cv":    [(2765, 659), (2947, 687), (2913, 929), (2727, 905)],
}

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
im = np.array(Image.open(src).convert("RGB")).astype(np.float32)
h, w, _ = im.shape
L = im.mean(axis=2)

# the ground: lit from above, so it changes down the frame and a little
# across it. rows from the left margin, columns from the top band.
row = np.median(L[:, : int(w * .03)], axis=1)
col = np.median(L[: int(h * .12)], axis=0)
gL = cv2.GaussianBlur((row[:, None] + col[None] - col.mean()).astype(np.float32), (0, 0), 6)
sat = im.max(axis=2) - im.min(axis=2)

# foreground: anything coloured, clearly darker, or brighter than the
# ground (the white envelope and paper). Soft floor shadow is only a
# little darker and colourless, so it stays out.
fgm = ((sat > 14) | (L < gL - 40) | (L > gL + 7)).astype(np.uint8)
fgm = cv2.morphologyEx(fgm, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

yy, xx = np.mgrid[0:h, 0:w]
d = [np.hypot(xx - cx * w, yy - cy * h) for cx, cy in CENTRES]
cell = np.argmin(np.stack(d), axis=0)

for k, name in enumerate(NAMES):
    m = fgm * (cell == k).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    m = np.isin(lab, [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 2500]).astype(np.uint8)
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # GrabCut settles the edges the thresholds cannot: white props against a
    # pale ground, hair, and the lit floor. Seeded from the threshold mask,
    # with the neighbours' cells and the frame border fixed as background.
    pad = 40
    X0, Y0, X1, Y1 = max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + pad, w), min(y1 + pad, h)
    roi = im[Y0:Y1, X0:X1].astype(np.uint8)[..., ::-1].copy()
    gc = np.full(roi.shape[:2], cv2.GC_PR_BGD, np.uint8)
    gc[m[Y0:Y1, X0:X1] == 1] = cv2.GC_PR_FGD
    core = cv2.erode(((sat > 30) & (cell == k)).astype(np.uint8)[Y0:Y1, X0:X1], np.ones((9, 9), np.uint8))
    gc[core == 1] = cv2.GC_FGD
    gc[(cell != k)[Y0:Y1, X0:X1]] = cv2.GC_BGD
    gc[:6] = gc[-6:] = cv2.GC_BGD; gc[:, :6] = gc[:, -6:] = cv2.GC_BGD
    bg_m, fg_m = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(roi, gc, None, bg_m, fg_m, 6, cv2.GC_INIT_WITH_MASK)
    sub = np.isin(gc, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(sub, 8)
    sub = np.isin(lab, [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 2500]).astype(np.uint8)
    ff = np.pad(sub, 1).copy(); cv2.floodFill(ff, None, (0, 0), 1)
    sub = sub | (1 - ff[1:-1, 1:-1])
    m = np.zeros((h, w), np.uint8); m[Y0:Y1, X0:X1] = sub
    if name in PROPS:
        cv2.fillPoly(m, [np.array(PROPS[name], np.int32)], 1)
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    a = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)
    alpha = a          # no baked floor shadow: the page draws one in CSS
    rgb = np.where(a[..., None] > .01, im, 0)
    side = int(max(x1 - x0, y1 - y0) * 1.06)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + int(side * .015)
    bx0, by0 = cx - side // 2, cy - side // 2
    rgba = np.dstack([rgb, alpha * 255])
    rgba = np.pad(rgba, ((side, side), (side, side), (0, 0)))[by0 + side: by0 + 2 * side, bx0 + side: bx0 + 2 * side]
    img = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), "RGBA").resize((256, 256), Image.LANCZOS)
    img.save(os.path.join(out, f"{name}.webp"), quality=88, method=6)
    print(name, (x1 - x0, y1 - y0), os.path.getsize(os.path.join(out, f"{name}.webp")))
