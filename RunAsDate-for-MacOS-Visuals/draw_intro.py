#!/usr/bin/env python3
"""RunAsDate-for-MacOS introduction banner: Antarctic station in the long night, wordless.
Foreground: a lone flagpole in blue shadowed snow, flag snapping, guy ropes to ice anchors,
a wooden crate with a coil of line and mittens left on its lid. Midground: an empty station
yard, huts on stilts with two windows lit, a windsock swinging slow, fuel drums, a tracked
vehicle with snow banked at its skids, marker wands on a path to the horizon. Background:
plateau and a sky more than half the frame, crowded stars, aurora curtains jade paling to
cream, slate shadow between folds. No text, letters, numerals, signs, or logos anywhere."""
import sys, random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
random.seed(71)
W, H = 1600, 900
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
SLATE = (23, 34, 52); JADE = (64, 208, 164); CREAM = (240, 234, 208); BRASS = (178, 138, 74)
img = Image.new("RGB", (W, H), SLATE); d = ImageDraw.Draw(img, "RGBA")
# polar night sky, deep slate easing down toward the plateau
for y in range(0, 620):
    t = y / 620
    d.line([(0, y), (W, y)], fill=(int(10 + 16 * t), int(18 + 22 * t), int(34 + 30 * t)))
# crowded stars, hard and white
for _ in range(340):
    x, y = random.randint(0, W), random.randint(0, 470)
    r = random.choice((1, 1, 2))
    d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 240, 245, random.randint(140, 255)))
# one clear constellation standing above the hut roofs (a loose chart cross)
for x, y in ((980, 96), (1032, 128), (1086, 106), (1130, 150), (1018, 176)):
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(250, 250, 246))
    d.line([(x - 8, y), (x + 8, y)], fill=(250, 250, 246, 150), width=1)
    d.line([(x, y - 8), (x, y + 8)], fill=(250, 250, 246, 150), width=1)
# aurora curtains: folded veils, jade paling to cream at the lower edge, slate between folds
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
curtains = [(60, 150, 420), (330, 96, 760), (640, 130, 1080), (950, 84, 1400), (1230, 140, 1620)]
amp = 26 if v == "v1" else 44
for x0, top, x1 in curtains:
    pts_top, pts_bot = [], []
    for i in range(21):
        t = i / 20
        x = x0 + (x1 - x0) * t
        sway = amp * np.sin(t * 5.1 + x0)
        pts_top.append((x, top + sway * 0.4))
        pts_bot.append((x, top + 330 + sway))
    ld.polygon(pts_top + pts_bot[::-1], fill=(64, 208, 164, 62))
    for i in range(20):
        x_a, y_a = pts_bot[i]; x_b, y_b = pts_bot[i + 1]
        ld.line([(x_a, y_a - 60), (x_b, y_b - 60)], fill=(226, 240, 208, 70), width=10)
img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(13))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# plateau snowfield, blue shadowed, sastrugi ridges catching low green light
d.rectangle([0, 600, W, H], fill=(172, 190, 208))
for y in range(600, H):
    t = (y - 600) / 300
    d.line([(0, y), (W, y)], fill=(int(172 - 30 * t), int(190 - 26 * t), int(208 - 18 * t)))
for i in range(26):
    x, y = random.randint(0, 1500), random.randint(640, 860)
    ln = random.randint(60, 190)
    d.arc([x, y, x + ln, y + 26], 190, 330, fill=(226, 240, 230, 130), width=3)
    d.arc([x + 4, y + 7, x + ln, y + 30], 190, 330, fill=(120, 140, 168, 110), width=3)
# marker wand path running diagonally from the foreground toward the horizon
for i, (x, y, s) in enumerate(((180, 790, 64), (300, 742, 54), (398, 706, 45), (478, 680, 38), (545, 660, 31))):
    d.line([(x, y), (x, y - s)], fill=(40, 44, 52), width=3)
    d.polygon([(x, y - s), (x + s * 0.55, y - s * 0.82), (x, y - s * 0.62)], fill=BRASS)
