#!/usr/bin/env python3
"""Generate chibi anime mascot sprites for a Corne (CRKBD) OLED.

Canvas is the slave half in ROTATION_270 => logical 32 wide x 128 tall.
Each expression is a 32 x H 1-bpp sprite, row-major, MSB-first, 4 bytes/row.
Lit pixel = 1 (white on the OLED).  We draw line-art (outlines) which reads
best on a small mono panel.
"""
from PIL import Image, ImageDraw

W = 32
H = 38  # face sprite height (content fits; trailing blank rows trimmed)

def new():
    img = Image.new("1", (W, H), 0)
    return img, ImageDraw.Draw(img)

def px(d, x, y, v=1):
    if 0 <= x < W and 0 <= y < H:
        d.point((x, y), 1 if v else 0)

def hair_and_head(d):
    # head outline (rounded, slightly wider than tall for chibi look)
    d.ellipse((3, 6, 28, 36), outline=1)
    # bob hair cap: arc across the top, sitting just above the head ring
    d.arc((2, 1, 29, 24), start=180, end=360, fill=1)
    # side bangs (two short strokes framing the face)
    d.line((4, 8, 6, 16), fill=1)
    d.line((27, 8, 25, 16), fill=1)
    # center bang split
    d.line((16, 4, 16, 11), fill=1)
    d.line((13, 5, 14, 11), fill=1)
    d.line((19, 5, 18, 11), fill=1)
    # ahoge (the signature anime cowlick)
    d.line((16, 2, 19, 0), fill=1)
    d.line((19, 0, 22, 2), fill=1)

def blush(d):
    px(d, 6, 26); px(d, 7, 26); px(d, 8, 25)
    px(d, 25, 26); px(d, 24, 26); px(d, 23, 25)

def eyes_open(d, sparkle=True):
    # big round eyes, filled, with a dark sparkle dot
    d.ellipse((8, 18, 13, 25), fill=1)
    d.ellipse((18, 18, 23, 25), fill=1)
    if sparkle:
        px(d, 9, 19, 0); px(d, 10, 20, 0)
        px(d, 19, 19, 0); px(d, 20, 20, 0)

def eyes_excited(d):
    # huge sparkly eyes (>_< energy but wide-open shiny)
    d.ellipse((7, 16, 13, 25), fill=1)
    d.ellipse((18, 16, 24, 25), fill=1)
    # twin sparkle highlights
    for (cx, cy) in ((9, 18), (19, 18)):
        px(d, cx, cy, 0); px(d, cx + 1, cy, 0)
        px(d, cx, cy + 1, 0)
        px(d, cx + 2, cy + 2, 0)

def eyes_happy(d):
    # ^_^ closed-happy arcs
    d.arc((7, 18, 14, 26), start=200, end=340, fill=1)
    d.arc((18, 18, 25, 26), start=200, end=340, fill=1)

def eyes_closed(d):
    # gentle ^ closed line (blink / sleep) -- slightly flatter than happy
    d.line((8, 22, 11, 21), fill=1); d.line((11, 21, 13, 22), fill=1)
    d.line((19, 22, 22, 21), fill=1); d.line((22, 21, 24, 22), fill=1)

def mouth_cat(d):
    # tiny w cat mouth
    d.line((14, 30, 15, 31), fill=1); d.line((15, 31, 16, 30), fill=1)
    d.line((16, 30, 17, 31), fill=1); d.line((17, 31, 18, 30), fill=1)

def mouth_open(d):
    d.ellipse((14, 29, 18, 33), outline=1)

def mouth_smile(d):
    d.arc((12, 27, 20, 33), start=20, end=160, fill=1)

def zzz(d):
    # little floating z's above the head for sleep
    def z(x, y, s):
        d.line((x, y, x + s, y), fill=1)
        d.line((x + s, y, x, y + s), fill=1)
        d.line((x, y + s, x + s, y + s), fill=1)
    z(24, 2, 3)
    z(28, 7, 2)

def sweat(d):
    # excited/effort sweat drop by the cheek
    d.line((28, 16, 28, 19), fill=1)
    px(d, 27, 18); px(d, 29, 18); px(d, 28, 20)

# ---- expression set ----
def f_neutral():
    img, d = new(); hair_and_head(d); blush(d); eyes_open(d); mouth_cat(d); return img
def f_blink():
    img, d = new(); hair_and_head(d); blush(d); eyes_closed(d); mouth_cat(d); return img
def f_sleep():
    img, d = new(); hair_and_head(d); eyes_closed(d); mouth_smile(d); zzz(d); return img
