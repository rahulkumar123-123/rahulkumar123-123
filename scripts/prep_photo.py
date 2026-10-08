from pathlib import Path
import cv2, numpy as np

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'source-photo.jpg'
out = ROOT / 'source-prepped.png'

img = cv2.imread(str(src))
if img is None:
    raise SystemExit(f'Could not read {src}')

# Crop to portrait while retaining shoulders/tie.
h, w = img.shape[:2]
target_ratio = 0.72
cur = w / h
if cur > target_ratio:
    nw = int(h * target_ratio)
    x = (w - nw) // 2
    img = img[:, x:x+nw]
else:
    nh = int(w / target_ratio)
    y = max(0, (h - nh) // 2)
    img = img[y:y+nh, :]

# GrabCut isolates the central subject without requiring rembg at build time.
mask = np.zeros(img.shape[:2], np.uint8)
rect = (int(img.shape[1]*0.08), int(img.shape[0]*0.04),
        int(img.shape[1]*0.84), int(img.shape[0]*0.94))
bgd = np.zeros((1,65), np.float64)
fgd = np.zeros((1,65), np.float64)
try:
    cv2.grabCut(img, mask, rect, bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    keep = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    # Keep central connected component(s) and soften edge.
    keep = cv2.medianBlur(keep, 5)
except cv2.error:
    keep = np.full(img.shape[:2], 255, np.uint8)

# Feather and composite onto white.
keep_f = cv2.GaussianBlur(keep, (0,0), 1.2).astype(np.float32)/255.0
bg = np.full_like(img, 255)
comp = img.astype(np.float32)*keep_f[...,None] + bg.astype(np.float32)*(1-keep_f[...,None])
comp = np.clip(comp,0,255).astype(np.uint8)

gray = cv2.cvtColor(comp, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.4, tileGridSize=(8,8))
gray = clahe.apply(gray)
# Increase global contrast gently.
gray = cv2.normalize(gray, None, 15, 245, cv2.NORM_MINMAX)
cv2.imwrite(str(out), gray)
print(out)
