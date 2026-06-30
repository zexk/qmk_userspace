#!/usr/bin/env python3
"""Generate chibi anime mascot sprites for a Corne (CRKBD) OLED.

Canvas is the slave half in ROTATION_270 => logical 32 wide x 128 tall.
Each expression is a 32 x H 1-bpp sprite, row-major, MSB-first, 4 bytes/row.
Lit pixel = 1 (white on the OLED).  We draw line-art (outlines) which reads
best on a small mono panel.
"""
from PIL import Image, ImageDraw

W = 32
H = 42  # face sprite height

def new():
    img = Image.new("1", (W, H), 0)
    return img, ImageDraw.Draw(img)

def px(d, x, y, v=1):
    if 0 <= x < W and 0 <= y < H:
        d.point((x, y), 1 if v else 0)

# Silhouette style: the head is a SOLID white shape; eyes/mouth/blush are dark
# cutouts (fill=0) with white sparkles. Bold and legible on a mono panel.
# Bold hair as a solid white mass; the FACE is a dark cut-out framed by hair,
# so the hairstyle reads as a real silhouette. Features are white on the dark face.
def hair_and_head(d):
    d.ellipse((2, 3, 29, 40), fill=1)                       # solid hair mass
    # ahoge cowlick, curling off to one side
    d.polygon([(15, 4), (18, 0), (22, 0), (20, 4), (18, 6)], fill=1)
    # carve the dark face
    d.ellipse((6, 15, 25, 39), fill=0)
    # spiky bang tips -- off-centre part, uneven lengths (asymmetry)
    d.polygon([(6, 14), (8, 22), (11, 15)], fill=1)
    d.polygon([(11, 15), (14, 26), (17, 15)], fill=1)       # long centre-left tip
    d.polygon([(17, 15), (20, 20), (25, 14)], fill=1)       # shorter right
    # side-locks: long flowing lock on the left, short on the right
    d.polygon([(7, 16), (1, 38), (8, 31)], fill=1)
    d.polygon([(24, 16), (28, 29), (23, 26)], fill=1)
    # little star hair-clip on the right bang (asymmetric accent)
    px(d, 21, 12, 0); px(d, 21, 13, 0); px(d, 21, 14, 0)
    px(d, 20, 13, 0); px(d, 22, 13, 0)

def blush(d):
    # white blush ticks on the dark cheeks
    for yy in (30, 31):
        d.line((8, yy, 10, yy), fill=1)
        d.line((21, yy, 23, yy), fill=1)

def _eye_cut(d, cx, cy, rx, ry, star=False):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=1)  # white eye on dark face
    # dark pupil + a white catch-light so it reads shiny, not blank
    d.ellipse((cx - rx + 2, cy - ry + 2, cx + rx - 1, cy + ry - 1), fill=0)
    px(d, cx - 1, cy - 1, 1)
    if star:
        px(d, cx + 1, cy + 1, 1)

def eyes_open(d):
    _eye_cut(d, 11, 27, 3, 4)
    _eye_cut(d, 20, 27, 3, 4)

def eyes_excited(d):
    _eye_cut(d, 11, 27, 4, 5, star=True)
    _eye_cut(d, 20, 27, 4, 5, star=True)

def eyes_happy(d):
    # winking: open shiny eye on the left, happy caret on the right
    _eye_cut(d, 11, 27, 3, 4)
    for off in (0, 1):
        d.arc((17, 26 + off, 23, 32 + off), 200, 340, fill=1)

def eyes_closed(d):
    # relaxed downward lashes (u u)
    for off in (0, 1):
        d.arc((8, 26 + off, 14, 31 + off), 20, 160, fill=1)
        d.arc((17, 26 + off, 23, 31 + off), 20, 160, fill=1)

def mouth_cat(d):
    d.arc((13, 33, 16, 37), 20, 160, fill=1)
    d.arc((16, 33, 19, 37), 20, 160, fill=1)

def mouth_open(d):
    d.ellipse((14, 33, 18, 38), fill=1)

def mouth_smile(d):
    d.arc((12, 33, 20, 39), 20, 160, fill=1)

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
    # short neck
    d.rectangle((14, 0, 17, 1), fill=1)
    # solid A-line dress
    d.polygon([(11, 3), (20, 3), (25, 23), (6, 23)], fill=1)
    # round collar (dark notch under the neck)
    d.arc((13, 1, 18, 6), 20, 160, fill=0)
    # waist belt (dark) + a centre skirt pleat
    d.line((10, 12, 21, 12), fill=0)
    d.line((16, 13, 16, 22), fill=0)
    # small ribbon bow on the skirt, off to one side (asymmetric flair)
    d.line((9, 14, 12, 16), fill=0); d.line((9, 18, 12, 16), fill=0); d.line((9, 14, 9, 18), fill=0)
    d.line((15, 14, 12, 16), fill=0); d.line((15, 18, 12, 16), fill=0); d.line((15, 14, 15, 18), fill=0)
    # slim legs
    d.rectangle((13, 23, 14, 28), fill=1)
    d.rectangle((17, 23, 18, 28), fill=1)
    # rounded shoes
    d.rectangle((10, 28, 14, 31), fill=1); px(d, 9, 30); px(d, 9, 31)
    d.rectangle((17, 28, 21, 31), fill=1); px(d, 22, 30); px(d, 22, 31)