def f_happy():
    img, d = new(); hair_and_head(d); blush(d); eyes_happy(d); mouth_smile(d); return img
def f_excited():
    img, d = new(); hair_and_head(d); blush(d); eyes_excited(d); mouth_open(d); sweat(d); return img

# ---- body (drawn on its own BH-tall canvas, stacked under the head) ----
BH = 34  # body sprite height

def new_body():
    img = Image.new("1", (W, BH), 0)
    return img, ImageDraw.Draw(img)

def bpx(d, x, y, v=1):
    if 0 <= x < W and 0 <= y < BH:
        d.point((x, y), 1 if v else 0)

def body_base(d):
    # neck
    d.line((15, 0, 15, 3), fill=1); d.line((17, 0, 17, 3), fill=1)
    # collar
    d.line((12, 4, 20, 4), fill=1)
    # little collar V
    d.line((14, 5, 16, 8), fill=1); d.line((16, 8, 18, 5), fill=1)
    # clean bell-shaped dress: two side edges flaring to a simple hem
    d.line((12, 4, 7, 24), fill=1)
    d.line((20, 4, 25, 24), fill=1)
    d.line((7, 24, 25, 24), fill=1)
    # short legs + little feet poking out under the hem
    d.line((13, 24, 13, 30), fill=1); d.line((19, 24, 19, 30), fill=1)
    d.line((10, 30, 13, 30), fill=1); d.line((19, 30, 22, 30), fill=1)

def arms_down(d):
    # stubby arms resting along the dress
    d.line((12, 5, 8, 17), fill=1); d.line((8, 17, 10, 19), fill=1)
    d.line((20, 5, 24, 17), fill=1); d.line((24, 17, 22, 19), fill=1)

def arms_up(d):
    # \o/ raised arms for the excited cheer
    d.line((12, 5, 6, 1), fill=1);  bpx(d, 5, 0); bpx(d, 6, 0)
    d.line((20, 5, 26, 1), fill=1); bpx(d, 25, 0); bpx(d, 26, 0)

def b_idle():
    img, d = new_body(); body_base(d); arms_down(d); return img
def b_cheer():
    img, d = new_body(); body_base(d); arms_up(d); return img

HEADS = [
    ("neutral", f_neutral()),
    ("blink",   f_blink()),
    ("sleep",   f_sleep()),
    ("happy",   f_happy()),
    ("excited", f_excited()),
]
BODIES = [
    ("idle",  b_idle()),
    ("cheer", b_cheer()),
]

def preview(name, img):
    w, h = img.size
    print(f"--- {name} ({w}x{h}) ---")
    px_ = img.load()
    for y in range(h):
        print("".join("##" if px_[x, y] else "  " for x in range(w)))
    print()

def pack(img):
    w, h = img.size
    px_ = img.load()
    out = []
    bpr = (w + 7) // 8
    for y in range(h):
        for bx in range(bpr):
            b = 0
            for bit in range(8):
                x = bx * 8 + bit
                if x < w and px_[x, y]:
                    b |= 1 << (7 - bit)
            out.append(b)
    return out

import sys
ALL = [(f"head_{n}", i) for n, i in HEADS] + [(f"body_{n}", i) for n, i in BODIES]
if "--emit" in sys.argv:
    print("// Generated by gen_avatar.py -- chibi anime mascot for a vertically-mounted")
    print("// Corne OLED (slave half, OLED_ROTATION_270 => 32 wide x 128 tall logical).")
    print("// Sprites are 1bpp, row-major, MSB-first. Head stacks on top of body.")
    print("#pragma once")
    print(f"#define AVATAR_W {W}")
    print(f"#define HEAD_H {H}")
    print(f"#define BODY_H {BH}")
    for name, img in ALL:
        data = pack(img)
        body = ", ".join(f"0x{b:02X}" for b in data)
        print(f"static const uint8_t PROGMEM avatar_{name}[{len(data)}] = {{ {body} }};")
    print(f"// total sprite bytes: {sum(len(pack(i)) for _, i in ALL)}")
else:
    # stack each head over the idle body for a full-figure preview
    for hn, himg in HEADS:
        combo = Image.new("1", (W, H + BH), 0)
        combo.paste(himg, (0, 0))
        bimg = dict(BODIES)["cheer" if hn == "excited" else "idle"]
        combo.paste(bimg, (0, H))
        preview(hn, combo)
    print(f"total sprite bytes: {sum(len(pack(i)) for _, i in ALL)}")
