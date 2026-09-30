"""Small eye layers for the creatures that live around the site (peek.js).
    python3 tools/build_mini.py <out_dir> id=path ...
Same split as the hero (tools/eyes.py), just smaller: every placement is at
most ~240px tall on screen, so 480px layers stay sharp on retina."""
import sys, os, json, cv2
sys.path.insert(0, os.path.dirname(__file__))
from eyes import split
LENS = json.load(open(os.path.join(os.path.dirname(__file__), "lens.json")))
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
man = {}
for cid, path in (a.split("=", 1) for a in sys.argv[2:]):
    spec = LENS.get(cid, {})
    rec = split(path, f"/tmp/mini-{cid}", target_h=480, lens=spec.get("lens"), iris=spec.get("iris"))
    files = {}
    for k in ("body", "iris", "mask", "shade", "hl"):
        im = cv2.imread(f"/tmp/mini-{cid}-{k}.png", cv2.IMREAD_UNCHANGED)
        if k in ("body", "iris"):
            n = f"{cid}-{k}.webp"; cv2.imwrite(os.path.join(out, n), im, [cv2.IMWRITE_WEBP_QUALITY, 88])
        else:
            n = f"{cid}-{k}.png"; cv2.imwrite(os.path.join(out, n), im, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        files[k] = n
    man[cid] = dict(files=files, geom=rec)
json.dump(man, open(os.path.join(out, "manifest.json"), "w"), indent=1)
print({k: (v["geom"]["w"], v["geom"]["h"]) for k, v in man.items()})
