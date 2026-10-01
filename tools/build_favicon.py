"""Export the site favicon set from one square source image.

    python3 tools/build_favicon.py path/to/eye.png [cx cy r]

Pass cx cy r (source pixels) when the eyeball sits on something other than a
plain ground and the auto-crop can't find it.

Crops to the eyeball (the source sits on #EBEBEB), masks it to a circle on a
transparent ground, and writes favicon.ico, the PNG sizes, apple-touch-icon
(on #EBEBEB, iOS does not do transparency) and an SVG wrapper around a
64px PNG. Needs Pillow + numpy.
"""
import base64, io, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
GROUND = (0xEB, 0xEB, 0xEB)


def eyeball(src, circle_px=None):
    im = Image.open(src).convert("RGB")
    if circle_px:
        cx, cy, r = circle_px
        return im.crop((cx - r, cy - r, cx + r, cy + r)).resize((1024, 1024), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    # anything clearly off the grey ground belongs to the eyeball
    diff = np.abs(a - np.array(GROUND)).sum(axis=2)
    ys, xs = np.where(diff > 40)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2
    r *= 0.985  # trim the soft rim so no grey fringe survives
    box = (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
    return im.crop(box).resize((1024, 1024), Image.LANCZOS)


def circle(im, size):
    big = size * 4
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big - 1, big - 1), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    out = im.resize((size, size), Image.LANCZOS)
    if size <= 48:  # tiny sizes go mushy; a touch of sharpening keeps the pupil
        out = out.filter(ImageFilter.UnsharpMask(radius=1, percent=80, threshold=2))
    out = out.convert("RGBA")
    out.putalpha(mask)
    return out


def main(src, circle_px=None):
    eye = eyeball(src, circle_px)
    sizes = {16: "favicon-16.png", 32: "favicon-32.png", 48: "favicon-48.png",
             192: "favicon-192.png", 512: "favicon-512.png"}
    icons = {s: circle(eye, s) for s in sizes}
    for s, name in sizes.items():
        im = icons[s]
        if s >= 192:  # 256-colour palette keeps the manifest icons light
            im = im.quantize(256, method=Image.Quantize.FASTOCTREE)
        im.save(os.path.join(A, name), optimize=True)

    icons[48].save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

    touch = Image.new("RGB", (180, 180), GROUND)
    c = circle(eye, 150)
    touch.paste(c, (15, 15), c)
    touch.save(os.path.join(A, "apple-touch-icon.png"), optimize=True)

    buf = io.BytesIO()
    circle(eye, 64).save(buf, "PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           'viewBox="0 0 64 64" role="img" aria-label="Khomeriki">'
           f'<image width="64" height="64" href="data:image/png;base64,{b64}"/></svg>\n')
    with open(os.path.join(A, "favicon.svg"), "w") as f:
        f.write(svg)
    print("favicon set written")


if __name__ == "__main__":
    main(sys.argv[1], tuple(map(int, sys.argv[2:5])) if len(sys.argv) >= 5 else None)
