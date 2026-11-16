"""Lab card images: a site's real screenshot set into a laptop mockup.

    node tools/lab_mockup/shoot.mjs LIST.txt SHOTS_DIR   # LIST: "slug url" per line, 1440x900 @1.5x
    python3 tools/lab_mockup/compose.py tools/lab_mockup/laptop.png SHOTS_DIR assets/lab

laptop.png is a Kling render with a chroma-green screen (#EBEBEB ground); the
screenshot is pasted into the green area only, so the notch and bezel stay
on top and the site's own text stays sharp. Output: 1200x600 JPG per slug.
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter
mock_p, shots_dir, out_dir = sys.argv[1:4]
os.makedirs(out_dir, exist_ok=True)
M = Image.open(mock_p).convert('RGB'); a = np.asarray(M).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
green = (g > 140) & (g - r > 60) & (g - b > 60)
ys, xs = np.where(green)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
W, H = x1 - x0 + 1, y1 - y0 + 1
print('screen', x0, y0, W, H, round(W / H, 3))
# mask: green pixels, grown 1px to eat the anti-aliased fringe, softened
mask = Image.fromarray((green * 255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
# card framing: 2:1, laptop ~ 74% of card width, laptop centred
lap_l, lap_r = x0 - int(W * 0.09), x1 + int(W * 0.09)
cw = int((lap_r - lap_l) / 0.60); ch = cw // 2
cx = (x0 + x1) // 2; cy = (y0 + (y1 + int(H * 0.07))) // 2
box = (cx - cw // 2, cy - ch // 2, cx + cw // 2, cy - ch // 2 + ch)
print('card box', box)
for f in sorted(os.listdir(shots_dir)):
    if not f.endswith('.png'): continue
    s = Image.open(os.path.join(shots_dir, f)).convert('RGB')
    # cover the screen from the top of the page
    sc = max(W / s.width, H / s.height)
    s = s.resize((round(s.width * sc), round(s.height * sc)), Image.LANCZOS)
    left = (s.width - W) // 2
    s = s.crop((left, 0, left + W, H))
    canvas = M.copy()
    full = Image.new('RGB', M.size); full.paste(s, (x0, y0))
    canvas = Image.composite(full, canvas, mask)
    card = canvas.crop(box).resize((1200, 600), Image.LANCZOS)
    card.save(os.path.join(out_dir, f.replace('.png', '.jpg')), quality=86, optimize=True, progressive=True)
print('done')