def arms_down(d):
    # short puff-sleeve stubs at the shoulders (part of the silhouette)
    d.polygon([(11, 3), (7, 12), (12, 10)], fill=1)
    d.polygon([(20, 3), (24, 12), (19, 10)], fill=1)

def arms_up(d):
    # arms raised in a cheer, with little round hands
    d.line((11, 4, 7, 0), fill=1); d.line((12, 4, 8, 0), fill=1)
    d.ellipse((5, 0, 8, 3), fill=1)
    d.line((20, 4, 24, 0), fill=1); d.line((19, 4, 23, 0), fill=1)
    d.ellipse((23, 0, 26, 3), fill=1)

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

# ---- name plate: あやめ (Ayame, "iris") in the zpix pixel font ----
NAME_TEXT = "あやめ"

def _find_font():
    import os, glob
    p = os.environ.get("NAME_FONT")
    if p and os.path.exists(p):
        return p
    for pat in ("/nix/store/*zpix*.ttf", "/nix/store/*zpix*/**/*.ttf"):
        hits = glob.glob(pat, recursive=True)
        if hits:
            return hits[0]
    raise SystemExit("zpix font not found; run in nix-shell -p zpix-pixel-font or set NAME_FONT")

def name_image(size=10):
    from PIL import ImageFont
    f = ImageFont.truetype(_find_font(), size)
    bbox = ImageDraw.Draw(Image.new("1", (1, 1))).textbbox((0, 0), NAME_TEXT, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    img = Image.new("1", (W, th + 2), 0)
    ImageDraw.Draw(img).text(((W - tw) // 2 - bbox[0], 1 - bbox[1]), NAME_TEXT, font=f, fill=1)
    return img

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

def figure(mood):
    """Compose the full standing figure for a mood (head over body)."""
    combo = Image.new("1", (W, H + BH), 0)
    combo.paste(dict(HEADS)[mood], (0, 0))
    combo.paste(dict(BODIES)["cheer" if mood == "excited" else "idle"], (0, H))
    return combo

def panel(mood, nimg):
    """The full 32x128 OLED panel: figure centred with the name plate beneath."""
    fig_h = H + BH
    gap = 4
    group = fig_h + gap + nimg.height
    top = (128 - group) // 2
    pnl = Image.new("1", (W, 128), 0)
    pnl.paste(figure(mood), (0, top))
    pnl.paste(nimg, (0, top + fig_h + gap))
    return pnl

def render_png(path, scale=6):
    """Each mood shown as the real 32x128 panel (white on black), upscaled."""
    from PIL import ImageFont
    moods = [n for n, _ in HEADS]
    nimg = name_image()
    pad, label_h = 14, 18
    pw, ph = W * scale, 128 * scale
    sheet = Image.new("RGB", (len(moods) * (pw + pad) + pad, ph + label_h + pad), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
    for i, mood in enumerate(moods):
        big = panel(mood, nimg).convert("L").resize((pw, ph), Image.NEAREST).convert("RGB")
        x = pad + i * (pw + pad)
        d.rectangle((x - 1, label_h - 1, x + pw, label_h + ph), outline=(70, 70, 80))
        sheet.paste(big, (x, label_h))
        d.text((x, 2), mood, fill=(220, 200, 240), font=font)
    sheet.save(path)
    print(f"wrote {path} ({sheet.size[0]}x{sheet.size[1]})")

if "--png" in sys.argv:
    render_png(sys.argv[sys.argv.index("--png") + 1] if len(sys.argv) > sys.argv.index("--png") + 1 else "avatar_preview.png")
elif "--emit" in sys.argv:
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
    nm = name_image()
    nd = pack(nm)
    print(f"// name plate: {NAME_TEXT} (Ayame = iris)")
    print(f"#define NAME_W {nm.width}")
    print(f"#define NAME_H {nm.height}")
    print(f"static const uint8_t PROGMEM avatar_name[{len(nd)}] = {{ {', '.join(f'0x{b:02X}' for b in nd)} }};")
    print(f"// total sprite bytes: {sum(len(pack(i)) for _, i in ALL) + len(nd)}")
else:
    # stack each head over the idle body for a full-figure preview
    for hn, himg in HEADS:
        combo = Image.new("1", (W, H + BH), 0)
        combo.paste(himg, (0, 0))
        bimg = dict(BODIES)["cheer" if hn == "excited" else "idle"]
        combo.paste(bimg, (0, H))
        preview(hn, combo)
    print(f"total sprite bytes: {sum(len(pack(i)) for _, i in ALL)}")
