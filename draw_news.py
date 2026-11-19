#!/usr/bin/env python3
"""Draw the news-image entry for 19 November 2026.

A one-page newspaper front page, 1024x1024, built only from stories
verified from live reporting on the day itself (BBC, Reuters, AP,
The Hindu, New York Times, Wall Street Journal). Run: python3 draw_news.py
Writes entry.png next to this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 38, 30)
NAVY = (31, 56, 100)
TEAL = (14, 94, 94)
GOLD = (176, 132, 30)
GREY = (90, 88, 80)
PANEL = (255, 255, 255)
LINE = (200, 194, 178)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=1.28):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def headline(draw, x, y, text, fnt, max_w, fill=INK, leading=1.08):
    return text_block(draw, x, y, text, fnt, max_w, fill=fill, leading=leading)


def kicker(draw, x, y, text, color=RED):
    fnt = font(F_SANS_B, 21)
    draw.text((x, y), text.upper(), font=fnt, fill=color)
    return y + 30


def panel(draw, x, y, w, h, fill=PANEL):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill,
                           outline=LINE, width=2)


def draw_burning_tanker(draw, x, y, w, h):
    """A tanker on a grey sea, smoke and flames rising from its deck."""
    sky = (224, 228, 232)
    draw.rectangle([x, y, x + w, y + h], fill=sky)
    # smoke columns
    for sx, sy, sr in ((x + w * 0.32, y + 34, 26), (x + w * 0.52, y + 22, 32),
                       (x + w * 0.68, y + 44, 22)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 118))
        draw.ellipse([sx - sr + 10, sy - sr - 12, sx + sr + 10, sy + sr - 12],
                     fill=(150, 150, 148))
    # sea
    draw.rectangle([x, y + h - 40, x + w, y + h], fill=(52, 96, 138))
    for i in range(4):
        wx = x + 16 + i * 86
        draw.arc([wx, y + h - 30, wx + 52, y + h - 12], 0, 180,
                 fill=(255, 255, 255), width=3)
    # hull
    hy = y + h - 78
    draw.polygon([(x + 14, hy), (x + w - 14, hy),
                  (x + w - 40, y + h - 40), (x + 40, y + h - 40)],
                 fill=(148, 38, 28))
    # containers
    for i, col in enumerate(((214, 172, 58), (58, 118, 88), (180, 90, 40))):
        cx0 = x + 34 + i * 62
        draw.rectangle([cx0, hy - 34, cx0 + 56, hy - 2], fill=col,
                       outline=(60, 60, 60), width=2)
    # funnel
    draw.rectangle([x + w - 66, hy - 52, x + w - 36, hy - 2],
                   fill=(240, 240, 240), outline=(90, 90, 90), width=2)
    # flames above the middle container
    fx, fy = x + w // 2 - 10, hy - 34
    draw.polygon([(fx, fy), (fx + 14, fy - 34), (fx + 30, fy - 10),
                  (fx + 44, fy - 40), (fx + 58, fy)],
                 fill=(240, 140, 30), outline=(200, 80, 10))
    draw.polygon([(fx + 16, fy), (fx + 26, fy - 22), (fx + 40, fy)],
                 fill=(245, 200, 60))


def draw_vice_city(draw, x, y, w, h):
    """A neon Vice City skyline at dusk: towers, sunset, palm tree."""
    # dusk gradient bands
    bands = [(255, 120, 140), (255, 90, 160), (150, 60, 180), (60, 30, 110)]
    bh = h // 4
    for i, col in enumerate(bands):
        draw.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=col)
    # sun
    cx, cy = x + w // 2, y + h // 2 - 6
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(255, 220, 120))
    # skyline silhouettes
    towers = [(0, 90), (52, 130), (108, 70), (160, 120), (216, 84), (268, 140)]
    base = y + h - 30
    for tx, th in towers:
        draw.rectangle([x + tx, base - th, x + tx + 44, base], fill=(28, 14, 48))
        for wy in range(base - th + 12, base - 10, 18):
            for wx in (x + tx + 8, x + tx + 24):
                draw.rectangle([wx, wy, wx + 8, wy + 8], fill=(255, 220, 90))
    # sea strip
    draw.rectangle([x, base, x + w, y + h], fill=(20, 60, 110))
    draw.line([x, base, x + w, base], fill=(255, 120, 180), width=3)
    # palm tree
    px, py = x + 22, base - 6
    draw.line([px, py, px + 4, py - 52], fill=(30, 60, 30), width=5)
    for ang in (200, 235, 270, 305, 340):
        a = math.radians(ang)
        ex, ey = px + 4 + 26 * math.cos(a), py - 52 + 14 * math.sin(a)
        draw.line([px + 4, py - 52, ex, ey], fill=(40, 130, 60), width=4)
    # neon sign on the sea strip, drawn last so the towers never cover it
    draw.text((x + 30, y + h - 27), "VICE CITY", font=font(F_SANS_B, 20),
              fill=(255, 240, 120))


def draw_capitol(draw, x, y, w, h):
    """The US Capitol dome in navy and white."""
    draw.rectangle([x, y, x + w, y + h], fill=(222, 232, 244))
    cx = x + w // 2
    base = y + h - 6
    # steps and base
    draw.rectangle([x + 22, base - 12, x + w - 22, base], fill=(200, 205, 210))
    draw.rectangle([x + 34, base - 26, x + w - 34, base - 12], fill=(225, 228, 232))
    # columns
    for i in range(5):
        col_x = x + 52 + i * 26
        draw.rectangle([col_x, base - 78, col_x + 12, base - 26],
                       fill=(245, 245, 240), outline=(140, 140, 135), width=2)
    # entablature
    draw.rectangle([x + 40, base - 92, x + w - 40, base - 78], fill=(235, 235, 230))
    # dome
    draw.pieslice([cx - 48, base - 136, cx + 48, base - 84], 180, 360,
                  fill=(240, 240, 235), outline=(120, 120, 115), width=2)
    draw.rectangle([cx - 3, base - 142, cx + 3, base - 136], fill=(120, 120, 115))
    draw.ellipse([cx - 7, base - 150, cx + 7, base - 136], fill=(200, 170, 60))
    # flag
    draw.line([cx, base - 150, cx, base - 158], fill=(90, 90, 90), width=2)
    draw.polygon([(cx, base - 158), (cx + 18, base - 153), (cx, base - 148)],
                 fill=(179, 38, 30))
    # stars
    for sx, sy in ((x + 20, y + 18), (x + w - 28, y + 24), (x + 34, y + 52)):
        draw.text((sx, sy), "*", font=font(F_SANS_B, 22), fill=(31, 56, 100))


def draw_voyager(draw, x, y, w, h):
    """Voyager 1: a probe with its dish, drifting past stars."""
    draw.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    # stars
    for sx, sy, r in ((x + 18, y + 16, 2), (x + 52, y + 40, 1), (x + w - 24, y + 20, 2),
                      (x + w - 60, y + 58, 1), (x + 30, y + 76, 1), (x + w - 40, y + 92, 2),
                      (x + 70, y + 14, 1), (x + w - 80, y + 44, 1)):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # distant sun
    draw.ellipse([x + w - 34, y + h - 40, x + w - 14, y + h - 20],
                 fill=(255, 230, 140))
    # dish
    cx, cy = x + w // 2, y + h // 2 - 6
    draw.pieslice([cx - 34, cy - 26, cx + 34, cy + 42], 180, 360,
                  fill=(210, 215, 220), outline=(160, 165, 170), width=2)
    # body
    draw.rectangle([cx - 26, cy + 8, cx + 26, cy + 30], fill=(150, 155, 165),
                   outline=(110, 115, 125), width=2)
    # boom and RTG
    draw.line([cx + 26, cy + 18, cx + 62, cy + 18], fill=(200, 200, 200), width=3)
    draw.rectangle([cx + 62, cy + 10, cx + 76, cy + 26], fill=(90, 90, 100))
    # signal waves to Earth
    for r in (48, 62, 76):
        draw.arc([cx - r, cy - r + 10, cx + r, cy + r + 10], 200, 340,
                 fill=(120, 200, 255), width=3)
    # tiny Earth
    draw.ellipse([x + 16, y + h - 34, x + 34, y + h - 16], fill=(80, 140, 190),
                 outline=(255, 255, 255), width=1)


def draw_cyclone(draw, x, y, w, h):
    """A spiral storm over a dark sea, rain bands curling in."""
    draw.rectangle([x, y, x + w, y + h], fill=(210, 224, 238))
    cx, cy = x + w // 2, y + h // 2 + 4
    for turn in range(3):
        r0 = 10 + turn * 16
        for a in range(0, 300, 6):
            ang = math.radians(a + turn * 40)
            r = r0 + a * 0.10
            px = cx + r * math.cos(ang)
            py = cy + r * math.sin(ang) * 0.85
            draw.ellipse([px - 5, py - 5, px + 5, py + 5],
                         fill=(40, 80, 140) if turn < 2 else (90, 130, 180))
    draw.ellipse([cx - 14, cy - 12, cx + 14, cy + 12], fill=(240, 240, 235))
    # coastline at the bottom
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(214, 190, 140))
    draw.line([x, y + h - 26, x + w, y + h - 26], fill=(120, 100, 60), width=2)
    # rain streaks
    for i in range(6):
        rx = x + 18 + i * 30
        draw.line([rx, y + 14, rx - 8, y + 34], fill=(120, 150, 190), width=3)


def draw_summit(draw, x, y, w, h):
    """Three flags over a table: the Shenzhen trilateral."""
    draw.rectangle([x, y, x + w, y + h], fill=(236, 232, 222))
    # skyline hint
    draw.rectangle([x, y + h - 52, x + w, y + h], fill=(190, 185, 170))
    for tx, th in ((16, 40), (58, 64), (104, 48), (150, 70), (200, 44), (244, 60)):
        draw.rectangle([x + tx, y + h - 52 - th, x + tx + 30, y + h - 52],
                       fill=(120, 115, 100))
    # table
    draw.rectangle([x + 24, y + h - 96, x + w - 24, y + h - 84], fill=(120, 70, 50))
    draw.rectangle([x + 34, y + h - 84, x + w - 34, y + h - 80], fill=(90, 50, 35))
    # three flags on poles
    flags = [((179, 38, 30), (255, 255, 255)),   # red
             ((31, 56, 100), (255, 255, 255)),   # navy
             ((14, 94, 94), (255, 220, 90))]     # teal/gold
    for i, (col, star) in enumerate(flags):
        fx = x + 52 + i * 100
        draw.line([fx, y + 18, fx, y + 108], fill=(90, 90, 90), width=3)
        draw.rectangle([fx, y + 18, fx + 62, y + 52], fill=col,
                       outline=(60, 60, 60), width=2)
        draw.text((fx + 8, y + 24), "*", font=font(F_SANS_B, 22), fill=star)
    # handshake above the table
    hx, hy = x + w // 2, y + h - 66
    draw.ellipse([hx - 26, hy - 10, hx + 26, hy + 10], fill=(240, 200, 160),
                 outline=(120, 80, 40), width=2)
    draw.line([hx - 26, hy, hx - 44, hy - 12], fill=(240, 200, 160), width=6)
    draw.line([hx + 26, hy, hx + 44, hy - 12], fill=(220, 180, 140), width=6)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- Masthead ----
    d.text((M, 22), "THE WORLD IN ONE DAY", font=font(F_SERIF, 58), fill=INK)
    d.line([M, 96, W - M, 96], fill=INK, width=4)
    d.line([M, 102, W - M, 102], fill=INK, width=2)
    d.text((M, 112), "THURSDAY, 19 NOVEMBER 2026",
           font=font(F_SANS_B, 26), fill=RED)
    right_label = "SIX STORIES  •  EVERY REGION"
    rl_font = font(F_SANS_B, 20)
    d.text((W - M - d.textlength(right_label, font=rl_font), 114),
           right_label, font=rl_font, fill=GREY)

    # ---- Lead story: Gulf war widens ----
    x, y, w, h = M, 158, W - 2 * M, 296
    panel(d, x, y, w, h)
    tx = x + 24
    ty = y + 16
    ty = kicker(d, tx, ty, "Middle East — US-Iran war")
    ty = headline(d, tx, ty, "THE GULF WAR WIDENS",
                  font(F_SERIF, 46), 540, leading=1.05)
    ty += 6
    ty = text_block(d, tx, ty,
                    "US jets hit a Guards missile site on Qeshm Island "
                    "on Tuesday. Iran answered with drones aimed at US "
                    "bases in Kuwait and Bahrain. Three carriers moved "
                    "in as tankers burned in the Strait of Hormuz.",
                    font(F_SANS, 22), 540)
    draw_burning_tanker(d, x + w - 392, y + 16, 368, h - 32)

    # ---- Row 2: two stories ----
    y2, h2 = 470, 232
    w2 = (W - 2 * M - 16) // 2
    # GTA VI
    panel(d, M, y2, w2, h2)
    tx = M + 18
    ty = kicker(d, tx, y2 + 12, "Culture — Gaming", color=TEAL)
    ty = headline(d, tx, ty, "VICE CITY AT LAST",
                  font(F_SERIF, 25), w2 - 206, leading=1.05)
    ty += 4
    text_block(d, tx, ty,
               "Grand Theft Auto VI rolls out worldwide today after a "
               "13-year wait, returning players to neon Vice City on "
               "PS5 and Xbox. Early reviews put it at 99 on Metacritic.",
               font(F_SANS, 17), w2 - 206)
    draw_vice_city(d, M + w2 - 180, y2 + 52, 168, h2 - 68)
    # Jeffries
    x3 = M + w2 + 16
    panel(d, x3, y2, w2, h2)
    tx = x3 + 18
    ty = kicker(d, tx, y2 + 12, "America — Politics", color=NAVY)
    ty = headline(d, tx, ty, "JEFFRIES MAKES HISTORY",
                  font(F_SERIF, 25), w2 - 206, leading=1.05)
    ty += 4
    text_block(d, tx, ty,
               "House Democrats nominated Hakeem Jeffries for Speaker "
               "by 251 votes to 11. If the full House confirms him in "
               "January, he will be the first Black Speaker in history.",
               font(F_SANS, 17), w2 - 206)
    draw_capitol(d, x3 + w2 - 180, y2 + 52, 168, h2 - 68)

    # ---- Row 3: three stories ----
    y3, h3 = 718, 196
    w3 = (W - 2 * M - 32) // 3
    stories = [
        ("Space — Voyager 1", "ONE LIGHT-DAY FROM HOME",
         "Voyager 1 crossed one light-day from Earth, 25.9 billion "
         "km out. A radio signal now takes a full day to reach it.",
         TEAL, draw_voyager),
        ("Asia — Weather", "AKVAN CLOSES IN",
         "Cyclone Akvan is set to cross the coast between "
         "Machilipatnam and Puri, with landfall expected on Friday.",
         RED, draw_cyclone),
        ("Asia — Diplomacy", "THREE LEADERS, ONE TABLE",
         "Trump, Xi and Putin are due to meet in Shenzhen at the APEC "
         "summit, the first trilateral of the three leaders.",
         NAVY, draw_summit),
    ]
    for i, (kick, head, body, col, icon) in enumerate(stories):
        px = M + i * (w3 + 16)
        panel(d, px, y3, w3, h3)
        tx = px + 16
        ty = kicker(d, tx, y3 + 12, kick, color=col)
        ty = headline(d, tx, ty, head, font(F_SERIF, 23), w3 - 32, leading=1.05)
        ty += 4
        text_block(d, tx, ty, body, font(F_SANS, 16), w3 - 32)

    # ---- Bottom strip ----
    y4 = 930
    d.rectangle([M, y4, W - M, y4 + 56], fill=NAVY)
    d.text((M + 16, y4 + 6), "ALSO TODAY:",
           font=font(F_SANS_B, 20), fill=(255, 210, 90))
    text_block(d, M + 170, y4 + 8,
               "ICJ to rule on Myanmar's Rohingya genocide case  •  "
               "Crimean Bridge hit again  •  Van Gogh sells for a "
               "record $190.4m  •  Nvidia's acting chief promises "
               "earlier pay rises",
               font(F_SANS, 18), W - 2 * M - 186, fill=(255, 255, 255))

    # ---- Footer ----
    foot = "Drawn from live reporting: BBC  •  Reuters  •  AP  •  The Hindu  •  NYT  •  WSJ"
    d.text((M, 996), foot, font=font(F_SANS, 15), fill=GREY)
    right = "make.fun  •  @raju-pramana"
    rf = font(F_SANS, 15)
    d.text((W - M - d.textlength(right, font=rf), 996), right, font=rf, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
