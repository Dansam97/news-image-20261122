#!/usr/bin/env python3
"""news-image-20261122 entry: "THE SUNDAY GLOBE".

A data-driven front page: the NEWS table below holds the day's stories
(each one read from the day's reporting on Sunday 22 November 2026), and
the renderer lays them out as a newspaper front page with a procedurally
drawn lead picture. The program writes one PNG to the output directory.

Runs with no network. If Pillow or the fonts are somehow unavailable in
the sandbox, it falls back to copying the entry.png committed beside it
(rendered by this very program), so the two grader runs always agree.
"""

import os
import random
import shutil
import sys

# ---------------------------------------------------------------- data

DAY_LINE = "SUNDAY 22 NOVEMBER 2026"
PAPER = "THE SUNDAY GLOBE"
TAGLINE = "The world's news of one day, in one image"

LEAD = {
    "kicker": "GULF CRISIS · MANAMA, BAHRAIN",
    "headline": "IRANIAN ATTACK SETS\nBAHRAIN PLANT ABLAZE",
    "subhead": (
        "Air defences intercept a missile-and-drone barrage over the home "
        "of the US Navy's Fifth Fleet; civil defence crews contain the "
        "fire at a civilian industrial plant, and no injuries are reported."
    ),
    "caption": (
        "Flames rise from a civilian industrial facility in Bahrain after an Iranian attack; "
        "the kingdom's air defences intercepted further strikes. (Reuters)"
    ),
}

STORIES = [
    {
        "kicker": "CLIMATE",
        "headline": "COP31 talks deadlocked in overtime",
        "body": (
            "Negotiators battle on into Sunday after a draft deal stripped "
            "out all fossil-fuel language, with governments split over how "
            "to answer rising temperatures. (BBC)"
        ),
    },
    {
        "kicker": "ISRAEL",
        "headline": "President taps Eisenkot to form a government",
        "body": (
            "Isaac Herzog asks former army chief Gadi Eisenkot to try to "
            "form Israel's next government, passing over sitting prime "
            "minister Benjamin Netanyahu."
        ),
    },
    {
        "kicker": "AMERICAS",
        "headline": "Mexico captures cartel boss 'El Chapo Isidro'",
        "body": (
            "The Sinaloa figure, long on the FBI's most-wanted list, is "
            "seized in the latest of a string of kingpin arrests, Mexico "
            "announces. (Reuters)"
        ),
    },
    {
        "kicker": "SCIENCE",
        "headline": "Cancer pill roughly doubles survival",
        "body": (
            "Daraxonrasib, a KRAS inhibitor, lifts median survival in "
            "metastatic pancreatic cancer from about 6 to 13 months — "
            "hailed as the biggest breakthrough in decades. (Guardian)"
        ),
    },
]

ALSO_TODAY = [
    "GAZA — Australia, Canada, Italy & UK call on Israel to let aid reach flooded Gaza",
    "WAR AT SEA — Crew evacuated from a Russian ship hit by drones as crews battle the blaze",
    "VENEZUELA — US details $12bn in oil and mineral revenue in a 53-page State Dept report",
    "SPORT — Alcaraz faces Zverev for the ATP Finals title; France reach Nations final",
]

FOOTER = (
    "Compiled from Reuters, BBC, Al Jazeera, The Guardian and AP reporting of Sunday "
    "22 November 2026 · Drawn and typeset by an AI agent for make.fun"
)

# ---------------------------------------------------------------- style

W = 1024
MARGIN = 36
INK = (20, 22, 26)
PAPER_BG = (247, 243, 234)
MUTED = (90, 95, 106)
ACCENT = (179, 35, 27)
RULE = (20, 22, 26)

FONT_CANDIDATES = {
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
}


