"""
Assemble the hero from creature stills.

    python3 tools/build_eyes.py <out_dir> id=path ... [--test]

Each creature is split into layers (tools/eyes.py), written as WebP/PNG,
and placed on a 1920x1080 stage. Two things come out besides the layers:

  manifest.json   what eyes.js needs to place and animate everything
  stage.png       the stage exactly as the page draws its first frame —
                  every iris centred, nothing breathing. This is the
                  preloader video's last frame, so the video can end on
                  the same picture the page starts on.
"""
import sys, os, json, cv2, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from eyes import split

STAGE = (1920, 1080)
# hand-measured eye openings (and, where detection missed, the iris) —
# see tools/lens.json; coordinates are in the 1400px working image
LENS = json.load(open(os.path.join(os.path.dirname(__file__), "lens.json")))
GROUND = (235, 235, 235)
HALO = (70, 35, 30, 0.28)      # rgb + peak alpha of the limbal shadow
# where each creature lives on the stage: centre x, centre y, height.
# The central one sits above the hero copy, which is set at ~74% height.
PLACE = {
    "p1": dict(x=960,  y=400, h=560, central=True,  speed=0.9, phase=0.11),
    "b":  dict(x=1575, y=735, h=420, central=False, speed=0.6, phase=0.47),
    "c":  dict(x=330,  y=320, h=330, central=False, speed=1.1, phase=0.73),
    "d":  dict(x=1545, y=215, h=210, central=False, speed=1.4, phase=0.29),
}

def over(dst, src_rgba, x, y):
    """alpha-composite src onto dst at integer (x, y), clipped"""
    h, w = src_rgba.shape[:2]
    X0, Y0 = max(0, x), max(0, y)
    X1, Y1 = min(dst.shape[1], x+w), min(dst.shape[0], y+h)
    if X1 <= X0 or Y1 <= Y0: return
    s = src_rgba[Y0-y:Y1-y, X0-x:X1-x].astype(np.float32)
    a = s[..., 3:4] / 255.0
    d = dst[Y0:Y1, X0:X1].astype(np.float32)
    dst[Y0:Y1, X0:X1] = (s[..., :3] * a + d * (1 - a)).astype(np.uint8)

def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    pairs = [a.split("=", 1) for a in sys.argv[2:] if "=" in a]
    man = dict(stage=dict(w=STAGE[0], h=STAGE[1]), creatures=[])
    canvas = np.full((STAGE[1], STAGE[0], 3), GROUND, np.uint8)
    for cid, path in pairs:
        pl = PLACE[cid]
        # layers at ~2x the height they are shown, so they stay sharp on
        # a retina screen at full-width stage scale
        spec = LENS.get(cid, {})
        rec = split(path, os.path.join("/tmp", "eyes-" + cid), target_h=min(1400, pl["h"]*2),
                    lens=spec.get("lens"), iris=spec.get("iris"))
        files = {}
        for k in ("body", "iris", "mask", "shade", "hl"):
            src = cv2.imread(f"/tmp/eyes-{cid}-{k}.png", cv2.IMREAD_UNCHANGED)
            if k in ("body", "iris"):
                name = f"{cid}-{k}.webp"
                cv2.imwrite(os.path.join(out, name), src, [cv2.IMWRITE_WEBP_QUALITY, 90])
            else:
                name = f"{cid}-{k}.png"
                cv2.imwrite(os.path.join(out, name), src, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            files[k] = name
        man["creatures"].append(dict(id=cid, x=pl["x"], y=pl["y"], h=pl["h"],
                                     central=pl["central"], speed=pl["speed"], phase=pl["phase"],
                                     files=files, geom=rec))

        # --- first frame, the way eyes.js draws it with the gaze at rest
        k = pl["h"] / rec["h"]
        body = cv2.imread(f"/tmp/eyes-{cid}-body.png", cv2.IMREAD_UNCHANGED)
        bw, bh = round(body.shape[1]*k), round(body.shape[0]*k)
        bx, by = round(pl["x"] - bw/2), round(pl["y"] - bh/2)
        body_s = cv2.resize(body, (bw, bh), interpolation=cv2.INTER_AREA)
        e = rec["eye"]; ir = rec["iris"]
        ew, eh = max(1, round(e["w"]*k)), max(1, round(e["h"]*k))
        iris = cv2.imread(f"/tmp/eyes-{cid}-iris.png", cv2.IMREAD_UNCHANGED)
        isz = max(1, round(ir["size"]*k))
        iris_s = cv2.resize(iris, (isz, isz), interpolation=cv2.INTER_AREA)
        eye = np.zeros((eh, ew, 4), np.float32)
        ix, iy = round((ir["cx"]-e["x"])*k - isz/2), round((ir["cy"]-e["y"])*k - isz/2)
        # paste the iris into the eye buffer
        tmp = np.zeros((eh, ew, 4), np.uint8)
        X0, Y0 = max(0, ix), max(0, iy); X1, Y1 = min(ew, ix+isz), min(eh, iy+isz)
        tmp[Y0:Y1, X0:X1] = iris_s[Y0-iy:Y1-iy, X0-ix:X1-ix]
        eye = tmp.astype(np.float32)
        shade = cv2.resize(cv2.imread(f"/tmp/eyes-{cid}-shade.png", 0), (ew, eh)).astype(np.float32)/255
        mask  = cv2.resize(cv2.imread(f"/tmp/eyes-{cid}-mask.png", 0), (ew, eh)).astype(np.float32)/255
        eye[..., :3] *= shade[..., None]
        # limbal shadow: a soft dark ring that travels with the iris, drawn
        # behind it (eyes.js draws the same gradient, same numbers)
        R = ir["r"]*k; ccx = (ir["cx"]-e["x"])*k; ccy = (ir["cy"]-e["y"])*k
        gy, gx = np.mgrid[0:eh, 0:ew].astype(np.float32)
        dd = np.hypot(gx + 0.5 - ccx, gy + 0.5 - ccy)
        ha = HALO[3] * np.clip((R*1.2 - dd) / (R*0.25), 0, 1)
        ia = eye[..., 3:4] / 255.0
        hb = ha[..., None] * (1 - ia)
        oa = ia + hb
        eye[..., :3] = (eye[..., :3] * ia + np.array(HALO[:3], np.float32)[::-1] * hb) / np.maximum(oa, 1e-4)  # BGR
        eye[..., 3] = oa[..., 0] * 255
        eye[..., 3] *= mask
        hl = cv2.resize(cv2.imread(f"/tmp/eyes-{cid}-hl.png", cv2.IMREAD_UNCHANGED), (ew, eh))
        # composite in the same order as the page: body, iris, catchlight
        over(canvas, body_s, bx, by)
        ex, ey = round(bx + e["x"]*k), round(by + e["y"]*k)
        over(canvas, eye.clip(0, 255).astype(np.uint8), ex, ey)
        over(canvas, hl, ex, ey)

    json.dump(man, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    cv2.imwrite(os.path.join(out, "stage.png"), canvas)
    cv2.imwrite(os.path.join(out, "stage.jpg"), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("manifest + stage written:", out, [c["id"] for c in man["creatures"]])

if __name__ == "__main__":
    main()
