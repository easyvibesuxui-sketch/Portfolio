"""Card / cover composites from a project's own screens.
Each layout puts real screens on the site's light ground with soft shadows,
sized so a 16:9 cover, a 4:3 card and a 16:11 card all keep the whole group."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

W, H = 1600, 1000

def ground(c0=(236,237,239), c1=(214,222,228)):
    yy, xx = np.mgrid[0:H, 0:W]; t = (xx / W * .5 + yy / H * .5)[..., None]
    g = np.array(c0) * (1 - t) + np.array(c1) * t
    return Image.fromarray(g.astype(np.uint8)).convert('RGBA')

def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m); return out

def fit_w(im, w): return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)

def place(cv, im, x, y, blur=32, off=16, alpha=100):
    m = Image.new('L', cv.size, 0); m.paste(im.split()[3], (int(x), int(y + off)))
    s = Image.new('RGBA', cv.size, (20, 24, 32, 0))
    s.putalpha(m.point(lambda v: v * alpha // 255).filter(ImageFilter.GaussianBlur(blur)))
    cv.alpha_composite(s); cv.alpha_composite(im, (int(x), int(y)))

def pair(big, small, bw=960, sw=520, drop=80, r=20):
    """one large window, a smaller one overlapping its lower right"""
    cv = ground()
    a = rounded(fit_w(big, bw), r); b = rounded(fit_w(small, sw), r - 4)
    gw = bw + sw - (bw + sw - 1180) if bw + sw > 1180 else bw + sw
    gw = 1180; gx = (W - gw) // 2
    gh = max(a.height, a.height - b.height + drop + b.height); gy = (H - gh) // 2
    place(cv, a, gx, gy)
    place(cv, b, gx + gw - b.width, gy + a.height - b.height + drop, blur=26, off=12, alpha=115)
    return cv

def cascade(ims, w=620, step=(250, 60), r=18):
    """three or so screens stepping across, each over the last"""
    cv = ground(); n = len(ims)
    tiles = [rounded(fit_w(i, w), r) for i in ims]
    gw = w + step[0] * (n - 1); gh = max(t.height for t in tiles) + step[1] * (n - 1)
    gx = (W - gw) // 2; gy = (H - gh) // 2
    for k, t in enumerate(tiles):
        place(cv, t, gx + step[0] * k, gy + step[1] * k)
    return cv

def plate(logo, bg):
    """a brand mark alone, on its own colour, full-bleed"""
    cv = Image.new('RGBA', (W, H), bg + (255,))
    lw = min(logo.width, 900)
    l = fit_w(logo.convert('RGBA'), lw)
    cv.alpha_composite(l, ((W - l.width) // 2, (H - l.height) // 2))
    return cv
