#!/usr/bin/env python3
"""RunAsDate-for-MacOS wordmark banner: a polar station in the middle of the long night,
stretched wide. Foreground sastrugi ridges in low green light and a fuel drum half buried
beside a path of marker wands. Middle: station huts on stilts, windows lit cream, aerial
masts and lightning rods still against the sky, a windsock at the masthead pulled straight
out by the katabatic wind. Twelve figures in heavy parkas scattered on the snow, most
looking up, one behind a tripod camera, one holding a mug that steams. Above everything
the aurora in folded curtains, jade over slate, stars hard and white between the folds.
The name RunAsDate-for-MacOS is painted in cream on the dark weather board fixed beside
the main hut door, in Anek Gurmukhi, part of the station furniture."""
import sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
random.seed(97)
W, H = 2560, 640
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
SLATE = (23, 34, 52); JADE = (64, 208, 164); CREAM = (240, 234, 208); BRASS = (178, 138, 74)
img = Image.new("RGB", (W, H), SLATE); d = ImageDraw.Draw(img, "RGBA")
for y in range(0, 430):
    t = y / 430
    d.line([(0, y), (W, y)], fill=(int(10 + 16 * t), int(18 + 22 * t), int(34 + 30 * t)))
for _ in range(420):
    x, y = random.randint(0, W), random.randint(0, 330)
    r = random.choice((1, 1, 2))
    d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 240, 245, random.randint(140, 255)))
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
for x0, top, x1 in ((0, 60, 700), (520, 30, 1290), (1120, 52, 1900), (1720, 26, 2560)):
    pts_top, pts_bot = [], []
    for i in range(21):
        t = i / 20; x = x0 + (x1 - x0) * t; sway = 34 * np.sin(t * 5.1 + x0)
        pts_top.append((x, top + sway * 0.4)); pts_bot.append((x, top + 236 + sway))
    ld.polygon(pts_top + pts_bot[::-1], fill=(64, 208, 164, 60))
    for i in range(20):
        ld.line([(pts_bot[i][0], pts_bot[i][1] - 44), (pts_bot[i + 1][0], pts_bot[i + 1][1] - 44)], fill=(226, 240, 208, 66), width=8)
img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(11))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# snowfield
d.rectangle([0, 428, W, H], fill=(168, 186, 205))
for i in range(30):
    x, y = random.randint(0, 2400), random.randint(470, 610)
    ln = random.randint(70, 210)
    d.arc([x, y, x + ln, y + 24], 190, 330, fill=(226, 240, 230, 120), width=3)
# marker wand path and a fuel drum half buried beside it
for x, y, s in ((150, 560, 52), (262, 528, 44), (360, 504, 37), (446, 486, 31)):
    d.line([(x, y), (x, y - s)], fill=(40, 44, 52), width=3)
    d.polygon([(x, y - s), (x + s * 0.55, y - s * 0.82), (x, y - s * 0.62)], fill=BRASS)
d.rectangle([520, 500, 576, 572], fill=(52, 62, 76), outline=(30, 36, 46), width=2)
d.polygon([(520, 572), (576, 572), (590, 592), (506, 592)], fill=(200, 212, 226))
# station huts on stilts across the middle
def hut(x, y, w, h, lit, board=False):
    for sx in (x + 14, x + w // 2, x + w - 22):
        d.line([(sx, y + h), (sx - 7, y + h + 40)], fill=(30, 36, 46), width=6)
        d.line([(sx, y + h), (sx + 9, y + h + 40)], fill=(30, 36, 46), width=6)
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 64))
    d.polygon([(x - 14, y), (x + w + 14, y), (x + w - 20, y - 28), (x + 20, y - 28)], fill=(26, 34, 48))
    d.line([(x + w // 2, y - 28), (x + w // 2, y - 84)], fill=(20, 26, 36), width=3)
    d.line([(x + 30, y - 26), (x + 30, y - 58)], fill=(20, 26, 36), width=2)
    for j, wx in enumerate(range(x + 22, x + w - 34, 54)):
        on = (j in lit)
        d.rectangle([wx, y + 28, wx + 28, y + 58], fill=CREAM if on else (18, 24, 34), outline=(12, 16, 24), width=2)
    dx = x + w - 74  # door
    d.rectangle([dx, y + 22, dx + 46, y + h], fill=(28, 36, 48), outline=(14, 18, 26), width=2)
    if board:
        bw = 560 if v == "ship" else 430
        d.rectangle([dx - bw - 26, y + 18, dx - 18, y + 84], fill=(30, 38, 50), outline=BRASS, width=3)
        f = ImageFont.truetype("fonts/AnekGurmukhi.ttf", 52 if v == "ship" else 40)
        txt = "RunAsDate-for-MacOS"; tw = d.textlength(txt, font=f)
        d.text((dx - bw - 22 + (bw - tw) / 2, y + 30), txt, font=f, fill=CREAM)
hut(880, 356, 620, 108, lit=(1, 4, 7), board=True)
hut(1620, 372, 460, 96, lit=(2, 5))
hut(2180, 384, 320, 84, lit=(3,))
# windsock masthead pulled straight out by the katabatic wind
d.line([(1560, 500), (1560, 330)], fill=(28, 34, 44), width=5)
d.polygon([(1560, 334), (1668, 342), (1664, 364), (1560, 358)], fill=(196, 120, 62))
d.polygon([(1560, 334), (1602, 338), (1600, 360), (1560, 358)], fill=CREAM)
# twelve figures in heavy parkas, most looking up
parkas = [(196, 120, 62), (150, 52, 44), (52, 84, 110), (110, 96, 52)]
spots = [(700, 520), (820, 548), (1010, 540), (1180, 556), (1330, 528), (1460, 552), (1700, 540),
         (1860, 558), (1990, 532), (2120, 552), (2300, 544), (2420, 560)]
for i, (x, y) in enumerate(spots):
    col = parkas[i % len(parkas)]; s = 1.0 + (i % 3) * 0.14
    d.polygon([(x - 15 * s, y + 52 * s), (x - 10 * s, y + 6 * s), (x + 10 * s, y + 6 * s), (x + 15 * s, y + 52 * s)], fill=col)
    d.ellipse([x - 10 * s, y - 12 * s, x + 10 * s, y + 8 * s], fill=(222, 196, 168))  # face turned up
    d.arc([x - 13 * s, y - 15 * s, x + 13 * s, y + 10 * s], 180, 360, fill=col, width=int(6 * s))  # hood rim
    if i == 4:  # tripod camera figure
        d.line([(x + 26, y + 52), (x + 44, y + 14), (x + 62, y + 52)], fill=(24, 28, 34), width=4)
        d.rectangle([x + 34, y + 2, x + 56, y + 16], fill=(24, 28, 34))
    if i == 7:  # mug that steams and freezes in the same breath
        d.rectangle([x + 16, y + 22, x + 30, y + 34], fill=CREAM)
        for k in range(4):
            d.ellipse([x + 19 + k * 2, y + 12 - k * 3, x + 24 + k * 2, y + 17 - k * 3], fill=(240, 244, 248, 150))
rng = np.random.default_rng(5); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "banner.png" if v == "ship" else f"scratch/banner-{v}.png"
img.save(out); print(out)
