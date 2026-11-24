#!/usr/bin/env python3
"""news-image-20261124: sum up Tuesday 24 November 2026 world news in one image.

Draws a 1024x1024 newspaper-style front page with PIL only: masthead,
four illustrated news panels (2x2) and a ticker of the day's other stories.
Deterministic: no network, no clock, no randomness. Writes entry.png to
$MAKEFUN_OUTPUT_DIR (default /output).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

# --- palette ---
PAPER = (247, 243, 236)
INK = (24, 24, 24)
MUTED = (90, 86, 78)
RULE = (24, 24, 24)
WHITE = (255, 255, 255)
GREEN = (27, 122, 61)
GREEN_DK = (18, 84, 42)
NAVY = (20, 48, 77)
NAVY_DK = (12, 32, 54)
ORANGE = (179, 74, 18)
ORANGE_DK = (128, 50, 10)
MAROON = (122, 31, 31)
MAROON_DK = (84, 20, 20)
GOLD = (212, 160, 32)
SKY = (214, 228, 240)
SEA = (38, 92, 130)
SEA_DK = (24, 64, 96)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def font(bold, serif, size):
    name = "DejaVuSerif-Bold.ttf" if (serif and bold) else \
        "DejaVuSerif.ttf" if serif else \
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in ("/usr/share/fonts/truetype/dejavu/",
                 "/usr/share/fonts/truetype/liberation/",
                 "/usr/share/fonts/truetype/noto/"):
        p = base + name
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font(True, True, s)
SANS_B = lambda s: font(True, False, s)
SANS = lambda s: font(False, False, s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def flame(draw, cx, cy, s, colors=((255, 190, 40), (240, 110, 20), (200, 40, 10))):
    # simple layered flame: three stacked ellipses + tip
    draw.ellipse([cx - s * 0.55, cy - s * 0.35, cx + s * 0.55, cy + s * 0.55], fill=colors[2])
    draw.ellipse([cx - s * 0.42, cy - s * 0.55, cx + s * 0.42, cy + s * 0.35], fill=colors[1])
    draw.ellipse([cx - s * 0.26, cy - s * 0.75, cx + s * 0.26, cy + s * 0.15], fill=colors[0])


def smoke(draw, x, y, s, color=(110, 108, 102)):
    # tight column of overlapping puffs rising from a roof point (x, y)
    for i, r in enumerate((s, s * 0.85, s * 0.7)):
        cx = x + (i % 2) * s * 0.3
        cy = y - i * s * 0.65
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


# --- panel illustrations (each draws inside its own box) ---
def ill_nvidia(draw, x, y, w, h):
    # green chip on a light board + big +31% badge
    draw.rectangle([x, y, x + w, y + h], fill=(232, 244, 233))
    # circuit traces
    for tx in (x + 30, x + 90, x + 150):
        draw.line([tx, y + 12, tx, y + h - 12], fill=(170, 205, 175), width=3)
    for ty in (y + 24, y + 60, y + 96):
        draw.line([x + 14, ty, x + w - 170, ty], fill=(170, 205, 175), width=3)
    # chip
    cx, cy, cs = x + 72, y + 12, 88
    for i in range(4):
        px = cx + 14 + i * 21
        draw.line([px, cy - 8, px, cy], fill=GREEN_DK, width=5)
        draw.line([px, cy + cs, px, cy + cs + 8], fill=GREEN_DK, width=5)
        py = cy + 14 + i * 21
        draw.line([cx - 8, py, cx, py], fill=GREEN_DK, width=5)
        draw.line([cx + cs, py, cx + cs + 8, py], fill=GREEN_DK, width=5)
    draw.rounded_rectangle([cx, cy, cx + cs, cy + cs], radius=8, fill=GREEN)
    draw.rounded_rectangle([cx + 14, cy + 14, cx + cs - 14, cy + cs - 14], radius=5,
                           outline=WHITE, width=3)
    nv = "NVDA"
    draw.text((cx + (cs - draw.textlength(nv, font=SANS_B(17))) / 2, cy + 34),
              nv, font=SANS_B(17), fill=WHITE)
    # badge
    bx, by = x + w - 168, y + 18
    draw.rounded_rectangle([bx, by, bx + 140, by + 82], radius=12, fill=GREEN_DK)
    draw.text((bx + 18, by + 8), "+31%", font=SANS_B(34), fill=WHITE)
    draw.text((bx + 18, by + 50), "IN ONE DAY", font=SANS_B(15), fill=(190, 230, 198))


def ill_warship(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun, top-left of the sky so it never collides with the drones
    draw.ellipse([x + 14, y + 10, x + 58, y + 54], fill=(250, 226, 150))
    draw.rectangle([x, y + 96, x + w, y + h], fill=SEA)
    for wy in (y + 104, y + 112):
        draw.line([x + 10, wy, x + w - 10, wy], fill=(120, 170, 205), width=2)
    # corvette silhouette
    hx, hy = x + 120, y + 78
    draw.polygon([(hx, hy), (hx + 220, hy), (hx + 196, hy + 26), (hx + 22, hy + 26)],
                 fill=(40, 44, 48))
    draw.rectangle([hx + 78, hy - 26, hx + 128, hy], fill=(40, 44, 48))
    draw.line([hx + 102, hy - 52, hx + 102, hy - 26], fill=(40, 44, 48), width=5)
    draw.polygon([(hx + 102, hy - 52), (hx + 126, hy - 40), (hx + 102, hy - 34)], fill=(40, 44, 48))
    # explosion starburst on the hull
    ex, ey = hx + 176, hy - 6
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 10, 30
        a = math.radians(ang)
        draw.line([ex + r1 * math.cos(a), ey + r1 * math.sin(a),
                   ex + r2 * math.cos(a), ey + r2 * math.sin(a)], fill=GOLD, width=5)
    draw.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(255, 120, 20))
    # seven naval drones as dots with wakes, top right
    for i in range(7):
        dx, dy = x + w - 150 + (i % 4) * 34, y + 16 + (i // 4) * 26
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=NAVY_DK)
        draw.line([dx - 22, dy, dx - 8, dy], fill=NAVY_DK, width=2)


def ill_hormuz(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(243, 228, 205))
    # land masses left/right, strait channel in the middle
    draw.polygon([(x, y), (x + 150, y), (x + 118, y + h), (x, y + h)], fill=(214, 190, 150))
    draw.polygon([(x + w, y), (x + w - 150, y), (x + w - 118, y + h), (x + w, y + h)],
                 fill=(214, 190, 150))
    draw.polygon([(x + 150, y), (x + w - 150, y), (x + w - 118, y + h), (x + 118, y + h)],
                 fill=(96, 150, 190))
    # three tankers in the strait
    for i, ty in enumerate((y + 14, y + 50, y + 86)):
        tx = x + 178 + (i % 2) * 26
        draw.rectangle([tx, ty, tx + 104, ty + 20], fill=(60, 60, 60))
        draw.rectangle([tx + 8, ty + 5, tx + 96, ty + 15], fill=(200, 60, 40))
        draw.rectangle([tx + 88, ty - 7, tx + 100, ty + 4], fill=(60, 60, 60))
    # flames over the tankers + spiked mines
    flame(draw, x + 300, y + 26, 24)
    flame(draw, x + 236, y + 96, 20)
    for mx, my in ((x + 196, y + 44), (x + 322, y + 72), (x + 252, y + 104)):
        draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(30, 30, 30))
        for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12), (-8, -8), (8, 8), (-8, 8), (8, -8)):
            draw.line([mx, my, mx + dx, my + dy], fill=(30, 30, 30), width=2)


def ill_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 226, 214))
    # dusk sky band
    draw.rectangle([x, y, x + w, y + 52], fill=(226, 196, 160))
    draw.ellipse([x + w - 84, y + 10, x + w - 44, y + 50], fill=(250, 220, 170))
    # skyline: intact + broken buildings
    base = y + h
    buildings = [(x + 8, 76, 46), (x + 62, 96, 52), (x + 122, 62, 44), (x + 174, 92, 56),
                 (x + 238, 70, 48), (x + 294, 100, 54), (x + 356, 80, 50), (x + 414, 56, 40)]
    for bx, bh, bw in buildings:
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(74, 66, 60))
    # broken tops (jagged) on two buildings
    draw.polygon([(x + 122, base - 62), (x + 138, base - 76), (x + 150, base - 66),
                  (x + 166, base - 62)], fill=(74, 66, 60))
    draw.polygon([(x + 294, base - 100), (x + 312, base - 114), (x + 330, base - 102),
                  (x + 348, base - 100)], fill=(74, 66, 60))
    # lit windows
    for wx, wy in ((x + 20, base - 62), (x + 76, base - 78), (x + 250, base - 56),
                   (x + 368, base - 66), (x + 426, base - 44)):
        draw.rectangle([wx, wy, wx + 8, wy + 10], fill=GOLD)
    # smoke columns (anchored low enough to stay inside the illustration box)
    smoke(draw, x + 130, base - 66, 10)
    smoke(draw, x + 306, base - 100, 10)


PANELS = [
    dict(kicker="TECH  •  MARKETS", place="SANTA CLARA, USA", color=GREEN, dk=GREEN_DK,
         ill=ill_nvidia,
         head="HUANG IS BACK AT NVIDIA",
         body="Nvidia reinstates Jensen Huang as chief executive, a day after Donald Trump pressed its board. Shares jump 31% in a day and the S&P 500 rises 4.73%."),
    dict(kicker="WAR IN UKRAINE  •  AT SEA", place="BENGHAZI, LIBYA", color=NAVY, dk=NAVY_DK,
         ill=ill_warship,
         head="UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         body="President Zelenskyy confirms seven naval drones sank the corvette Merkury at Benghazi. A Russian cargo ship was also hit; the UN mission in Libya calls for an independent probe."),
    dict(kicker="IRAN  •  ENERGY", place="STRAIT OF HORMUZ", color=ORANGE, dk=ORANGE_DK,
         ill=ill_hormuz,
         head="THREE TANKERS HIT MINES IN THE STRAIT",
         body="Iran says three tankers caught fire after hitting mines in the Strait of Hormuz. Tehran refuses talks until its seven conditions are met amid the US naval blockade."),
    dict(kicker="ISRAEL–HAMAS WAR", place="GAZA", color=MAROON, dk=MAROON_DK,
         ill=ill_gaza,
         head="STRIKES KILL HAMAS SECURITY CHIEF",
         body="Israeli strikes kill Hamas internal security chief Naeem Abu Nahel and six others in Gaza, medics say. The UN says the war has undone 77 years of human development."),
]

TICKER_1 = "ALSO TODAY  •  UK sanctions 5 Myanmar generals after the ICJ genocide ruling"
TICKER_2 = "COP31 ends with no deal on fossil fuels  •  Zaporizhzhia: 2 killed, 40 wounded, incl. 4 children"
TICKER_3 = "US loses measles-free status after 25 years  •  Indonesia factory fire kills 26"


def draw_panel(draw, px, py, pw, ph, p):
    draw.rectangle([px, py, px + pw, py + ph], fill=WHITE, outline=(200, 194, 182), width=2)
    # kicker bar
    draw.rectangle([px, py, px + pw, py + 36], fill=p["color"])
    draw.text((px + 12, py + 8), p["kicker"], font=SANS_B(15), fill=WHITE)
    pw_place = draw.textlength(p["place"], font=SANS_B(14))
    draw.text((px + pw - 12 - pw_place, py + 9), p["place"], font=SANS_B(14),
              fill=(225, 225, 225))
    # illustration
    ix, iy, iw, ih = px + 12, py + 48, pw - 24, 118
    p["ill"](draw, ix, iy, iw, ih)
    draw.rectangle([ix, iy, ix + iw, iy + ih], outline=(200, 194, 182), width=1)
    # headline
    hy = iy + ih + 12
    hy = draw_text_block(draw, px + 14, hy, p["head"], SERIF_B(27), INK, pw - 28, 32)
    # body
    draw_text_block(draw, px + 14, hy + 4, p["body"], SANS(18), (52, 50, 46), pw - 28, 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # masthead
    title = "THE WORLD IN ONE IMAGE"
    tw = draw.textlength(title, font=SERIF_B(56))
    draw.text(((W - tw) / 2, 22), title, font=SERIF_B(56), fill=INK)
    sub = "TUESDAY, 24 NOVEMBER 2026  •  WORLD NEWS IN ONE PICTURE"
    sw = draw.textlength(sub, font=SANS_B(19))
    draw.text(((W - sw) / 2, 92), sub, font=SANS_B(19), fill=MUTED)
    draw.line([28, 126, W - 28, 126], fill=RULE, width=3)
    draw.line([28, 132, W - 28, 132], fill=RULE, width=1)
    # 2x2 grid
    gx, gy, gap = 28, 148, 16
    pw, ph = (W - 2 * gx - gap) // 2, 348
    for i, p in enumerate(PANELS):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        draw_panel(draw, px, py, pw, ph, p)
    # ticker
    ty = gy + 2 * ph + gap + 16
    draw.rectangle([28, ty, W - 28, ty + 84], fill=NAVY_DK)
    draw.text((44, ty + 7), TICKER_1, font=SANS_B(15), fill=WHITE)
    draw.text((44, ty + 32), TICKER_2, font=SANS_B(15), fill=(200, 214, 230))
    draw.text((44, ty + 57), TICKER_3, font=SANS_B(15), fill=(200, 214, 230))
    # footer
    foot = "Sources: Reuters  •  AP  •  BBC  •  The Guardian  •  One Turn  —  Tuesday 24 November 2026"
    fw = draw.textlength(foot, font=SANS(15))
    draw.text(((W - fw) / 2, ty + 94), foot, font=SANS(15), fill=MUTED)
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
