#!/usr/bin/env python3
"""RunAsDate-for-MacOS logo: a station flag on a short brass pole, cloth rectangular and
stiff with cold, one corner lifted by wind, flat with no gradient. Cloth split between deep
jade green and cloud cream with a single slate stripe along the fly end. Wordmark below in
Anek Gurmukhi, level and spare, cream on slate, the way a duty officer rules a date line.
No penguin, no globe, no snowflake badge, no clock face. At 64px the flag alone carries it."""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W = H = 1024
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
SLATE = (23, 34, 52); JADE = (46, 178, 142); CREAM = (240, 234, 208); BRASS = (178, 138, 74)
img = Image.new("RGB", (W, H), SLATE); d = ImageDraw.Draw(img, "RGBA")
# snow footing line the pole stands in
d.rectangle([0, 742, W, 760], fill=(172, 190, 208))
for x in range(60, 980, 130):
    d.arc([x, 726, x + 92, 748], 190, 330, fill=(226, 240, 230), width=3)
# brass pole with plain ball finial
px = 330
d.line([(px, 128), (px, 748)], fill=BRASS, width=22)
d.ellipse([px - 24, 84, px + 24, 132], fill=BRASS)
d.line([(px, 128), (px, 748)], fill=(146, 110, 54), width=6)
# stiff cloth, one corner lifted by wind: jade over cream, slate stripe at the fly end
lift = 26 if v != "v1" else 0
cloth = [(px + 10, 140), (px + 470, 118 - lift), (px + 500, 150 - lift), (px + 500, 356), (px + 470, 392), (px + 10, 372)]
d.polygon(cloth, fill=JADE)
d.polygon([(px + 10, 262), (px + 478, 240 - lift), (px + 500, 268 - lift), (px + 500, 356), (px + 470, 392), (px + 10, 372)], fill=CREAM)
STRIPE = SLATE if v == "v1" else (52, 68, 90)  # fly end stripe lifted one step off the sky so it reads at 64px
d.polygon([(px + 424, 124 - lift), (px + 470, 118 - lift), (px + 500, 150 - lift), (px + 500, 356), (px + 470, 392), (px + 424, 388)], fill=STRIPE)
d.line([(px + 10, 140), (px + 10, 372)], fill=BRASS, width=6)
if v != "v1":
    f = ImageFont.truetype("fonts/AnekGurmukhi.ttf", 84)
    txt = "RunAsDate-for-MacOS"; tw = d.textlength(txt, font=f)
    d.text(((W - tw) / 2, 812), txt, font=f, fill=CREAM)
    d.line([(W - tw) / 2, 792, (W + tw) / 2, 792], fill=BRASS, width=3)  # the ruled date line
rng = np.random.default_rng(3); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 3, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "logo.png" if v == "ship" else f"scratch/logo-{v}.png"
img.save(out); print(out)
img.resize((64, 64), Image.LANCZOS).save(f"scratch/logo64-{v}.png"); print("64px saved")
