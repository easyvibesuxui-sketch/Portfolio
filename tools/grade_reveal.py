"""grade_reveal.py — Kling preloader reveal → assets/home/preload-eyes.mp4
· leaves the black→light reveal alone (it is the point)
· from frame FF on, flattens the plate toward #EBEBEB with a 2nd-order fit on
  the pixels that are plate in the hero's stage frame, ramped in so it never pops
· dissolves the last BL frames into the exact stage frame, then holds HOLD frames,
  so the video's last frame is the hero's first frame
usage: python3 grade_reveal.py src.mp4 stage.png dst.mp4 [lift]
"""
import sys, subprocess, numpy as np
from PIL import Image
src, stage_p, dst = sys.argv[1:4]
LIFT = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
W, H, T = 1920, 1080, 235.0
FF, BL, HOLD = 96, 20, 8
stage = np.asarray(Image.open(stage_p).convert('RGB').resize((W, H))).astype(np.float32)
plate = (np.abs(stage - T).max(2) < 1.5)
ys, xs = np.nonzero(plate[::8, ::8]); ys = ys * 8; xs = xs * 8
u = xs / W - .5; v = ys / H - .5
A = np.stack([np.ones_like(u), u, v, u*u, u*v, v*v], 1)
gu, gv = np.meshgrid(np.arange(W) / W - .5, np.arange(H) / H - .5)
G = np.stack([np.ones_like(gu), gu, gv, gu*gu, gu*gv, gv*gv], -1)
dec = subprocess.Popen(["ffmpeg","-v","error","-i",src,"-f","rawvideo","-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
N = int(subprocess.check_output(["ffprobe","-v","error","-count_frames","-select_streams","v:0",
    "-show_entries","stream=nb_read_frames","-of","csv=p=0",src]).decode().strip())
def frames():
    while True:
        b = dec.stdout.read(W*H*3)
        if len(b) < W*H*3: return
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","24","-i","-",
    "-an","-c:v","libx264","-profile:v","main","-level","4.0","-preset","slow","-crf","20",
    "-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709","-color_range","tv",
    "-movflags","+faststart", dst], stdin=subprocess.PIPE)
def sstep(x): x = min(max(x, 0), 1); return x*x*(3-2*x)
for i, f in enumerate(frames()):
    g = f
    wf = sstep((i - FF) / 24)
    if wf > 0:
        fit = np.empty_like(f)
        # sample only pixels that are plate in THIS frame too: grey and bright,
        # so a creature passing over a stage-plate pixel can't drag the fit
        smp = f[ys, xs]
        ok = (smp.max(1) - smp.min(1) < 7) & (smp.mean(1) > smp.mean(1).max() - 40)
        for c in range(3):
            coef, *_ = np.linalg.lstsq(A[ok], smp[ok, c], rcond=None)
            fit[..., c] = G @ coef
        gain = T / np.maximum(fit, 40)
        g = f * (1 + wf * (gain - 1))
    wb = sstep((i - (N - BL)) / (BL - 1))
    if wb > 0: g = (1 - wb) * g + wb * stage
    g = np.clip(g * LIFT, 0, 255)
    enc.stdin.write(g.astype(np.uint8).tobytes())
for _ in range(HOLD): enc.stdin.write(np.clip(stage * LIFT, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()
print(dst, N + HOLD, "frames")
