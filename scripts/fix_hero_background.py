"""
Replace the hero illustration's background with the exact app background
color, preserving anti-aliased line edges via alpha-based recompositing.

The source art is rust-colored line work on a near-solid off-white
background (not pure white, not a gradient/photo). A hard brightness
threshold can't cleanly separate ink from background here because
anti-aliased edge pixels are partial blends of ink and the OLD
background color -- naively leaving them as-is bakes in a mismatched
tint against the NEW background.

Instead, per-pixel opacity (how "inky" a pixel is) is estimated from
luminance, and each pixel is recomposited from the old background onto
the new one:

    C_new = C + (1 - alpha) * (bg_new - bg_old)

alpha=1 (pure ink) leaves the pixel unchanged; alpha=0 (pure
background) fully replaces it; partial alpha blends proportionally,
so anti-aliased fringes shift color without banding.
"""

from pathlib import Path
import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
SRC = BASE_DIR / "assets" / "apple tree.png"
OUT = BASE_DIR / "assets" / "apple_tree_display.png"
TARGET_BG = (250, 243, 235)  # #FAF3EB

# Measured in-browser: cssWidth 273.609375px * devicePixelRatio 2 * 2 (retina
# sharpness margin) = 1094.4 -> 1094px. Must match the width= passed to
# st.image() in app/streamlit_app.py, since Streamlit re-encodes the source
# to that exact raster size server-side -- any extra resolution beyond it is
# discarded before the browser ever sees it.
OUTPUT_SIZE = 1094


def luminance(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


img = Image.open(SRC).convert("RGB")
arr = np.asarray(img).astype(np.float64)

# Sample the source's own background color from a corner patch, rather
# than assuming pure white.
corner_patch = arr[0:6, 0:6, :].reshape(-1, 3)
bg_old = corner_patch.mean(axis=0)

lum = luminance(arr)
lum_bg = luminance(bg_old[None, None, :])[0, 0]
lum_ink = lum.min()  # darkest pixel approximates full ink coverage

denom = max(lum_bg - lum_ink, 1e-6)
alpha = np.clip((lum_bg - lum) / denom, 0.0, 1.0)  # 0=background, 1=ink

bg_new = np.array(TARGET_BG, dtype=np.float64)
delta = bg_new - bg_old
new_arr = arr + (1.0 - alpha)[..., None] * delta[None, None, :]
new_arr = np.clip(new_arr, 0, 255).astype(np.uint8)

result = Image.fromarray(new_arr, mode="RGB")
resized = result.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.LANCZOS)
resized.save(OUT, optimize=True)

print(f"sampled old background: {tuple(bg_old.round(1))}")
print(f"saved: {OUT} ({resized.size[0]}x{resized.size[1]})")
