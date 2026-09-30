"""
Grade a Kling clip onto the site's ground.

Pass 1 (small frames): fit a smooth 2nd-order surface to the background of
every frame, per channel. The fit is robust — anything noticeably darker
than the surface (planets, their shadows) or coloured (rings) is dropped
and the surface refit — so it models the plate, not the objects on it.
The per-frame coefficients are then smoothed over time, because a surface
that re-fits independently every frame flickers.

Pass 2 (full frames): divide each frame by its surface and multiply by
235, which makes the plate exactly #EBEBEB everywhere and neutral (the
cool cast goes with it), while objects keep their contrast against it.
Optionally rotate hue and lift saturation — both done with the same
matrices CSS uses for hue-rotate()/saturate(), which leave greys grey, so
the ground is untouched by the colour move.

Loop: the last K frames are crossfaded into the first K, and the output
starts at frame K, so the end runs straight back into the beginning.
"""
import sys, subprocess, numpy as np, math

src, dst = sys.argv[1], sys.argv[2]
hue_deg = float(sys.argv[3]); sat_mul = float(sys.argv[4])
crop = sys.argv[5] if len(sys.argv) > 5 else ""       # "x,y,side,out" or ""
K = 12
import os
TARGET = 235.0
# the codec round-trip loses a few levels on flat grey; ENCODE_LIFT closes
# that gap and is measured on the decoded output, not guessed
LIFT = float(os.environ.get('ENCODE_LIFT', '1.0'))

def probe(p):
    out = subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","csv=p=0",p]).decode().strip()
    w,h = map(int,out.split(","))
    return w,h
W,H = probe(src)

def frames(p, w, h, scale=None):
    vf = ["-vf", f"scale={scale[0]}:{scale[1]}:flags=area"] if scale else []
    fw, fh = (scale if scale else (w, h))
    pr = subprocess.Popen(["ffmpeg","-v","error","-i",p,*vf,"-f","rawvideo",
                           "-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
    n = fw*fh*3
    while True:
        b = pr.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(fh, fw, 3).astype(np.float32)

# ---- pass 1: fit the plate on 160x90-ish frames -------------------------
sw, sh = 160, int(round(160*H/W))
ys, xs = np.mgrid[0:sh, 0:sw]
X = (xs/(sw-1))*2-1; Y = (ys/(sh-1))*2-1
basis = np.stack([np.ones_like(X), X, Y, X*X, X*Y, Y*Y, X**3, X*X*Y, X*Y*Y, Y**3], -1).reshape(-1, 10)

coefs = []
for f in frames(src, W, H, (sw, sh)):
    px = f.reshape(-1, 3)
    lum = px.mean(1); sat = px.max(1) - px.min(1)
    m = (sat < 16) & (lum > 120)
    c = np.zeros((10, 3), np.float32)
    for it in range(4):
        for ch in range(3):
            c[:, ch] = np.linalg.lstsq(basis[m], px[m, ch], rcond=None)[0]
        model = basis @ c
        res = px.mean(1) - model.mean(1)
        m = (sat < 16) & (res > -7) & (res < 9)
    coefs.append(c)
coefs = np.array(coefs)                                  # (N, 10, 3)
N = len(coefs)

# temporal smoothing — a surface that jitters frame to frame reads as flicker
win = 9
pad = np.concatenate([coefs[:1].repeat(win//2, 0), coefs, coefs[-1:].repeat(win//2, 0)])
kern = np.ones(win) / win
coefs = np.stack([np.convolve(pad[:, i, j], kern, 'valid')
                  for i in range(10) for j in range(3)], -1).reshape(N, 10, 3)


# ---- calibration ---------------------------------------------------------
meds = []
for i, f in enumerate(frames(src, W, H, (sw, sh))):
    if i % 10: continue
    px = f.reshape(-1, 3) * (TARGET / np.maximum(basis @ coefs[i], 40))
    lum = px.mean(1); sat = px.max(1) - px.min(1)
    m = (sat < 12) & (lum > 200)
    meds.append(np.median(px[m], 0))
GAIN = TARGET / np.median(np.array(meds), 0)            # per channel
print("calibration gain:", GAIN.round(4))

# ---- colour matrices, as CSS defines them -------------------------------
a = math.radians(hue_deg); cA, sA = math.cos(a), math.sin(a)
HUE = np.array([
 [0.213+cA*0.787-sA*0.213, 0.715-cA*0.715-sA*0.715, 0.072-cA*0.072+sA*0.928],
 [0.213-cA*0.213+sA*0.143, 0.715+cA*0.285+sA*0.140, 0.072-cA*0.072-sA*0.283],
 [0.213-cA*0.213-sA*0.787, 0.715-cA*0.715+sA*0.715, 0.072+cA*0.928+sA*0.072]], np.float32)
s = sat_mul
SAT = np.array([
 [0.213+0.787*s, 0.715-0.715*s, 0.072-0.072*s],
 [0.213-0.213*s, 0.715+0.285*s, 0.072-0.072*s],
 [0.213-0.213*s, 0.715-0.715*s, 0.072+0.928*s]], np.float32)
M = (SAT @ HUE).T

# full-res basis
yF, xF = np.mgrid[0:H, 0:W]
XF = (xF/(W-1))*2-1; YF = (yF/(H-1))*2-1
basisF = np.stack([np.ones_like(XF), XF, YF, XF*XF, XF*YF, YF*YF, XF**3, XF*XF*YF, XF*YF*YF, YF**3], -1).astype(np.float32)

def grade(f, c):
    plate = basisF @ c                                   # (H, W, 3)
    g = f * (TARGET / np.maximum(plate, 40)) * GAIN * LIFT
    if hue_deg or sat_mul != 1:
        g = g.reshape(-1, 3) @ M
        g = g.reshape(H, W, 3)
    return np.clip(g, 0, 255)

# ---- pass 2: grade and stream, folding the tail into the head ----------
# Streaming rather than holding 121 full frames: only the first K graded
# frames are kept, because they are what the tail fades into.
vf = []
ow, oh = W, H
cx = cy = side = osz = None
if crop:
    cx, cy, side, osz = map(int, crop.split(","))
    x0 = max(0, min(W - side, cx - side//2)); y0 = max(0, min(H - side, cy - side//2))
    ow = oh = side
    vf = ["-vf", f"scale={osz}:{osz}:flags=lanczos"]
def cut(f):
    return f[y0:y0+side, x0:x0+side] if crop else f

enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24",
    "-s",f"{ow}x{oh}","-r","24","-i","-",*vf,"-an","-c:v","libx264","-profile:v","main","-level","4.0","-preset","slow",
    "-crf", sys.argv[6] if len(sys.argv) > 6 else "24",
    "-pix_fmt","yuv420p","-movflags","+faststart", dst], stdin=subprocess.PIPE)

head = []
written = 0
for i, f in enumerate(frames(src, W, H)):
    g = cut(grade(f, coefs[min(i, N-1)]))
    if i < K:
        head.append(g); continue
    if i >= N - K:
        al = (i - (N - K) + 1) / (K + 1)
        g = (1 - al) * g + al * head[i - (N - K)]
    enc.stdin.write(np.ascontiguousarray(g.astype(np.uint8)).tobytes()); written += 1
enc.stdin.close(); enc.wait()
print(f"{dst}: {written} frames ({written/24:.2f}s), fold {K}f, hue {hue_deg}°, sat ×{sat_mul}")