# midground huts on stilts, two windows lit cream, the rest dark
def hut(x, y, w, h, lit):
    for sx in (x + 12, x + w // 2, x + w - 20):
        d.line([(sx, y + h), (sx - 6, y + h + 44)], fill=(30, 36, 46), width=6)
        d.line([(sx, y + h), (sx + 8, y + h + 44)], fill=(30, 36, 46), width=6)
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 64))
    d.polygon([(x - 12, y), (x + w + 12, y), (x + w - 18, y - 26), (x + 18, y - 26)], fill=(26, 34, 48))
    d.line([(x + w // 2, y - 26), (x + w // 2, y - 66)], fill=(20, 26, 36), width=3)  # aerial mast, still
    d.line([(x + 22, y - 24), (x + 22, y - 52)], fill=(20, 26, 36), width=2)  # lightning rod, still
    for j, wx in enumerate(range(x + 18, x + w - 30, 44)):
        on = (j in lit)
        d.rectangle([wx, y + 26, wx + 24, y + 52], fill=CREAM if on else (18, 24, 34),
                    outline=(12, 16, 24), width=2)
hut(120, 520, 300, 96, lit=(1,))
hut(470, 540, 230, 84, lit=(3,))
hut(760, 530, 190, 78, lit=())
# fuel drums in a row
for i, x in enumerate(range(990, 1150, 38)):
    d.rectangle([x, 566, x + 30, 622], fill=(52, 62, 76), outline=(30, 36, 46), width=2)
    d.line([(x, 584), (x + 30, 584)], fill=(30, 36, 46), width=2)
# tracked vehicle parked, snow banked against its skids
d.rectangle([1230, 556, 1440, 606], fill=(44, 54, 68))
d.rectangle([1300, 524, 1396, 558], fill=(44, 54, 68))
d.rectangle([1314, 532, 1350, 550], fill=(18, 24, 34))
d.rounded_rectangle([1216, 600, 1456, 632], 14, fill=(34, 42, 54))
d.polygon([(1216, 632), (1300, 606), (1456, 632)], fill=(196, 210, 224))
# windsock on its own mast in the gap between huts, swinging slow
d.line([(728, 640), (728, 486)], fill=(28, 34, 44), width=5)
sock_tilt = 10 if v != "v1" else 2
d.polygon([(728, 490), (786, 500 + sock_tilt), (782, 518 + sock_tilt), (728, 512)], fill=(196, 120, 62))
d.polygon([(728, 490), (752, 494), (750, 514), (728, 512)], fill=CREAM)
# foreground flagpole at the right third, guy ropes out to ice anchors, frost on the lower rope
px, ptop, pbase = 1085, 250, 838
for ax in (px - 250, px + 265):
    d.line([(px, ptop + 26), (ax, pbase)], fill=(210, 218, 226, 200), width=3)
    d.ellipse([ax - 7, pbase - 5, ax + 7, pbase + 5], fill=(90, 100, 114))
for fx in range(px - 120, px - 30, 12):  # frost feathering on the lower left rope
    d.line([(fx, pbase - (fx - (px - 250)) * 2.35 + 580), (fx - 5, pbase - (fx - (px - 250)) * 2.35 + 592)], fill=(240, 246, 250, 160), width=2)
d.line([(px, ptop), (px, pbase)], fill=(24, 28, 36), width=8)
d.ellipse([px - 8, ptop - 14, px + 8, ptop + 2], fill=BRASS)  # finial ball
# the flag, snapping: stiff cloth, jade over cream, one slate stripe at the fly end
wave = [(px, ptop + 6), (px + 96, ptop - 4), (px + 196, ptop + 12), (px + 262, ptop + 2),
        (px + 262, ptop + 62), (px + 196, ptop + 76), (px + 96, ptop + 58), (px, ptop + 68)]
d.polygon(wave, fill=JADE)
d.polygon([(px, ptop + 36), (px + 98, ptop + 27), (px + 197, ptop + 44), (px + 262, ptop + 33),
           (px + 262, ptop + 62), (px + 196, ptop + 76), (px + 96, ptop + 58), (px, ptop + 68)], fill=CREAM)
d.polygon([(px + 224, ptop + 6), (px + 262, ptop + 2), (px + 262, ptop + 62), (px + 224, ptop + 70)], fill=SLATE)
# wooden crate at the pole base, coil of line, mittens left on the lid
d.rectangle([px - 210, 752, px - 60, 838], fill=(104, 78, 48))
d.rectangle([px - 210, 752, px - 60, 776], fill=(124, 96, 58))
for r in (30, 21, 12):
    d.ellipse([px - 178 - r, 742 - r // 2, px - 178 + r, 742 + r // 2 + 8], outline=(196, 168, 116), width=5)
# aurora fold striations on the ship render: vertical light seams inside the curtains
if v == "ship":
    st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    for sx in range(90, 1560, 64):
        top = 90 + 60 * np.sin(sx / 210.0)
        sd.line([(sx, top), (sx + 26, top + 330)], fill=(150, 235, 200, 34), width=15)
        sd.line([(sx + 30, top + 20), (sx + 52, top + 320)], fill=(16, 30, 48, 40), width=11)
    img = Image.alpha_composite(img.convert("RGBA"), st.filter(ImageFilter.GaussianBlur(9))).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
for mx, col in ((px - 118, (168, 52, 44)), (px - 88, (168, 52, 44))):  # mittens, thumb bumps
    d.rounded_rectangle([mx, 716, mx + 26, 754], 11, fill=col)
    d.ellipse([mx + 18, 736, mx + 32, 752], fill=col)
# window light pools on the snow
for cx in (252, 602):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - 90, 640, cx + 90, 690], fill=(240, 226, 170, 52))
    img = Image.alpha_composite(img.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(18))).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
rng = np.random.default_rng(7); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "intro-banner.png" if v == "ship" else f"scratch/intro-{v}.png"
img.save(out); print(out)