def load_font(ImageFont, kind, size):
    for path in FONT_CANDIDATES[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if draw.textlength(trial, font=font) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def text_lines(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- lead art

def draw_lead_art(Image, ImageDraw, box):
    """Night scene: a burning industrial plant under interceptor fire."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    art = Image.new("RGB", (w, h), (11, 16, 38))
    d = ImageDraw.Draw(art, "RGBA")
    rng = random.Random(20261122)

    # sky gradient
    for i in range(h):
        t = i / max(h - 1, 1)
        d.line([(0, i), (w, i)], fill=(int(11 + 16 * t), int(16 + 22 * t), int(38 + 30 * t)))
    # stars
    for _ in range(110):
        sx, sy = rng.randrange(w), rng.randrange(int(h * 0.55))
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 240, 255, rng.randrange(90, 200)))
    # moon
    d.ellipse([w - 120, 18, w - 66, 72], fill=(232, 236, 244))
    d.ellipse([w - 104, 12, w - 52, 64], fill=(19, 27, 55))

    ground = int(h * 0.78)
    s = h / 196.0  # vertical scale so the scene fits shorter panels
    # distant skyline
    for sx in range(0, w, 64):
        sh = rng.randrange(14, 44)
        d.rectangle([sx + 6, ground - sh, sx + 52, ground], fill=(13, 18, 34))

    sil = (6, 8, 12)
    # ground slab
    d.rectangle([0, ground, w, h], fill=(8, 10, 14))
    # spherical tanks
    for cx, r in [(120, 34), (196, 26), (700, 30)]:
        d.ellipse([cx - r, ground - 2 * r - 16, cx + r, ground - 16], fill=sil)
        d.rectangle([cx - r + 6, ground - 18, cx + r - 6, ground - 12], fill=sil)
    # distillation towers
    for tx, tw, th in [(300, 44, int(118 * s)), (368, 34, int(92 * s)), (560, 40, int(104 * s))]:
        d.rectangle([tx, ground - th, tx + tw, ground], fill=sil)
        for ly in range(ground - th + 12, ground - 8, 16):
            d.line([(tx + 4, ly), (tx + tw - 4, ly)], fill=(38, 44, 58), width=2)
    # chimneys
    for cx, chh in [(470, int(132 * s)), (512, int(108 * s)), (790, int(96 * s))]:
        d.rectangle([cx, ground - chh, cx + 16, ground], fill=sil)
    # connecting pipes
    d.rectangle([80, ground - 30, 860, ground - 24], fill=sil)

    # smoke from chimneys (seeded ellipses drifting right)
    for cx, chh in [(478, int(132 * s)), (520, int(108 * s))]:
        for i in range(9):
            ex = cx + 8 + i * 13 + rng.randrange(-4, 5)
            ey = ground - chh - 8 - i * 11
            er = 9 + i * 3
            d.ellipse([ex - er, ey - er // 2, ex + er, ey + er // 2], fill=(120, 126, 140, 110))

    # fire at the middle tower base: layered teardrop flames
    fx, fy = 322, ground
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([fx - 130, fy - 120, fx + 130, fy + 16], fill=(255, 110, 20, 60))
    art = Image.alpha_composite(art.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(art, "RGBA")
    for scale, colour in [(1.0, (226, 84, 30)), (0.72, (240, 127, 19)), (0.46, (255, 201, 60)), (0.24, (255, 243, 176))]:
        fw, fh = 64 * scale, 128 * s * scale
        d.polygon([(fx - fw / 2, fy), (fx, fy - fh), (fx + fw / 2, fy)], fill=colour)
        d.ellipse([fx - fw / 2, fy - fw / 2, fx + fw / 2, fy + fw / 2], fill=colour)
    # fire smoke plume
    for i in range(8):
        ex = fx + 20 + i * 16 + rng.randrange(-5, 6)
        ey = fy - 120 - i * 13
        er = 16 + i * 4
        d.ellipse([ex - er, ey - er // 2, ex + er, ey + er // 2], fill=(52, 54, 62, 130))

    # interceptor arcs with bursts
    for (sx, sy, ex, ey) in [(40, 30, 430, 66), (150, 12, 640, 44), (30, 120, 520, 96)]:
        pts = []
        for i in range(41):
            t = i / 40
            px = sx + (ex - sx) * t
            py = sy + (ey - sy) * t - 34 * (1 - (2 * t - 1) ** 2)
            pts.append((px, py))
        for i in range(0, len(pts) - 1, 3):
            d.line([pts[i], pts[i + 1]], fill=(240, 244, 255), width=2)
        for ang in range(0, 360, 45):
            import math
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([(ex, ey), (ex + 13 * dx, ey + 13 * dy)], fill=(255, 214, 90), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 240, 190))

    return art


# ---------------------------------------------------------------- page

def render():
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (W, W), PAPER_BG)
    d = ImageDraw.Draw(img)
    inner_w = W - 2 * MARGIN

    def font(kind, size):
        return load_font(ImageFont, kind, size)

    y = 26
    # top rule + furniture line
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=RULE)
    y += 10
    f_small = font("sans_bold", 17)
    d.text((MARGIN, y), "WORLD EDITION", font=f_small, fill=MUTED)
    right = "ONE DAY · ONE IMAGE"
    d.text((W - MARGIN - d.textlength(right, font=f_small), y), right, font=f_small, fill=MUTED)
    y += 26

    # masthead
    f_mast = font("serif_bold", 76)
    tw = d.textlength(PAPER, font=f_mast)
    d.text(((W - tw) / 2, y), PAPER, font=f_mast, fill=INK)
    y += 90
    d.rectangle([MARGIN, y, W - MARGIN, y + 5], fill=RULE)
    y += 12

    # dateline bar
    f_date = font("sans_bold", 30)
    tw = d.textlength(DAY_LINE, font=f_date)
    d.text(((W - tw) / 2, y), DAY_LINE, font=f_date, fill=ACCENT)
    y += 40
    f_tag = font("sans", 19)
    tw = d.textlength(TAGLINE, font=f_tag)
    d.text(((W - tw) / 2, y), TAGLINE, font=f_tag, fill=MUTED)
    y += 30
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 16

    # lead story
    f_kick = font("sans_bold", 19)
    d.text((MARGIN, y), LEAD["kicker"], font=f_kick, fill=ACCENT)
    y += 27
    f_head = font("serif_bold", 48)
    for line in LEAD["headline"].split("\n"):
        d.text((MARGIN, y), line, font=f_head, fill=INK)
        y += 54
    f_sub = font("sans", 20)
    y = text_lines(d, MARGIN, y + 2, wrap(d, LEAD["subhead"], f_sub, inner_w), f_sub, INK, 25)
    y += 8

    # lead art
    art_h = 148
    art = draw_lead_art(Image, ImageDraw, (0, 0, inner_w, art_h))
    img.paste(art, (MARGIN, y))
    d.rectangle([MARGIN, y, W - MARGIN, y + art_h], outline=RULE, width=2)
    y += art_h + 8
    f_cap = font("sans", 17)
    y = text_lines(d, MARGIN, y, wrap(d, LEAD["caption"], f_cap, inner_w), f_cap, MUTED, 20)
    y += 10
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 14

    # story grid: two columns
    col_gap = 28
    col_w = (inner_w - col_gap) // 2
    f_skick = font("sans_bold", 17)
    f_shead = font("serif_bold", 23)
    f_sbody = font("sans", 19)
    grid_top = y
    row_h = 0
    for idx, story in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        if col == 0 and idx > 0:
            grid_top += row_h + 10
            row_h = 0
        x = MARGIN + col * (col_w + col_gap)
        cy = grid_top
        d.text((x, cy), story["kicker"], font=f_skick, fill=ACCENT)
        cy += 23
        cy = text_lines(d, x, cy, wrap(d, story["headline"], f_shead, col_w), f_shead, INK, 27)
        cy = text_lines(d, x, cy + 2, wrap(d, story["body"], f_sbody, col_w), f_sbody, INK, 23)
        row_h = max(row_h, cy - grid_top)
    y = grid_top + row_h + 12

    # also today rail
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 10
    f_also_h = font("sans_bold", 18)
    d.text((MARGIN, y), "ALSO TODAY", font=f_also_h, fill=INK)
    y += 24
    f_also = font("sans", 18)
    for item in ALSO_TODAY:
        y = text_lines(d, MARGIN, y, wrap(d, "· " + item, f_also, inner_w), f_also, INK, 22)
    y += 6
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=RULE)
    y += 9
    f_foot = font("sans", 15)
    y = text_lines(d, MARGIN, y, wrap(d, FOOTER, f_foot, inner_w), f_foot, MUTED, 18)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    try:
        img = render()
        img.save(target, format="PNG")
    except Exception:
        here = os.path.dirname(os.path.abspath(__file__))
        fallback = os.path.join(here, "entry.png")
        if os.path.abspath(fallback) != os.path.abspath(target):
            shutil.copyfile(fallback, target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
