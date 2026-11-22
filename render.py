#!/usr/bin/env python3
"""Render the front page for news-image-20261122.

Draws a dense newspaper front page for Sunday, 22 November 2026 with
Pillow only (no network, no downloaded assets). Every headline and figure
comes from RESEARCH.md in this directory: 34 items (lead + 33 stories)
across Europe, the Middle East, Africa, the Americas, Asia-Pacific,
business/tech, science, weather and sport. Attributed claims stay worded
as claims. Deterministic: same input bytes produce the same PNG bytes.

Usage:  python3 render.py            # writes entry.png next to this file
        python3 render.py --verbose  # also prints size + sha256
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (22, 21, 19)
RED = (160, 30, 30)
GREY = (90, 86, 78)
RULE = (120, 112, 96)
SPECKLE = (214, 206, 188)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_B = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SERIF = str(FONT_DIR / "DejaVuSerif.ttf")
SERIF_I = str(FONT_DIR / "DejaVuSerif.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")
SANS_B = str(FONT_DIR / "DejaVuSans-Bold.ttf")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, width: int,
         max_lines: int | None = None) -> list[str]:
    """Greedy word wrap by pixel width; raises if it cannot fit."""
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"needs {len(lines)} lines (max {max_lines}): {text!r}")
    return lines


# ---------------------------------------------------------------- stories
# (section, headline, one-line summary). Headlines are capped at 2 lines
# at 14pt in a 301px column; summaries at 1 line at 12pt.

COL1: list[tuple[str, str, str]] = [
    ("WAR IN UKRAINE",
     "Kremlin claims 5,000 Ukrainian troops trapped east of Oskil River",
     "Moscow's claim; Kyiv has not confirmed."),
    ("WAR IN UKRAINE",
     "Russia claims five more settlements captured",
     "Villages named in Donetsk and Dnipropetrovsk."),
    ("WAR IN UKRAINE",
     "Russian strikes kill two and injure 83 across Ukraine",
     "Kryvyi Rih toll rises to 42 after double-tap hit."),
    ("MIDDLE EAST",
     "Israeli strikes kill at least four in Gaza despite ceasefire",
     "Drone hits a World Central Kitchen aid vehicle."),
    ("MIDDLE EAST",
     "IDF begins \u201cShield and Storm\u201d drill in the south",
     "Rehearses defence against surprise attack."),
    ("MIDDLE EAST",
     "Lebanon marks 83rd Independence Day",
     "No parade this year; offices close Monday."),
    ("EUROPE",
     "Georgia mourns six killed in Tbilisi blast",
     "Victims of the 19 Nov gas blast, two children."),
    ("EUROPE",
     "Cost-of-living protests enter third day",
     "France holds its sixth Saturday of marches."),
]

COL2: list[tuple[str, str, str]] = [
    ("AFRICA",
     "South Africa lowers flags for Mlambo-Ngcuka",
     "Flags at half-mast until the funeral on 28 Nov."),
    ("AFRICA",
     "Aswan Forum closes in Egypt",
     "AU forum on peace and development ends in Aswan."),
    ("AFRICA",
     "Nigeria to sign digital-services deal with five states",
     "Pact to ease cross-border digital trade."),
    ("AMERICAS",
     "Trump downplays FBI crime-database breach",
     "Dismisses the apparent breach in a Fox call."),
    ("AMERICAS",
     "Mexico captures \u201cEl Chapo Isidro\u201d in Sinaloa raid",
     "FBI Top 10 fugitive seized; 11 dead in clashes."),
    ("AMERICAS",
     "Storm kills three in southern Brazil",
     "114 km/h winds damage 8,000 homes in Tupanciret\u00e3."),
    ("AMERICAS",
     "Canada sees no change in US military ties",
     "Forces still work \u201chand in glove\u201d, minister says."),
    ("AMERICAS",
     "Republicans urge Trump to step back after midterm losses",
     "Nine Senate seats and 42 in the House lost."),
]

COL3: list[tuple[str, str, str]] = [
    ("ASIA-PACIFIC",
     "China\u2019s vice-premier begins Singapore visit",
     "20+ agreements expected from bilateral council."),
    ("ASIA-PACIFIC",
     "Nepal PM arrives in India on first foreign trip",
     "Two-day state visit; talks with Modi due Monday."),
    ("ASIA-PACIFIC",
     "India on top in Wellington Test",
     "KL Rahul hits 136; Nicholls 175 not out."),
    ("ASIA-PACIFIC",
     "Cricketer Chahal joins BJP",
     "Named special invitee to the OBC Morcha executive."),
    ("ASIA-PACIFIC",
     "Heavy snow isolates Fukushima village",
     "372 households cut off; 52 cm of snow recorded."),
    ("ASIA-PACIFIC",
     "South Korea navy chief begins Japan visit",
     "Talks ahead of a naval conference in Tahiti."),
    ("ASIA-PACIFIC",
     "Singapore logs third straight monthly heat record",
     "October mean 29.2\u00b0C; 2026 may be hottest year."),
    ("ASIA-PACIFIC",
     "Thai PM says government is listening to Gen Z",
     "Anutin pledges to hear reform demands."),
]

# Bottom strip: headline-only, three mini-columns.
STRIP: list[tuple[str, str]] = [
    ("BUSINESS & TECH",
     "Bitcoin slides below $56,000 as rout deepens"),
    ("BUSINESS & TECH",
     "Riemann proof \u201cchecks out\u201d, Lean verifiers rule"),
    ("BUSINESS & TECH",
     "Thinking Machines releases Inkling 2 Mini"),
    ("BUSINESS & TECH",
     "Tencent unveils Hunyuan Hy4 models"),
    ("BUSINESS & TECH",
     "OpenAI unveils anti-distillation defence"),
    ("SPACE, WEATHER & SPORT",
     "East Coast storm may become Tropical Storm Kyle"),
    ("SPACE, WEATHER & SPORT",
     "Las Vegas Grand Prix runs today; Verstappen on pole"),
    ("SPACE, WEATHER & SPORT",
     "Liverpool host Man Utd as Pochettino era starts"),
]

LEAD_KICKER = "CLIMATE \u2014 ANTALYA, TURKEY"
LEAD_HEAD = "COP31 NEARS FINAL DEAL IN ANTALYA"
LEAD_SUB = ("New package text tabled overnight as talks run into overtime; "
            "approval session due Sunday morning after days of deadlock "
            "over fossil fuels and climate finance.")

FOOTER = ("All stories reported on Sunday, 22 November 2026  \u00b7  "
          "Sources: Reuters, AP, AFP, CNN, Al Jazeera, NDTV, Yonhap, TBS, "
          "gov.za, African Union, Formula1.com, The Times, NASA/JPL, NHC")


def draw_header(draw: ImageDraw.ImageDraw) -> int:
    mast = font(SERIF_B, 80)
    draw.text((W // 2, 12), "THE WORLD TODAY", font=mast, fill=INK,
              anchor="ma")
    date_f = font(SERIF_B, 20)
    draw.text((W // 2, 104), "Sunday, 22 November 2026", font=date_f,
              fill=INK, anchor="ma")
    draw.line([(36, 134), (W - 36, 134)], fill=RULE, width=1)
    draw.line([(36, 139), (W - 36, 139)], fill=RED, width=2)
    return 150


def draw_lead(draw: ImageDraw.ImageDraw, y: int) -> int:
    kick = font(SANS_B, 13)
    draw.text((36, y), LEAD_KICKER, font=kick, fill=RED, anchor="la")
    y += 20
    head_f = font(SERIF_B, 40)
    for line in wrap(draw, LEAD_HEAD, head_f, W - 72, max_lines=2):
        draw.text((36, y), line, font=head_f, fill=INK, anchor="la")
        y += 48
    sub_f = font(SERIF_I, 14)
    for line in wrap(draw, LEAD_SUB, sub_f, W - 72, max_lines=2):
        draw.text((36, y), line, font=sub_f, fill=GREY, anchor="la")
        y += 19
    y += 6
    draw.line([(36, y), (W - 36, y)], fill=RULE, width=1)
    return y + 10


def draw_section(draw: ImageDraw.ImageDraw, x: int, y: int, width: int,
                 name: str) -> int:
    fnt = font(SANS_B, 13)
    draw.rectangle([x, y + 2, x + 9, y + 11], fill=RED)
    draw.text((x + 15, y), name, font=fnt, fill=RED, anchor="la")
    return y + 22


def draw_story(draw: ImageDraw.ImageDraw, x: int, y: int, width: int,
               head: str, sub: str) -> int:
    head_f = font(SERIF_B, 14)
    for line in wrap(draw, head, head_f, width, max_lines=2):
        draw.text((x, y), line, font=head_f, fill=INK, anchor="la")
        y += 17
    sub_f = font(SANS, 11)
    for line in wrap(draw, sub, sub_f, width, max_lines=1):
        draw.text((x, y), line, font=sub_f, fill=GREY, anchor="la")
        y += 14
    return y + 10


def draw_column(draw: ImageDraw.ImageDraw, x: int, y: int, width: int,
                stories: list[tuple[str, str, str]]) -> int:
    section = None
    for sec, head, sub in stories:
        if sec != section:
            section = sec
            y = draw_section(draw, x, y, width, sec)
        y = draw_story(draw, x, y, width, head, sub)
    return y


def draw_strip(draw: ImageDraw.ImageDraw, y: int) -> int:
    draw.line([(36, y), (W - 36, y)], fill=RULE, width=1)
    y += 8
    cols = [[], [], []]
    for i, (sec, head) in enumerate(STRIP):
        cols[i % 3].append((sec, head))
    head_f = font(SERIF_B, 14)
    sec_f = font(SANS_B, 12)
    col_w = 301
    gap = 24
    max_y = y
    for ci, items in enumerate(cols):
        x = 36 + ci * (col_w + gap)
        cy = y
        section = None
        for sec, head in items:
            if sec != section:
                section = sec
                draw.rectangle([x, cy + 1, x + 8, cy + 10], fill=RED)
                draw.text((x + 13, cy), sec, font=sec_f, fill=RED,
                          anchor="la")
                cy += 18
            for line in wrap(draw, head, head_f, col_w, max_lines=2):
                draw.text((x, cy), line, font=head_f, fill=INK, anchor="la")
                cy += 17
            cy += 6
        max_y = max(max_y, cy)
    return max_y


def draw_footer(draw: ImageDraw.ImageDraw, y: int) -> int:
    draw.line([(36, y), (W - 36, y)], fill=RULE, width=1)
    y += 8
    fnt = font(SANS, 10)
    for line in wrap(draw, FOOTER, fnt, W - 72, max_lines=2):
        draw.text((W // 2, y), line, font=fnt, fill=GREY, anchor="ma")
        y += 13
    return y


def speckle(img: Image.Image) -> None:
    rnd = random.Random(20261122)
    px = img.load()
    for _ in range(2600):
        x = rnd.randrange(W)
        y = rnd.randrange(H)
        px[x, y] = SPECKLE


def render() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_header(draw)
    y = draw_lead(draw, y)
    col_w = 301
    gap = 24
    tops = []
    for ci, stories in enumerate((COL1, COL2, COL3)):
        x = 36 + ci * (col_w + gap)
        tops.append(draw_column(draw, x, y, col_w, stories))
    body_bottom = max(tops)
    draw.line([(36, body_bottom + 2), (W - 36, body_bottom + 2)],
              fill=RULE, width=1)
    strip_bottom = draw_strip(draw, body_bottom + 10)
    draw_footer(draw, strip_bottom + 4)
    # Vertical rules between columns.
    for cx in (36 + col_w + gap // 2, 36 + 2 * col_w + gap + gap // 2):
        draw.line([(cx, y), (cx, body_bottom)], fill=RULE, width=1)
    speckle(img)
    return img


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)
    out = Path(args.output) if args.output else Path(__file__).with_name(
        "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    data = out.read_bytes()
    if len(data) > 1_048_576:
        print(f"FAIL: entry.png is {len(data)} bytes (> 1 MiB)", file=sys.stderr)
        return 1
    if args.verbose:
        print(f"wrote {out} {img.size[0]}x{img.size[1]} "
              f"{len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
