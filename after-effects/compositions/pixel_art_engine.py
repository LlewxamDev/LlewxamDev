#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJECT LWX.EXE — 16-Bit Sega Genesis / Classic Sonic.EXE Pixel Art & Compositing Engine
Generates all multi-layered PNG source plates for Adobe After Effects (LWX_EXE_Profile.aep)
and compiles high-craft, palette-optimized animated GIFs and SVGs for the GitHub Profile README.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AE_DIR = os.path.join(BASE_DIR, "after-effects")
SRC_DIR = os.path.join(AE_DIR, "assets-source")
RENDERS_DIR = os.path.join(AE_DIR, "renders")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

for sub in [
    SRC_DIR,
    RENDERS_DIR,
    os.path.join(AE_DIR, "compositions"),
    os.path.join(ASSETS_DIR, "hero"),
    os.path.join(ASSETS_DIR, "identity"),
    os.path.join(ASSETS_DIR, "dividers"),
    os.path.join(ASSETS_DIR, "projects"),
    os.path.join(ASSETS_DIR, "green-hill"),
    os.path.join(ASSETS_DIR, "technologies"),
    os.path.join(ASSETS_DIR, "trophies"),
    os.path.join(ASSETS_DIR, "footer"),
    os.path.join(ASSETS_DIR, "previews"),
]:
    os.makedirs(sub, exist_ok=True)


# ============================================================================
# 1. AUTHENTIC 5x7 / 8x8 BITMAP PIXEL FONT RENDERER (SEGA HUD STYLE)
# ============================================================================
GLYPHS_5X7 = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10011", "10101", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "00110", "00100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "/": ["00001", "00010", "00100", "00100", "01000", "10000", "10000"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "#": ["01010", "11111", "01010", "01010", "11111", "01010", "00000"],
    "@": ["01110", "10001", "10111", "10101", "10111", "10000", "01110"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    ">": ["10000", "11000", "11100", "11110", "11100", "11000", "10000"],
    "<": ["00001", "00011", "00111", "01111", "00111", "00011", "00001"],
    "·": ["00000", "00000", "00100", "01110", "00100", "00000", "00000"],
    "•": ["00000", "00000", "00100", "01110", "00100", "00000", "00000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00010", "00100", "00100", "00000", "00100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
}


def draw_pixel_text(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    scale: int = 2,
    fill=(242, 236, 238, 255),
    shadow=(5, 3, 5, 255),
    outline=None,
    letter_spacing: int = 1,
    align: str = "left",
    h_scale: int | None = None,
):
    text = text.upper()
    sx = h_scale if h_scale is not None else scale
    sy = scale
    char_w = 5 * sx
    space_w = letter_spacing * sx
    total_w = len(text) * char_w + max(0, len(text) - 1) * space_w
    if align == "center":
        x = x - total_w // 2
    elif align == "right":
        x = x - total_w

    cur_x = x
    for ch in text:
        grid = GLYPHS_5X7.get(ch, GLYPHS_5X7[" "])
        if outline:
            for r_idx, row in enumerate(grid):
                for c_idx, bit in enumerate(row):
                    if bit == "1":
                        px = cur_x + c_idx * sx
                        py = y + r_idx * sy
                        draw.rectangle(
                            [px - sx, py - sy, px + 2 * sx - 1, py + 2 * sy - 1],
                            fill=outline,
                        )
        if shadow:
            for r_idx, row in enumerate(grid):
                for c_idx, bit in enumerate(row):
                    if bit == "1":
                        px = cur_x + c_idx * sx + sx
                        py = y + r_idx * sy + sy
                        draw.rectangle([px, py, px + sx - 1, py + sy - 1], fill=shadow)
        for r_idx, row in enumerate(grid):
            for c_idx, bit in enumerate(row):
                if bit == "1":
                    px = cur_x + c_idx * sx
                    py = y + r_idx * sy
                    draw.rectangle([px, py, px + sx - 1, py + sy - 1], fill=fill)
        cur_x += char_w + space_w
    return total_w


# ============================================================================
# 2. AUTHENTIC WEB SPRITE LOADER (SONIC 1 / SONIC.EXE / GREEN HILL ZONE)
# ============================================================================
WEB_SPRITES_DIR = os.path.join(SRC_DIR, "web_authentic")
_SPRITE_CACHE: dict[str, Image.Image] = {}


def load_web_sprite(filename: str) -> Image.Image:
    if filename not in _SPRITE_CACHE:
        path = os.path.join(WEB_SPRITES_DIR, filename)
        _SPRITE_CACHE[filename] = Image.open(path).convert("RGBA")
    return _SPRITE_CACHE[filename].copy()


def extract_clean_sonic_portrait(filename: str) -> Image.Image:
    """
    Extracts the 89x81 pixel-art Sonic / Sonic.EXE portrait from sprSWSonic_* / sprSWExetior_*
    (cropping out the bottom 3px blue frame border) and removes the exterior black box via
    border floodfill while preserving internal dark eyes.
    """
    cache_key = f"portrait_clean::{filename}"
    if cache_key in _SPRITE_CACHE:
        return _SPRITE_CACHE[cache_key].copy()

    im = load_web_sprite(filename)
    crop = im.crop((4, 4, 93, 80))
    w, h = crop.size
    px = crop.load()

    visited = set()
    stack = []
    for x in range(w):
        stack.append((x, 0))
        stack.append((x, h - 1))
    for y in range(h):
        stack.append((0, y))
        stack.append((w - 1, y))

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited or cx < 0 or cy < 0 or cx >= w or cy >= h:
            continue
        visited.add((cx, cy))
        r, g, b, a = px[cx, cy]
        if r <= 10 and g <= 10 and b <= 16:
            px[cx, cy] = (0, 0, 0, 0)
            stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

    _SPRITE_CACHE[cache_key] = crop
    return crop.copy()


def build_sonic_blink_portraits() -> dict[str, Image.Image]:
    """
    Cuts the actual pixel-art blue upper eyelids from sprSWSonic_EvilSmile_0.png and
    sprSWExetior_Normal_0.png and composites/warps them onto sprSWSonic_Normal_0.png /
    sprSWExetior_Grin_0.png so Sonic closes and opens his eyes smoothly without flat rectangles.
    """
    cache_key = "sonic_blink_portraits_v2"
    if cache_key in _SPRITE_CACHE:
        return _SPRITE_CACHE[cache_key]

    p_norm = extract_clean_sonic_portrait("sprSWSonic_Normal_0.png")
    p_evil = extract_clean_sonic_portrait("sprSWSonic_EvilSmile_0.png")
    p_exe_norm = extract_clean_sonic_portrait("sprSWExetior_Normal_0.png")
    p_exe_grin = extract_clean_sonic_portrait("sprSWExetior_Grin_0.png")

    # 1. Half-blink: cut upper eyelid pixels from sprSWSonic_EvilSmile_0.png onto sprSWSonic_Normal_0.png
    p_half = p_norm.copy()
    px_half = p_half.load()
    px_evil = p_evil.load()
    for y in range(28, 50):
        for x in range(13, 60):
            if px_evil[x, y][3] > 0:
                px_half[x, y] = px_evil[x, y]

    # 2. Fully closed eyes: stretch the cut blue upper eyelid vertically down to the lower eye boundary
    p_closed = p_norm.copy()
    px_closed = p_closed.load()
    px_norm = p_norm.load()
    for x in range(12, 59):
        lid_col = []
        for y in range(26, 49):
            r, g, b, a = px_evil[x, y]
            if a > 0 and b > r + 20:
                lid_col.append((y, (r, g, b, a)))
        if not lid_col:
            continue
        y_top = lid_col[0][0]
        y_open_bot = None
        for y in range(56, 36, -1):
            r, g, b, a = px_norm[x, y]
            if a > 0 and (
                (r > 180 and g > 180 and b > 180)
                or (r < 50 and g < 50 and b < 55 and y < 55)
                or (g > r + 25 and y < 56)
            ):
                y_open_bot = y
                break
        if y_open_bot is None or y_open_bot <= y_top:
            continue
        span = y_open_bot - y_top + 1
        for dy in range(span):
            src_idx = min(len(lid_col) - 1, int(dy * len(lid_col) / max(1, span)))
            px_closed[x, y_top + dy] = lid_col[src_idx][1]
        px_closed[x, y_open_bot] = (10, 20, 56, 255)
        if y_open_bot - 1 >= y_top:
            px_closed[x, y_open_bot - 1] = (24, 52, 128, 255)

    # 3. EXE half-open blink: cut dark eyelids from sprSWExetior_Normal_0.png onto sprSWExetior_Grin_0.png
    p_exe_full = p_exe_grin.copy()
    pd_exe = ImageDraw.Draw(p_exe_full)
    pd_exe.rectangle([25, 48, 27, 50], fill=(255, 24, 52, 255))
    pd_exe.rectangle([46, 47, 48, 49], fill=(255, 24, 52, 255))
    pd_exe.rectangle([25, 55, 27, 63], fill=(148, 0, 22, 220))
    pd_exe.rectangle([46, 54, 48, 62], fill=(148, 0, 22, 220))

    p_exe_half = p_exe_full.copy()
    px_exe_half = p_exe_half.load()
    px_exe_n = p_exe_norm.load()
    for y in range(28, 48):
        for x in range(13, 60):
            r, g, b, a = px_exe_n[x, y]
            if a > 0 and b > r + 10:
                if y + 3 < 76:
                    px_exe_half[x, y + 3] = (r, g, b, a)
                px_exe_half[x, y] = (r, g, b, a)

    res = {
        "normal": p_norm,
        "blink_half": p_half,
        "blink_closed": p_closed,
        "exe_blink_half": p_exe_half,
        "exe_full": p_exe_full,
    }
    _SPRITE_CACHE[cache_key] = res
    return res


def render_sonic_character_canvas(
    mode: str = "normal",  # "normal", "blink_half", "blink_closed", "exe_blink_half", "exe_full"
    breath_offset: int = 0,
    wag_phase: int = 0,
    upscale: int = 4,
    style: str = "emblem",  # "emblem" (Hero ring portrait) or "fullbody" (Identity standing sprite)
) -> Image.Image:
    """
    Composites authentic Classic Sonic (1991) and Classic Sonic.EXE sprites from `web_authentic`
    on an 88x88 base grid upscaled with NEAREST neighbor. Both Normal and EXE states share 100%
    identical framing.
    """
    target_w, target_h = 88 * upscale, 88 * upscale
    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    is_exe = mode in ("exe_full", "exe_blink_half")
    by = breath_offset * (upscale // 2)

    if style == "fullbody":
        # Full-body authentic Classic Sonic / Sonic.EXE standing sprite for COMP_02_IDENTITY
        if mode in ("normal", "blink_half"):
            full_spr = load_web_sprite("sprGU_SonicSmile_0.png") if wag_phase == 0 else load_web_sprite("sprSonicStand_0.png")
        elif mode == "blink_closed":
            full_spr = load_web_sprite("sprSonicStandCrazy_0.png")
        elif mode == "exe_blink_half":
            full_spr = load_web_sprite("sprExetior_StandSmile_0.png")
        else:
            full_spr = load_web_sprite("sprExetior_StandSmile_0.png") if wag_phase == 0 else load_web_sprite("sprExetiorWinPose_0.png")

        fb_scale = max(1, int(round(upscale * 1.65)))
        fb_resized = full_spr.resize((full_spr.width * fb_scale, full_spr.height * fb_scale), Image.Resampling.NEAREST)
        fb_x = (target_w - fb_resized.width) // 2 - (4 * upscale)
        fb_y = target_h - fb_resized.height - (10 * upscale) + by
        canvas.paste(fb_resized, (fb_x, fb_y), fb_resized)

        # Floating authentic spinning Golden/Blood Ring beside Sonic
        ring_sp = render_ring_sprite(size=18 * upscale, phase=(wag_phase * 0.25), corrupted=is_exe)
        canvas.alpha_composite(ring_sp, (fb_x + fb_resized.width + 2 * upscale, fb_y + 10 * upscale - by))
        return canvas

    # --- Default style == "emblem": Iconic Sonic Golden Ring Emblem with High-Res Authentic Portrait ---
    ring_box = [10 * upscale, 8 * upscale, 78 * upscale, 76 * upscale]
    ring_inner = [18 * upscale, 16 * upscale, 70 * upscale, 68 * upscale]
    if not is_exe:
        draw.ellipse([ring_box[0] + 4, ring_box[1] + 4, ring_box[2] + 4, ring_box[3] + 4], fill=(4, 2, 6, 195))
        draw.ellipse(ring_box, fill=(255, 208, 0, 255), outline=(148, 76, 0, 255), width=max(2, upscale // 2))
        draw.ellipse(
            [ring_box[0] + upscale, ring_box[1] + upscale, ring_box[2] - upscale, ring_box[3] - upscale],
            outline=(255, 248, 156, 255),
            width=max(2, upscale // 2),
        )
        draw.ellipse(ring_inner, fill=(14, 36, 108, 255), outline=(92, 44, 0, 255), width=max(2, upscale // 2))
    else:
        draw.ellipse([ring_box[0] + 4, ring_box[1] + 4, ring_box[2] + 4, ring_box[3] + 4], fill=(2, 0, 2, 235))
        draw.ellipse(ring_box, fill=(196, 8, 28, 255), outline=(64, 0, 10, 255), width=max(2, upscale // 2))
        draw.ellipse(
            [ring_box[0] + upscale, ring_box[1] + upscale, ring_box[2] - upscale, ring_box[3] - upscale],
            outline=(255, 68, 92, 255),
            width=max(2, upscale // 2),
        )
        draw.ellipse(ring_inner, fill=(10, 2, 6, 255), outline=(48, 0, 8, 255), width=max(2, upscale // 2))

    portraits = build_sonic_blink_portraits()
    portrait = portraits.get(mode, portraits["normal"]).copy()

    p_scale = max(1, int(round(upscale * 0.76)))
    p_resized = portrait.resize((portrait.width * p_scale, portrait.height * p_scale), Image.Resampling.NEAREST)
    px_pos = 44 * upscale - p_resized.width // 2
    py_pos = ring_inner[3] - p_resized.height + (2 * upscale) + by

    # Clip bottom half of portrait cleanly inside the inner circle of the Golden Ring while letting top ears/quills pop out
    p_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    p_layer.paste(p_resized, (px_pos, py_pos), p_resized)

    clip_mask = Image.new("L", (target_w, target_h), 0)
    md = ImageDraw.Draw(clip_mask)
    md.ellipse(ring_inner, fill=255)
    md.rectangle([ring_inner[0], 0, ring_inner[2], 40 * upscale], fill=255)

    clipped_p = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    clipped_p.paste(p_layer, (0, 0), clip_mask)
    canvas.alpha_composite(clipped_p)

    return canvas


# ============================================================================
# 3. GREEN HILL ZONE MULTI-PLANE ENVIRONMENT GENERATOR (AUTHENTIC SPRITES)
# ============================================================================
def render_ghz_sky_layer(width=1200, height=440, corrupted=False, cloud_shift=0) -> Image.Image:
    """
    Uses authentic sprGHZ26_0.png (normal) and sprGHZ26_Bloody_0.png (corrupted) sky plates.
    """
    src = load_web_sprite("sprGHZ26_Bloody_0.png" if corrupted else "sprGHZ26_0.png")
    sky_h = int(height * 0.56)
    scaled_w = max(640, int(src.width * (sky_h / src.height)))
    sky_strip = src.resize((scaled_w, sky_h), Image.Resampling.NEAREST)

    img = Image.new("RGBA", (width, height), (8, 4, 8, 255) if corrupted else (24, 96, 228, 255))
    shift = int(cloud_shift) % scaled_w
    for x in range(-shift, width, scaled_w):
        img.paste(sky_strip, (x, 0))
    return img


def render_ghz_mountains_and_water_layer(width=1200, height=440, corrupted=False, water_phase=0) -> Image.Image:
    """
    Uses authentic 4-frame animated sprGHZ16_0..3.png (normal) and sprGHZ16_Bloody_0..3.png (corrupted)
    containing the original Green Hill Zone mountains, waterfall, and shimmering lake reflection.
    """
    frame_idx = int(water_phase) % 4
    fn = f"sprGHZ16_Bloody_{frame_idx}.png" if corrupted else f"sprGHZ16_{frame_idx}.png"
    src = load_web_sprite(fn)

    band_y0 = int(height * 0.28)
    band_h = int(height * 0.46)
    scaled_w = max(640, int(src.width * (band_h / src.height)))
    strip = src.resize((scaled_w, band_h), Image.Resampling.NEAREST)

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for x in range(0, width, scaled_w):
        img.paste(strip, (x, band_y0), strip)
    return img


def render_ghz_palms_and_ground_layer(
    width=1200,
    height=440,
    corrupted=False,
    sway_px=0,
    include_critters=True,
) -> Image.Image:
    """
    Composites authentic Green Hill Zone bushes (backGHZ_Bushes1 / Blood), palm trees (backGHZ_Trees1),
    animated flowers (sprGHZ_Flower1), grass/soil tiles (backGHZGround_Tile & backGHZ_Tile),
    and discrete background critter silhouettes.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ground_y = int(height * 0.68)

    # 1. Authentic Green Hill Bushes along the horizon
    bush = load_web_sprite("backGHZ_Bushes1Blood.png" if corrupted else "backGHZ_Bushes1.png")
    for bx in [24, 340, 720, 980]:
        img.paste(bush, (bx, ground_y - bush.height + 8), bush)

    # 2. Authentic Green Hill Flowers
    flower_fn = "sprGHZ_Flower1Blood_0.png" if corrupted else ("sprGHZ_Flower1_0.png" if sway_px == 0 else "sprGHZ_Flower1_1.png")
    flower = load_web_sprite(flower_fn)
    flower_s = flower.resize((flower.width * 2, flower.height * 2), Image.Resampling.NEAREST)
    for fx in [260, 650, 910]:
        img.paste(flower_s, (fx, ground_y - flower_s.height + 4), flower_s)

    # 3. Authentic 16-bit Palm Trees
    palm = load_web_sprite("backGHZ_Trees1.png")
    palm_s = palm.resize((int(palm.width * 1.3), int(palm.height * 1.3)), Image.Resampling.NEAREST)
    if corrupted:
        # Darken palm tree slightly for corrupted atmosphere
        r, g, b, a = palm_s.split()
        r = r.point(lambda v: int(v * 0.55))
        g = g.point(lambda v: int(v * 0.35))
        b = b.point(lambda v: int(v * 0.35))
        palm_s = Image.merge("RGBA", (r, g, b, a))

    for px_pos in [36, width - palm_s.width - 36]:
        img.paste(palm_s, (px_pos + sway_px, ground_y - palm_s.height + 12), palm_s)

    # 4. Authentic Discrete Critter Sprites in Background (Section 9 Compliance)
    if include_critters:
        c1 = load_web_sprite("sprGHZ_Animal1Dead_0.png")
        c2 = load_web_sprite("sprGHZ_Animal2Dead_0.png")
        img.paste(c1, (192, ground_y - c1.height + 2), c1)
        img.paste(c2, (width - 210, ground_y - c2.height + 2), c2)

    # 5. Authentic Checkerboard Ground & Grass Cap (backGHZGround_Tile.png + backGHZ_Tile.png)
    top_tile = load_web_sprite("backGHZGround_Tile.png")
    sub_tile = load_web_sprite("backGHZ_Tile.png")
    if corrupted:
        for t_im in (top_tile, sub_tile):
            r, g, b, a = t_im.split()
            r = r.point(lambda v: min(255, int(v * 0.65 + 20)))
            g = g.point(lambda v: int(v * 0.25))
            b = b.point(lambda v: int(v * 0.25))
            t_im.paste(Image.merge("RGBA", (r, g, b, a)))

    for x in range(0, width, top_tile.width):
        img.paste(top_tile, (x, ground_y - 10), top_tile)
        for y in range(ground_y - 10 + top_tile.height, height, sub_tile.height):
            img.paste(sub_tile, (x, y), sub_tile)

    return img


# ============================================================================
# 4. 16-BIT ROTATING GOLDEN RING & CORRUPTED RING GENERATOR (AUTHENTIC SPRITES)
# ============================================================================
def render_ring_sprite(size=44, phase=0.0, corrupted=False, scatter=0.0) -> Image.Image:
    """
    Uses authentic sprRing_0..3.png and sprHS_BloodRing_0.png from web_authentic.
    """
    if not corrupted:
        idx = int(phase * 4) % 4
        base_ring = load_web_sprite(f"sprRing_{idx}.png")
    else:
        base_ring = load_web_sprite("sprHS_BloodRing_0.png")

    grid = 24
    img = base_ring.resize((grid, grid), Image.Resampling.NEAREST)

    if scatter > 0.0:
        src_px = img.load()
        scattered = Image.new("RGBA", (grid, grid), (0, 0, 0, 0))
        dst_px = scattered.load()
        rng = random.Random(int(phase * 100) + 42)
        for y in range(grid):
            for x in range(grid):
                r, g, b, a = src_px[x, y]
                if a > 0:
                    if rng.random() < scatter * 0.72:
                        continue
                    dx = int(rng.uniform(-scatter * 6, scatter * 6))
                    dy = int(rng.uniform(-scatter * 4, scatter * 4))
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid and 0 <= ny < grid:
                        dst_px[nx, ny] = (255, 18, 42, a) if rng.random() < scatter else (r, g, b, a)
        img = scattered

    return img.resize((size, size), Image.Resampling.NEAREST)


# ============================================================================
# 5. SONIC 16-BIT ITEM MONITOR BOXES & OFFICIAL HIGH-RES TECHNOLOGY LOGOS
# ============================================================================
TECH_LOGOS_DIR = os.path.join(SRC_DIR, "tech_logos")
_TECH_LOGO_CACHE: dict[str, Image.Image] = {}

TECH_SPECS = {
    # Languages (11)
    "PYTHON": {"bg": (20, 38, 62), "fg": (255, 212, 59), "accent": (55, 118, 171), "logo": "python.png"},
    "JAVASCRIPT": {"bg": (36, 32, 12), "fg": (247, 223, 30), "accent": (247, 223, 30), "logo": "javascript.png"},
    "TYPESCRIPT": {"bg": (18, 42, 74), "fg": (255, 255, 255), "accent": (49, 120, 198), "logo": "typescript.png"},
    "PHP": {"bg": (52, 56, 92), "fg": (255, 255, 255), "accent": (119, 123, 180), "logo": "php.png"},
    "LUA": {"bg": (14, 18, 58), "fg": (255, 255, 255), "accent": (82, 132, 255), "logo": "lua.png"},
    "JAVA": {"bg": (232, 238, 246), "fg": (248, 152, 32), "accent": (248, 152, 32), "logo": "java.png"},
    "C++": {"bg": (14, 36, 68), "fg": (255, 255, 255), "accent": (101, 154, 210), "logo": "cpp.png"},
    "C#": {"bg": (42, 18, 56), "fg": (255, 255, 255), "accent": (155, 79, 150), "logo": "csharp.png"},
    "RUST": {"bg": (36, 22, 16), "fg": (247, 76, 0), "accent": (255, 142, 82), "logo": "rust.png"},
    "KOTLIN": {"bg": (34, 20, 68), "fg": (255, 255, 255), "accent": (127, 82, 255), "logo": "kotlin.png"},
    "ASSEMBLY": {"bg": (22, 28, 38), "fg": (0, 255, 168), "accent": (0, 212, 255), "logo": "assembly.png"},
    # Ecosystem (13)
    "NODE.JS": {"bg": (18, 44, 22), "fg": (255, 255, 255), "accent": (104, 160, 99), "logo": "nodejs.png"},
    "REACT": {"bg": (14, 34, 48), "fg": (97, 218, 251), "accent": (97, 218, 251), "logo": "react.png"},
    "NEXT.JS": {"bg": (20, 22, 30), "fg": (255, 255, 255), "accent": (200, 200, 215), "logo": "nextjs.png"},
    "VUE": {"bg": (18, 42, 34), "fg": (65, 184, 131), "accent": (65, 184, 131), "logo": "vue.png"},
    "NUXT": {"bg": (16, 44, 34), "fg": (0, 220, 130), "accent": (0, 220, 130), "logo": "nuxt.png"},
    "ANGULAR": {"bg": (52, 12, 24), "fg": (255, 255, 255), "accent": (255, 68, 102), "logo": "angular.png"},
    "SVELTE": {"bg": (54, 20, 12), "fg": (255, 255, 255), "accent": (255, 110, 64), "logo": "svelte.png"},
    "ASTRO": {"bg": (28, 16, 48), "fg": (255, 93, 1), "accent": (255, 120, 40), "logo": "astro.png"},
    "EXPRESS": {"bg": (26, 28, 36), "fg": (245, 245, 250), "accent": (180, 180, 196), "logo": "express.png"},
    "NESTJS": {"bg": (52, 12, 26), "fg": (255, 255, 255), "accent": (224, 35, 78), "logo": "nestjs.png"},
    "VITE": {"bg": (32, 24, 68), "fg": (255, 214, 46), "accent": (148, 108, 255), "logo": "vite.png"},
    "TAILWIND": {"bg": (12, 42, 58), "fg": (56, 189, 248), "accent": (56, 189, 248), "logo": "tailwind.png"},
    "FASTIFY": {"bg": (24, 26, 34), "fg": (255, 255, 255), "accent": (255, 204, 0), "logo": "fastify.png"},
    # Web / Data / Tools / Creative (15)
    "HTML5": {"bg": (54, 22, 14), "fg": (255, 255, 255), "accent": (227, 79, 38), "logo": "html5.png"},
    "CSS3": {"bg": (14, 38, 64), "fg": (255, 255, 255), "accent": (51, 169, 220), "logo": "css3.png"},
    "POSTGRES": {"bg": (18, 38, 58), "fg": (255, 255, 255), "accent": (108, 168, 216), "logo": "postgres.png"},
    "MYSQL": {"bg": (232, 240, 248), "fg": (242, 145, 17), "accent": (0, 145, 178), "logo": "mysql.png"},
    "SQL SERVER": {"bg": (244, 238, 240), "fg": (255, 255, 255), "accent": (232, 72, 72), "logo": "sql_server.png"},
    "DOCKER": {"bg": (14, 38, 64), "fg": (255, 255, 255), "accent": (36, 150, 237), "logo": "docker.png"},
    "GIT": {"bg": (54, 20, 14), "fg": (255, 255, 255), "accent": (240, 80, 50), "logo": "git.png"},
    "GITHUB": {"bg": (24, 28, 36), "fg": (255, 255, 255), "accent": (168, 180, 198), "logo": "github.png"},
    "LINUX": {"bg": (32, 32, 40), "fg": (242, 201, 76), "accent": (242, 201, 76), "logo": "linux.png"},
    "VS CODE": {"bg": (12, 38, 68), "fg": (255, 255, 255), "accent": (35, 168, 242), "logo": "vs_code.png"},
    "VISUAL STUDIO": {"bg": (38, 20, 62), "fg": (255, 255, 255), "accent": (158, 104, 224), "logo": "visual_studio.png"},
    "BLENDER": {"bg": (54, 28, 12), "fg": (255, 255, 255), "accent": (245, 130, 32), "logo": "blender.png"},
    "AFTER EFFECTS": {"bg": (16, 16, 58), "fg": (153, 153, 255), "accent": (153, 153, 255), "logo": "after_effects.png"},
    "PHOTOSHOP": {"bg": (10, 32, 58), "fg": (49, 168, 255), "accent": (49, 168, 255), "logo": "photoshop.png"},
    "HOUDINI": {"bg": (54, 22, 10), "fg": (255, 255, 255), "accent": (255, 102, 26), "logo": "houdini.png"},
}


def load_official_tech_logo(logo_filename: str, target_size: int) -> Image.Image | None:
    key = f"{logo_filename}::{target_size}"
    if key in _TECH_LOGO_CACHE:
        return _TECH_LOGO_CACHE[key].copy()
    path = os.path.join(TECH_LOGOS_DIR, logo_filename)
    if not os.path.exists(path):
        return None
    im = Image.open(path).convert("RGBA")
    resized = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    _TECH_LOGO_CACHE[key] = resized
    return resized.copy()


def draw_condensed_scale2_text(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    fill=(244, 240, 242, 255),
    shadow=(0, 0, 0, 255),
):
    """
    Draws 14px-tall (scale=2 vertical) pixel text with slightly tighter horizontal column widths
    ([2, 2, 1, 2, 2] = 9px per char + 1px space = 10px pitch) so 13-char labels like
    'AFTER EFFECTS' and 'VISUAL STUDIO' have the EXACT same 14px height as every other technology
    while fitting cleanly inside their monitor box with generous right margin.
    """
    text = text.upper()
    col_widths = [2, 2, 1, 2, 2]
    col_offsets = [0, 2, 4, 5, 7]
    char_w = 9
    space_w = 1
    cur_x = x
    for ch in text:
        grid = GLYPHS_5X7.get(ch, GLYPHS_5X7[" "])
        if shadow:
            for r_idx, row in enumerate(grid):
                for c_idx, bit in enumerate(row):
                    if bit == "1":
                        px = cur_x + col_offsets[c_idx] + 2
                        py = y + r_idx * 2 + 2
                        cw = col_widths[c_idx]
                        draw.rectangle([px, py, px + cw - 1, py + 1], fill=shadow)
        for r_idx, row in enumerate(grid):
            for c_idx, bit in enumerate(row):
                if bit == "1":
                    px = cur_x + col_offsets[c_idx]
                    py = y + r_idx * 2
                    cw = col_widths[c_idx]
                    draw.rectangle([px, py, px + cw - 1, py + 1], fill=fill)
        cur_x += char_w + space_w


def draw_tech_emblem_icon(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    size: int,
    name: str,
    corrupted: bool = False,
    canvas_img: Image.Image | None = None,
):
    spec = TECH_SPECS.get(name, {"bg": (30, 32, 44), "fg": (255, 255, 255), "accent": (255, 15, 43), "logo": ""})
    if not corrupted:
        bg = spec["bg"]
    else:
        bg = (232, 198, 206) if spec["bg"][0] > 180 else (max(14, spec["bg"][0] // 2), 6, 12)
    acc = spec["accent"] if not corrupted else (220, 18, 44)

    # Monitor inner CRT screen
    draw.rectangle([x, y, x + size, y + size], fill=(6, 6, 12, 255))
    draw.rectangle([x + 1, y + 1, x + size - 1, y + size - 1], fill=(*bg, 255), outline=(*acc, 185), width=1)

    target_im = canvas_img if canvas_img is not None else getattr(draw, "_image", None)
    logo_fn = spec.get("logo", "")
    logo_pad = 4
    logo_im = load_official_tech_logo(logo_fn, size - logo_pad * 2) if logo_fn else None
    if logo_im is not None and target_im is not None:
        target_im.alpha_composite(logo_im, (x + logo_pad, y + logo_pad))
    else:
        draw_pixel_text(
            draw,
            x + size // 2,
            y + size // 2 - 6,
            name[:2],
            scale=2,
            fill=(255, 255, 255, 255),
            shadow=(0, 0, 0, 255),
            align="center",
        )


def draw_sonic_monitor_slot(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    tech_name: str,
    corrupted: bool = False,
    highlight_border: bool = False,
    canvas_img: Image.Image | None = None,
):
    """
    Draws an authentic 16-bit Sonic Item Monitor / Zone Slot integrated into Green Hill Zone,
    featuring the official high-resolution logo on the left and uniform 14px-tall typography.
    """
    casing_outer = (22, 24, 34, 255) if not corrupted else (36, 4, 10, 255)
    casing_mid = (72, 78, 98, 255) if not corrupted else (98, 8, 22, 255)
    casing_hi = (142, 152, 178, 255) if not corrupted else (255, 18, 44, 255)
    screen_bg = (10, 12, 20, 242) if not corrupted else (12, 3, 6, 248)

    if highlight_border and not corrupted:
        casing_mid = (148, 24, 44, 255)
        casing_hi = (255, 180, 0, 255)

    # Drop shadow onto terrain
    draw.rectangle([x + 4, y + 4, x + w + 4, y + h + 4], fill=(4, 2, 4, 180))
    # Outer metallic monitor casing
    draw.rectangle([x, y, x + w, y + h], fill=casing_outer)
    draw.rectangle([x + 2, y + 2, x + w - 2, y + h - 2], fill=casing_mid)
    # Top/left 16-bit bevel highlight
    draw.line([(x + 2, y + 2), (x + w - 2, y + 2)], fill=casing_hi, width=2)
    draw.line([(x + 2, y + 2), (x + 2, y + h - 2)], fill=casing_hi, width=2)
    # Inner screen recess
    draw.rectangle([x + 5, y + 5, x + w - 5, y + h - 5], fill=screen_bg)

    # Left CRT icon box with official high-res logo
    icon_s = h - 14
    draw_tech_emblem_icon(draw, x + 8, y + 7, icon_s, tech_name, corrupted=corrupted, canvas_img=canvas_img)

    # Right text label + subtle CRT status LED
    led_col = (40, 220, 96, 255) if not corrupted else (255, 15, 43, 255)
    draw.rectangle([x + w - 11, y + 8, x + w - 7, y + 12], fill=led_col)

    text_col = (244, 240, 242, 255) if not corrupted else (255, 204, 212, 255)
    tx = x + 8 + icon_s + 9
    ty = y + (h - 14) // 2
    avail_text_w = (x + w - 8) - tx
    normal_w = len(tech_name) * 10 + max(0, len(tech_name) - 1) * 2

    if normal_w <= avail_text_w:
        draw_pixel_text(
            draw,
            tx,
            ty,
            tech_name,
            scale=2,
            fill=text_col,
            shadow=(0, 0, 0, 255),
            align="left",
        )
    else:
        draw_condensed_scale2_text(
            draw,
            tx,
            ty,
            tech_name,
            fill=text_col,
            shadow=(0, 0, 0, 255),
        )


# ============================================================================
# 6. GLITCH, INTERFERENCE & CRT SCANLINE FILTERS
# ============================================================================
def apply_crt_scanlines(img: Image.Image, alpha: int = 28) -> Image.Image:
    out = img.copy()
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    w, h = out.size
    for y in range(0, h, 3):
        d.line([(0, y), (w, y)], fill=(4, 1, 3, alpha), width=1)
    return Image.alpha_composite(out, overlay)


def apply_exe_interference(img: Image.Image, intensity: float = 1.0, seed: int = 7) -> Image.Image:
    """
    Applies authentic 16-bit horizontal slice displacement, crimson chromatic shift,
    and brief static bars for the 60-100ms Sonic.EXE transition frames.
    """
    rng = random.Random(seed)
    w, h = img.size
    out = img.copy()

    # Horizontal slice displacement
    num_slices = int(6 + intensity * 10)
    for _ in range(num_slices):
        sy = rng.randint(0, h - 18)
        sh = rng.randint(4, 22)
        dx = rng.choice([-18, -12, -8, 8, 12, 18, 24])
        strip = out.crop((0, sy, w, min(h, sy + sh)))
        out.paste(strip, (dx, sy))

    # Subtle red channel offset
    r, g, b, a = out.split()
    r_shifted = ImageChops.offset(r, int(4 * intensity), 0)
    b_shifted = ImageChops.offset(b, int(-3 * intensity), 0)
    out = Image.merge("RGBA", (r_shifted, g, b_shifted, a))

    # Brief crimson static scanline bars
    d = ImageDraw.Draw(out)
    for _ in range(int(4 * intensity)):
        by = rng.randint(10, h - 10)
        bx0 = rng.randint(0, w // 2)
        bx1 = rng.randint(w // 2, w)
        d.rectangle([bx0, by, bx1, by + 2], fill=(255, 15, 43, 165))

    return out


def save_optimized_gif(frames: list[Image.Image], out_path: str, durations_ms: list[int] | int):
    """
    Saves a sequence of RGBA/RGB PIL images as a crisp, size-optimized looping GIF.
    Each frame is quantized with FASTOCTREE and dither=NONE so normal Green Hill frames,
    corrupted Sonic.EXE frames, and official high-resolution technology logos retain
    full 256-color fidelity without color starvation or dithering noise.
    """
    quantized = [
        f.convert("RGB").quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        for f in frames
    ]
    quantized[0].save(
        out_path,
        save_all=True,
        append_images=quantized[1:],
        duration=durations_ms,
        loop=0,
        optimize=True,
    )


# ============================================================================
# 7. COMPOSITION 01: HERO ("OLHE MEU PERFIL." — BLINK TRANSITION + 6s NORMAL / 6s EXE)
# ============================================================================
def build_comp_01_hero():
    W, H = 1200, 400

    # Export separated source layers for After Effects COMP_01_HERO
    sky_norm = render_ghz_sky_layer(W, H, corrupted=False)
    sky_corr = render_ghz_sky_layer(W, H, corrupted=True)
    mtn_norm = render_ghz_mountains_and_water_layer(W, H, corrupted=False)
    mtn_corr = render_ghz_mountains_and_water_layer(W, H, corrupted=True)
    fg_norm = render_ghz_palms_and_ground_layer(W, H, corrupted=False, include_critters=False)
    fg_corr = render_ghz_palms_and_ground_layer(W, H, corrupted=True, include_critters=True)

    sonic_norm_0 = render_sonic_character_canvas("normal", breath_offset=0, wag_phase=0, upscale=4)
    sonic_norm_1 = render_sonic_character_canvas("normal", breath_offset=1, wag_phase=1, upscale=4)
    sonic_blink_half = render_sonic_character_canvas("blink_half", breath_offset=0, wag_phase=0, upscale=4)
    sonic_blink_closed = render_sonic_character_canvas("blink_closed", breath_offset=0, wag_phase=0, upscale=4)
    sonic_exe_blink_half = render_sonic_character_canvas("exe_blink_half", breath_offset=0, wag_phase=0, upscale=4)
    sonic_exe_0 = render_sonic_character_canvas("exe_full", breath_offset=0, wag_phase=0, upscale=4)
    sonic_exe_1 = render_sonic_character_canvas("exe_full", breath_offset=1, wag_phase=1, upscale=4)

    sky_norm.save(os.path.join(SRC_DIR, "hero_sky_normal.png"))
    sky_corr.save(os.path.join(SRC_DIR, "hero_sky_corrupted.png"))
    mtn_norm.save(os.path.join(SRC_DIR, "hero_mountains_normal.png"))
    mtn_corr.save(os.path.join(SRC_DIR, "hero_mountains_corrupted.png"))
    fg_norm.save(os.path.join(SRC_DIR, "hero_ground_normal.png"))
    fg_corr.save(os.path.join(SRC_DIR, "hero_ground_corrupted.png"))
    sonic_norm_0.save(os.path.join(SRC_DIR, "sonic_normal_idle_01.png"))
    sonic_norm_1.save(os.path.join(SRC_DIR, "sonic_normal_idle_02.png"))
    sonic_blink_closed.save(os.path.join(SRC_DIR, "sonic_normal_blink.png"))
    sonic_exe_0.save(os.path.join(SRC_DIR, "sonic_exe_corrupt_01.png"))
    sonic_exe_blink_half.save(os.path.join(SRC_DIR, "sonic_exe_eye_micro.png"))

    # Also save Hero Title Plates ("OLHE MEU PERFIL.") for AE
    plates = {}
    for plate_mode in ["normal", "exe"]:
        t_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        td = ImageDraw.Draw(t_img)
        is_ex = plate_mode == "exe"
        bx0, by0, bx1, by1 = 470, 128, 1118, 256
        td.rectangle([bx0 + 6, by0 + 6, bx1 + 6, by1 + 6], fill=(4, 2, 4, 205))
        td.rectangle([bx0, by0, bx1, by1], fill=(12, 16, 36, 238) if not is_ex else (16, 2, 6, 248))
        border_c = (255, 216, 0, 255) if not is_ex else (255, 15, 43, 255)
        inner_c = (24, 88, 216, 255) if not is_ex else (128, 0, 20, 255)
        td.rectangle([bx0, by0, bx1, by1], outline=border_c, width=4)
        td.rectangle([bx0 + 6, by0 + 6, bx1 - 6, by1 - 6], outline=inner_c, width=2)
        td.rectangle([bx0 + 18, by0 + 18, bx1 - 18, by0 + 24], fill=border_c)
        td.rectangle([bx0 + 18, by1 - 24, bx1 - 18, by1 - 18], fill=inner_c)
        txt_col = (255, 252, 240, 255) if not is_ex else (255, 20, 48, 255)
        sh_col = (12, 24, 88, 255) if not is_ex else (56, 0, 10, 255)
        draw_pixel_text(
            td,
            (bx0 + bx1) // 2,
            by0 + 44,
            "OLHE MEU PERFIL.",
            scale=5,
            fill=txt_col,
            shadow=sh_col,
            letter_spacing=1,
            align="center",
        )
        t_img.save(os.path.join(SRC_DIR, f"hero_title_plate_{plate_mode}.png"))
        plates[plate_mode] = t_img

    # Timeline specification:
    # - 24 frames Normal (24 * 250ms = 6,000ms = 6.0s)
    # - 3 frames Eye-Blink Transition into EXE:
    #     f=24: blink_half (80ms)
    #     f=25: blink_closed (90ms) -> transition trigger
    #     f=26: exe_blink_half (80ms) -> eyes opening as Sonic.EXE
    # - 24 frames Corrupted Sonic.EXE (24 * 250ms = 6,000ms = 6.0s, clean non-glitched corrupted animation)
    # - 3 frames Eye-Blink Transition back to Normal:
    #     f=51: exe_blink_half (80ms)
    #     f=52: blink_closed (90ms)
    #     f=53: blink_half (80ms)
    timeline = []
    for i in range(24):
        timeline.append(("normal", False, 250, False))
    timeline.append(("blink_half", False, 110, False))
    timeline.append(("blink_closed", False, 130, False))
    timeline.append(("exe_blink_half", True, 110, False))
    for i in range(24):
        timeline.append(("exe_full", True, 250, False))
    timeline.append(("exe_blink_half", True, 110, False))
    timeline.append(("blink_closed", False, 130, False))
    timeline.append(("blink_half", False, 110, False))

    frames = []
    durations = []
    total_f = len(timeline)

    for f, (c_mode, corrupt_env, dur_ms, is_trans_peak) in enumerate(timeline):
        sway = int(round(math.sin(f * 2 * math.pi / 24.0) * 3))
        cloud_dx = int((f * 6) % 640)

        canvas = render_ghz_sky_layer(W, H, corrupted=corrupt_env, cloud_shift=cloud_dx)
        mtn = render_ghz_mountains_and_water_layer(W, H, corrupted=corrupt_env, water_phase=f)
        fg = render_ghz_palms_and_ground_layer(
            W, H, corrupted=corrupt_env, sway_px=sway, include_critters=corrupt_env
        )
        canvas = Image.alpha_composite(canvas, mtn)
        canvas = Image.alpha_composite(canvas, fg)

        for idx_r, rx in enumerate([520, 580, 640]):
            ry = 72 + int(math.sin((f + idx_r * 3) * 2 * math.pi / 12.0) * 4)
            ring_sp = render_ring_sprite(size=36, phase=((f + idx_r) % 4) / 4.0, corrupted=corrupt_env)
            canvas.alpha_composite(ring_sp, (rx, ry))

        char_x, char_y = 108, 22
        breath = 1 if (f // 2) % 2 == 1 else 0

        if c_mode == "normal":
            char_sp = sonic_norm_1 if breath else sonic_norm_0
        elif c_mode == "blink_half":
            char_sp = sonic_blink_half
        elif c_mode == "blink_closed":
            char_sp = sonic_blink_closed
        elif c_mode == "exe_blink_half":
            char_sp = sonic_exe_blink_half
        else:
            char_sp = sonic_exe_1 if breath else sonic_exe_0

        canvas.alpha_composite(char_sp, (char_x, char_y))
        canvas.alpha_composite(plates["exe" if corrupt_env else "normal"], (0, 0))

        if is_trans_peak:
            canvas = apply_exe_interference(canvas, intensity=0.55, seed=101 + f)

        canvas = apply_crt_scanlines(canvas, alpha=22 if not corrupt_env else 34)
        frames.append(canvas)
        durations.append(dur_ms)

        if f == 0:
            canvas.save(os.path.join(ASSETS_DIR, "previews", "hero_normal_frame.png"))
        elif f == 25:
            canvas.save(os.path.join(ASSETS_DIR, "previews", "hero_blink_frame.png"))
        elif f == 30:
            canvas.save(os.path.join(ASSETS_DIR, "previews", "hero_exe_80ms_frame.png"))

    hero_gif_path = os.path.join(ASSETS_DIR, "hero", "lwx-exe-hero.gif")
    save_optimized_gif(frames, hero_gif_path, durations)
    return hero_gif_path


# ============================================================================
# 8. COMPOSITION 02: IDENTITY (6s NORMAL + 6s CORRUPTED + "MOTION DESIGNER")
# ============================================================================
def build_comp_02_identity():
    W, H = 1200, 300
    frames = []
    durations = []

    plates = {}
    for p_mode in ["normal", "corrupted"]:
        is_c = p_mode == "corrupted"
        plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pd = ImageDraw.Draw(plate)
        pd.rectangle([28, 20, 1172, 280], fill=(8, 7, 12, 245) if not is_c else (14, 3, 6, 248))
        pd.rectangle([28, 20, 1172, 280], outline=(138, 0, 24, 255) if not is_c else (255, 15, 43, 255), width=3)
        pd.rectangle([34, 26, 1166, 274], outline=(38, 22, 32, 255) if not is_c else (120, 0, 20, 255), width=2)

        # Mini Green Hill checkered pedestal under Sonic on the left
        for col_i, gx in enumerate(range(54, 342, 24)):
            c_even = (180, 88, 0, 255) if not is_c else (72, 16, 14, 255)
            c_odd = (112, 48, 0, 255) if not is_c else (38, 6, 8, 255)
            pd.rectangle([gx, 232, gx + 23, 258], fill=c_even if col_i % 2 == 0 else c_odd)
        pd.rectangle([54, 222, 342, 233], fill=(40, 200, 0, 255) if not is_c else (196, 8, 28, 255))

        # Divider vertical bar
        pd.rectangle([372, 44, 376, 256], fill=(138, 0, 24, 255) if not is_c else (255, 15, 43, 255))

        # Concise, real professional information ONLY — updated to MOTION DESIGNER
        draw_pixel_text(
            pd,
            412,
            54,
            "EVANDRO",
            scale=5,
            fill=(255, 255, 255, 255) if not is_c else (255, 24, 52, 255),
            shadow=(138, 0, 24, 255) if not is_c else (48, 0, 8, 255),
        )
        draw_pixel_text(
            pd,
            690,
            66,
            "@LLEWXAMDEV",
            scale=3,
            fill=(255, 216, 0, 255) if not is_c else (255, 160, 176, 255),
            shadow=(0, 0, 0, 255),
        )

        pd.rectangle([412, 106, 1128, 110], fill=(184, 0, 28, 255) if not is_c else (255, 15, 43, 255))

        draw_pixel_text(
            pd,
            412,
            128,
            "FULL-STACK DEVELOPER · MOTION DESIGNER",
            scale=3,
            fill=(238, 232, 236, 255) if not is_c else (255, 210, 218, 255),
            shadow=(0, 0, 0, 255),
        )
        draw_pixel_text(
            pd,
            412,
            168,
            "SYSTEMS ANALYSIS AND DEVELOPMENT (ADS)",
            scale=2,
            fill=(172, 162, 170, 255) if not is_c else (210, 130, 145, 255),
            shadow=(0, 0, 0, 255),
        )
        draw_pixel_text(
            pd,
            412,
            204,
            "TS · JS · PYTHON · RUST · NODE.JS · REACT · AE · BLENDER",
            scale=2,
            fill=(76, 156, 255, 255) if not is_c else (255, 64, 92, 255),
            shadow=(0, 0, 0, 255),
        )
        plates[p_mode] = plate

    plates["normal"].save(os.path.join(SRC_DIR, "identity_panel_plate.png"))

    # 24 frames Normal (6.0s) + 1 transition (100ms) + 24 frames Corrupted (6.0s) + 1 transition (100ms)
    id_timeline = []
    for i in range(24):
        id_timeline.append(("normal", False, 250, False))
    id_timeline.append(("blink_closed", False, 100, True))
    for i in range(24):
        id_timeline.append(("exe_full", True, 250, False))
    id_timeline.append(("blink_closed", True, 100, True))

    for f, (mode, is_c, dur_ms, is_trans) in enumerate(id_timeline):
        bg = Image.new("RGBA", (W, H), (5, 3, 6, 255))
        bg.alpha_composite(plates["corrupted" if is_c else "normal"], (0, 0))

        breath = 1 if (f // 2) % 2 == 1 else 0
        wag = f % 4

        sp = render_sonic_character_canvas(mode=mode, breath_offset=breath, wag_phase=wag, upscale=3, style="fullbody")
        bg.alpha_composite(sp, (68, 12))

        if is_trans:
            bg = apply_exe_interference(bg, intensity=0.5, seed=55 + f)

        bg = apply_crt_scanlines(bg, alpha=22)
        frames.append(bg)
        durations.append(dur_ms)

    out_gif = os.path.join(ASSETS_DIR, "identity", "lwx-exe-identity.gif")
    save_optimized_gif(frames, out_gif, durations)
    frames[0].save(os.path.join(ASSETS_DIR, "previews", "identity_preview.png"))
    return out_gif


# ============================================================================
# 9. COMPOSITION 03: DIVIDERS (6s NORMAL + 6s CORRUPTED FOR ALL 3 VARIATIONS)
# ============================================================================
def build_comp_03_dividers():
    W, H = 1200, 76
    # Shared 6s Normal + transition + 6s Corrupted + transition timeline
    div_timeline = [(False, 250, False)] * 24 + [(True, 100, True)] + [(True, 250, False)] * 24 + [(False, 100, True)]

    # --- Variation A: Golden Ring (6s Golden Ring spinning -> 6s Blood Ring spinning) ---
    frames_a, dur_a = [], []
    for f, (is_corr, dur_ms, is_trans) in enumerate(div_timeline):
        img = Image.new("RGBA", (W, H), (5, 3, 5, 255))
        d = ImageDraw.Draw(img)
        line_col = (255, 216, 0, 190) if not is_corr else (255, 15, 43, 240)
        sub_col = (24, 88, 216, 160) if not is_corr else (120, 0, 18, 200)

        d.rectangle([60, H // 2 - 2, 540, H // 2], fill=line_col)
        d.rectangle([660, H // 2 - 2, 1140, H // 2], fill=line_col)
        d.rectangle([120, H // 2 + 4, 540, H // 2 + 5], fill=sub_col)
        d.rectangle([660, H // 2 + 4, 1080, H // 2 + 5], fill=sub_col)

        ring = render_ring_sprite(size=52, phase=(f % 4) / 4.0, corrupted=is_corr)
        img.alpha_composite(ring, (W // 2 - 26, H // 2 - 26))
        if is_trans:
            img = apply_exe_interference(img, intensity=0.55, seed=70 + f)
        dur_a.append(dur_ms)
        frames_a.append(apply_crt_scanlines(img, 20))

    path_a = os.path.join(ASSETS_DIR, "dividers", "divider-golden-ring.gif")
    save_optimized_gif(frames_a, path_a, dur_a)
    frames_a[0].save(os.path.join(SRC_DIR, "divider_a_golden_ring.png"))

    # --- Variation B: Corrupted Ring (6s Golden Segmented Ring -> 6s Crimson Corrupted Ring) ---
    frames_b, dur_b = [], []
    for f, (is_corr, dur_ms, is_trans) in enumerate(div_timeline):
        img = Image.new("RGBA", (W, H), (5, 3, 5, 255))
        d = ImageDraw.Draw(img)
        scatter = 0.65 if is_trans else 0.0
        bar_col = (255, 15, 43, 215) if is_corr else (212, 168, 0, 185)
        for seg_x in range(80, 530, 28):
            d.rectangle([seg_x, H // 2 - 2, seg_x + 18, H // 2 + 1], fill=bar_col)
        for seg_x in range(670, 1120, 28):
            d.rectangle([seg_x, H // 2 - 2, seg_x + 18, H // 2 + 1], fill=bar_col)

        ring = render_ring_sprite(size=52, phase=(f % 4) / 4.0, corrupted=is_corr, scatter=scatter)
        img.alpha_composite(ring, (W // 2 - 26, H // 2 - 26))
        if is_trans:
            img = apply_exe_interference(img, intensity=0.55, seed=170 + f)
        dur_b.append(dur_ms)
        frames_b.append(apply_crt_scanlines(img, 22))

    path_b = os.path.join(ASSETS_DIR, "dividers", "divider-corrupted-ring.gif")
    save_optimized_gif(frames_b, path_b, dur_b)
    frames_b[26].save(os.path.join(SRC_DIR, "divider_b_corrupted_ring.png"))

    # --- Variation C: Green Hill Transition Strip (6s Normal Grass/Soil -> 6s Corrupted Blood Grass/Soil) ---
    frames_c, dur_c = [], []
    for f, (is_corr, dur_ms, is_trans) in enumerate(div_timeline):
        img = Image.new("RGBA", (W, H), (5, 3, 5, 255))
        d = ImageDraw.Draw(img)

        strip_y = 26
        tile = 16
        soil_a = (200, 100, 0, 255) if not is_corr else (58, 18, 12, 255)
        soil_b = (120, 52, 0, 255) if not is_corr else (28, 8, 6, 255)
        grass_hi = (40, 208, 0, 255) if not is_corr else (168, 8, 24, 255)
        grass_mid = (0, 148, 0, 255) if not is_corr else (72, 12, 18, 255)

        for r_i, y in enumerate(range(strip_y, H - 10, tile)):
            for c_i, x in enumerate(range(40, W - 40, tile)):
                d.rectangle(
                    [x, y, x + tile - 1, min(H - 10, y + tile - 1)],
                    fill=soil_a if (r_i + c_i) % 2 == 0 else soil_b,
                )
        d.rectangle([40, strip_y - 8, W - 40, strip_y + 2], fill=grass_hi)
        d.rectangle([40, strip_y + 2, W - 40, strip_y + 7], fill=grass_mid)

        if is_trans:
            img = apply_exe_interference(img, intensity=0.6, seed=290 + f)
        dur_c.append(dur_ms)
        frames_c.append(apply_crt_scanlines(img, 22))

    path_c = os.path.join(ASSETS_DIR, "dividers", "divider-green-hill-transition.gif")
    save_optimized_gif(frames_c, path_c, dur_c)
    frames_c[0].save(os.path.join(SRC_DIR, "divider_c_green_hill.png"))

    return path_a, path_b, path_c


# ============================================================================
# 10. COMPOSITION 04: PROJECTS SHOWCASE & SONIC.EXE MENU BUTTONS
# ============================================================================
REAL_PROJECTS = [
    {
        "slug": "portfolio",
        "title": "LLEWXAM.ME",
        "subtitle": "INTERACTIVE 2.5D WEBGL & CANVAS PORTFOLIO",
        "stack": "TYPESCRIPT · REACT · WEBGL/GLSL · CANVAS 2D",
        "btn_label": "OPEN PORTFOLIO",
        "url": "https://www.llewxam.me",
        "accent": (239, 5, 116),
        "secondary": (36, 148, 165),
        "preview_type": "webgl_city",
    },
    {
        "slug": "aegishub",
        "title": "AEGISHUB",
        "subtitle": "GITHUB REPOSITORY SECURITY ANALYZER",
        "stack": "RUST · TYPESCRIPT · REACT · CLI SCANNER",
        "btn_label": "VIEW AEGISHUB",
        "url": "https://github.com/LlewxamDev/AegisHub",
        "accent": (255, 68, 34),
        "secondary": (49, 120, 198),
        "preview_type": "security_radar",
    },
    {
        "slug": "aegiscore",
        "title": "AEGISCORE",
        "subtitle": "HYBRID WEB-DEFENSE & RISK SCORING PLATFORM",
        "stack": "TYPESCRIPT · RUST · AUTH & SESSION DEFENSE",
        "btn_label": "VIEW AEGISCORE",
        "url": "https://github.com/LlewxamDev/AegisCore",
        "accent": (0, 212, 168),
        "secondary": (196, 36, 68),
        "preview_type": "shield_matrix",
    },
    {
        "slug": "hackerpage",
        "title": "HACKERPAGE",
        "subtitle": "BREACHROOM 3D CYBERSECURITY EXPERIENCE",
        "stack": "THREE.JS · JAVASCRIPT · HTML5 · 3D WEB",
        "btn_label": "VIEW HACKERPAGE",
        "url": "https://github.com/LlewxamDev/HackerPage",
        "accent": (40, 224, 96),
        "secondary": (24, 88, 216),
        "preview_type": "breach_3d",
    },
    {
        "slug": "soullist",
        "title": "SOUL-LIST",
        "subtitle": "1,400+ COMMAND HIGH-SPEED WHATSAPP BOT",
        "stack": "TYPESCRIPT · NODE.JS · BAILEYS WEBSOCKETS",
        "btn_label": "VIEW SOUL-LIST",
        "url": "https://github.com/LlewxamDev/Soul-List",
        "accent": (29, 136, 155),
        "secondary": (255, 216, 0),
        "preview_type": "bot_socket",
    },
    {
        "slug": "polybech",
        "title": "POLYBECH",
        "subtitle": "POLYGLOT ALGORITHM BENCHMARK LABORATORY",
        "stack": "RUST · C++ · ASSEMBLY · PYTHON · TS · C#",
        "btn_label": "VIEW POLYBECH",
        "url": "https://github.com/LlewxamDev/Polybech",
        "accent": (255, 184, 0),
        "secondary": (148, 82, 255),
        "preview_type": "bench_bars",
    },
]


def draw_project_logo_or_preview(
    card_img: Image.Image,
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    slug: str,
    ptype: str,
    acc: tuple[int, int, int],
    sec: tuple[int, int, int],
):
    """
    Draws the static high-resolution project logo (for AegisHub, AegisCore, HackerPage,
    Soul-List, Polybech) or the 2.5D city preview (for llewxam.me, as requested by the user).
    """
    draw.rectangle([x, y, x + w, y + h], fill=(8, 6, 12, 255))
    logo_path = os.path.join(ASSETS_DIR, "projects", "logos", f"logo-{slug}.png")

    if slug != "portfolio" and os.path.exists(logo_path):
        logo_im = Image.open(logo_path).convert("RGBA")
        inner_w, inner_h = w - 8, h - 8
        logo_resized = logo_im.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
        card_img.alpha_composite(logo_resized, (x + 4, y + 4))
    else:
        # 2.5D city skyline + crimson visor beacon for llewxam.me
        draw.rectangle([x + 4, y + 4, x + w - 4, y + h - 4], fill=(14, 10, 24, 255))
        b_widths = [36, 46, 40, 52, 38, 44]
        bx = x + 14
        for idx, bw in enumerate(b_widths):
            bh = 76 + (idx * 31) % 96
            draw.rectangle([bx, y + h - bh - 6, bx + bw - 6, y + h - 6], fill=(24, 20, 38, 255))
            for wy in range(y + h - bh + 8, y + h - 16, 18):
                draw.rectangle([bx + 8, wy, bx + 18, wy + 8], fill=(*sec, 220))
                if bw > 40:
                    draw.rectangle([bx + 24, wy, bx + 34, wy + 8], fill=(*acc, 185))
            bx += bw
        vx, vy = x + w - 68, y + 58
        draw.ellipse([vx - 16, vy - 8, vx + 16, vy + 8], fill=(255, 15, 43, 255))

    draw.rectangle([x, y, x + w, y + h], outline=(*acc, 255), width=3)
    draw.rectangle([x + 3, y + 3, x + w - 3, y + h - 3], outline=(255, 216, 0, 140), width=1)


def render_sonic_exe_menu_button(label: str, out_gif_path: str, out_png_path: str = None, width=320, height=54):
    frames = []
    durations = []
    btn_timeline = [(False, 250, False)] * 24 + [(True, 100, True)] + [(True, 250, False)] * 24 + [(False, 100, True)]
    for f, (is_corr, dur_ms, is_trans) in enumerate(btn_timeline):
        img = Image.new("RGBA", (width, height), (5, 3, 5, 255))
        d = ImageDraw.Draw(img)

        outer_b = (255, 15, 43, 255) if is_corr else (168, 0, 28, 255)
        inner_b = (255, 216, 0, 255) if (f // 2) % 2 == 0 and not is_corr else (255, 24, 52, 255)
        fill_c = (18, 6, 12, 255) if not is_corr else (36, 4, 10, 255)

        d.rectangle([2, 2, width - 3, height - 3], fill=fill_c, outline=outer_b, width=3)
        d.rectangle([7, 7, width - 8, height - 8], outline=inner_b, width=1)

        # Animated pixel selection arrow ►
        ax = 20 + (2 if (f // 2) % 2 == 0 else 0)
        ay = height // 2
        d.polygon([(ax, ay - 7), (ax + 10, ay), (ax, ay + 7)], fill=(255, 216, 0, 255) if not is_corr else (255, 15, 43, 255))

        draw_pixel_text(
            d,
            width // 2 + 8,
            (height - 14) // 2,
            label,
            scale=2,
            fill=(255, 248, 250, 255) if not is_corr else (255, 68, 92, 255),
            shadow=(0, 0, 0, 255),
            align="center",
        )

        if is_trans:
            img = apply_exe_interference(img, intensity=0.5, seed=33 + f)
        durations.append(dur_ms)
        frames.append(apply_crt_scanlines(img, 20))

    save_optimized_gif(frames, out_gif_path, durations)
    if out_png_path:
        frames[0].save(out_png_path)


def build_comp_04_projects():
    # 1. Section Header GIF (COMP_04_PROJECTS, 1200 x 110) — 6s Normal + 6s Corrupted
    W, H = 1200, 110
    h_frames, h_dur = [], []
    hdr_timeline = [(False, 250, False)] * 24 + [(True, 100, True)] + [(True, 250, False)] * 24 + [(False, 100, True)]
    for f, (is_corr, dur_ms, is_trans) in enumerate(hdr_timeline):
        img = Image.new("RGBA", (W, H), (5, 3, 5, 255))
        d = ImageDraw.Draw(img)
        d.rectangle([28, 14, W - 28, H - 14], fill=(12, 6, 10, 255), outline=(168, 0, 28, 255) if not is_corr else (255, 15, 43, 255), width=3)
        d.rectangle([36, 22, W - 36, H - 22], outline=(255, 216, 0, 180) if not is_corr else (138, 0, 22, 255), width=1)

        ring_l = render_ring_sprite(size=36, phase=(f % 4) / 4.0, corrupted=is_corr)
        img.alpha_composite(ring_l, (64, H // 2 - 18))
        img.alpha_composite(ring_l, (W - 100, H // 2 - 18))

        draw_pixel_text(
            d,
            W // 2,
            30,
            "PROJECTS",
            scale=4,
            fill=(255, 216, 0, 255) if not is_corr else (255, 15, 43, 255),
            shadow=(110, 0, 18, 255),
            align="center",
        )
        draw_pixel_text(
            d,
            W // 2,
            68,
            "PUBLIC REPOSITORIES & INTERACTIVE WEB SYSTEMS",
            scale=2,
            fill=(210, 198, 204, 255) if not is_corr else (255, 175, 188, 255),
            shadow=(0, 0, 0, 255),
            align="center",
        )
        if is_trans:
            img = apply_exe_interference(img, intensity=0.55, seed=400 + f)
        h_dur.append(dur_ms)
        h_frames.append(apply_crt_scanlines(img, 22))

    header_gif = os.path.join(ASSETS_DIR, "projects", "projects-header-exe.gif")
    save_optimized_gif(h_frames, header_gif, h_dur)
    h_frames[0].save(os.path.join(SRC_DIR, "projects_header_plate.png"))

    # 2. High-Resolution Static Project Cards (1160 x 380 24-bit PNG) + Menu Buttons
    for idx, proj in enumerate(REAL_PROJECTS):
        CW, CH = 1160, 380
        card = Image.new("RGBA", (CW, CH), (5, 3, 5, 255))
        cd = ImageDraw.Draw(card)

        outer_col = (168, 0, 28, 255)
        inner_col = (255, 216, 0, 220)
        cd.rectangle([8, 8, CW - 9, CH - 9], fill=(11, 7, 11, 255), outline=outer_col, width=5)
        cd.rectangle([18, 18, CW - 19, CH - 19], outline=inner_col, width=2)

        # Top slot header strip
        cd.rectangle([26, 26, CW - 27, 78], fill=(24, 8, 16, 255))
        draw_pixel_text(
            cd,
            44,
            40,
            f"SLOT 0{idx + 1} · {proj['title']}",
            scale=4,
            fill=(255, 216, 0, 255),
            shadow=(0, 0, 0, 255),
        )

        # Left Square High-Res Logo Viewport (264 x 264)
        draw_project_logo_or_preview(
            card,
            cd,
            38,
            94,
            264,
            264,
            proj["slug"],
            proj["preview_type"],
            proj["accent"],
            proj["secondary"],
        )

        # Right Metadata
        rx = 332
        draw_pixel_text(cd, rx, 108, proj["title"], scale=6, fill=(255, 255, 255, 255), shadow=(110, 0, 18, 255))
        draw_pixel_text(cd, rx, 184, proj["subtitle"], scale=2, fill=(224, 214, 220, 255), shadow=(0, 0, 0, 255))
        cd.rectangle([rx, 224, CW - 44, 228], fill=(168, 0, 28, 255))
        draw_pixel_text(cd, rx, 248, proj["stack"], scale=2, fill=(92, 172, 255, 255), shadow=(0, 0, 0, 255))
        draw_pixel_text(
            cd,
            rx,
            302,
            "> SELECT BUTTON BELOW TO OPEN REPOSITORY",
            scale=2,
            fill=(255, 216, 0, 255),
            shadow=(0, 0, 0, 255),
        )

        card_png = os.path.join(ASSETS_DIR, "projects", f"card-{proj['slug']}.png")
        card.save(card_png)

        # Also keep a 580x190 GIF copy for AE project / backward compatibility
        card_small = card.resize((580, 190), Image.Resampling.LANCZOS)
        card_gif = os.path.join(ASSETS_DIR, "projects", f"card-{proj['slug']}.gif")
        save_optimized_gif([card_small], card_gif, [1000])
        if idx == 0:
            card_small.save(os.path.join(SRC_DIR, "project_card_sample.png"))

        btn_gif = os.path.join(ASSETS_DIR, "projects", f"btn-{proj['slug']}.gif")
        render_sonic_exe_menu_button(proj["btn_label"], btn_gif, width=285, height=50)


# ============================================================================
# 11. COMPOSITIONS 05, 06, 07: GREEN HILL ZONE CORRUPTED TECH PANELS (6s / 6s)
# ============================================================================
def render_ghz_tech_panel(
    comp_id: str,
    title: str,
    subtitle: str,
    rows_of_techs: list[tuple[str | None, list[str]]],
    out_gif_path: str,
    src_overlay_name: str,
    height: int = 430,
):
    W, H = 1200, height
    frames, durations = [], []

    # Export clean static monitor overlay for After Effects composition
    for ov_mode in ["normal", "corrupted"]:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        is_c = ov_mode == "corrupted"

        # Classic Sonic Zone Header Signpost Banner
        od.rectangle([38, 16, W - 38, 66], fill=(10, 12, 24, 238) if not is_c else (18, 3, 8, 244))
        od.rectangle([38, 16, W - 38, 66], outline=(255, 216, 0, 255) if not is_c else (255, 15, 43, 255), width=3)
        draw_pixel_text(
            od,
            62,
            28,
            title,
            scale=3,
            fill=(255, 216, 0, 255) if not is_c else (255, 24, 52, 255),
            shadow=(0, 0, 0, 255),
        )
        draw_pixel_text(
            od,
            W - 62,
            34,
            subtitle,
            scale=2,
            fill=(210, 224, 255, 255) if not is_c else (255, 160, 176, 255),
            shadow=(0, 0, 0, 255),
            align="right",
        )

        cur_y = 82
        for row_label, items in rows_of_techs:
            if row_label:
                od.rectangle([44, cur_y, 380, cur_y + 24], fill=(12, 16, 32, 225) if not is_c else (28, 4, 10, 235))
                od.rectangle([44, cur_y, 380, cur_y + 24], outline=(76, 136, 255, 220) if not is_c else (184, 0, 28, 240), width=1)
                draw_pixel_text(
                    od,
                    56,
                    cur_y + 6,
                    row_label,
                    scale=2,
                    fill=(255, 255, 255, 255) if not is_c else (255, 190, 200, 255),
                    shadow=(0, 0, 0, 255),
                )
                cur_y += 32

            n_items = len(items)
            avail_w = W - 88
            gap = 12
            slot_w = min(212, (avail_w - gap * (n_items - 1)) // n_items)
            slot_h = 58
            total_row_w = n_items * slot_w + (n_items - 1) * gap
            start_x = (W - total_row_w) // 2

            for item_i, tech in enumerate(items):
                sx = start_x + item_i * (slot_w + gap)
                draw_sonic_monitor_slot(
                    od,
                    sx,
                    cur_y,
                    slot_w,
                    slot_h,
                    tech,
                    corrupted=is_c,
                    highlight_border=(row_label == "CURRENTLY LEARNING"),
                    canvas_img=ov,
                )
            cur_y += slot_h + 16

        if ov_mode == "normal":
            ov.save(os.path.join(SRC_DIR, src_overlay_name))
        else:
            ov.save(os.path.join(SRC_DIR, src_overlay_name.replace(".png", "_corrupted.png")))

    ov_norm = Image.open(os.path.join(SRC_DIR, src_overlay_name)).convert("RGBA")
    ov_corr = Image.open(os.path.join(SRC_DIR, src_overlay_name.replace(".png", "_corrupted.png"))).convert("RGBA")

    # 24 frames Normal (6.0s) + 1 transition (100ms) + 24 frames Corrupted (6.0s) + 1 transition (100ms)
    tech_timeline = [(False, 250, False)] * 24 + [(True, 100, True)] + [(True, 250, False)] * 24 + [(False, 100, True)]

    for f, (is_corr, dur_ms, is_trans) in enumerate(tech_timeline):
        sway = int(round(math.sin(f * 2 * math.pi / 24.0) * 3))
        cloud_dx = int((f * 5) % 640)

        canvas = render_ghz_sky_layer(W, H, corrupted=is_corr, cloud_shift=cloud_dx)
        mtn = render_ghz_mountains_and_water_layer(W, H, corrupted=is_corr, water_phase=f)
        fg = render_ghz_palms_and_ground_layer(W, H, corrupted=is_corr, sway_px=sway, include_critters=is_corr)
        canvas = Image.alpha_composite(canvas, mtn)
        canvas = Image.alpha_composite(canvas, fg)

        # Subtle atmospheric dark vignette over middle area so monitors have maximum contrast
        vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        vd = ImageDraw.Draw(vig)
        vd.rectangle([32, 74, W - 32, H - 72], fill=(6, 8, 18, 92) if not is_corr else (16, 2, 6, 130))
        canvas = Image.alpha_composite(canvas, vig)

        # Composite Sonic Item Monitors overlay
        canvas = Image.alpha_composite(canvas, ov_corr if is_corr else ov_norm)

        # Floating Golden/Corrupted Rings on the Green Hill ground corners
        for r_idx, rx in enumerate([132, W - 164]):
            ring_sp = render_ring_sprite(size=30, phase=((f + r_idx) % 4) / 4.0, corrupted=is_corr)
            canvas.alpha_composite(ring_sp, (rx, H - 52))

        if is_trans:
            canvas = apply_exe_interference(canvas, intensity=0.55, seed=700 + f)

        canvas = apply_crt_scanlines(canvas, alpha=18 if not is_corr else 28)
        frames.append(canvas)
        durations.append(dur_ms)

    save_optimized_gif(frames, out_gif_path, durations)
    frames[0].save(os.path.join(ASSETS_DIR, "green-hill", f"{comp_id.lower()}_normal.png"))
    frames[26].save(os.path.join(ASSETS_DIR, "green-hill", f"{comp_id.lower()}_corrupted.png"))


def build_comp_05_06_07_technologies():
    # COMP_05_TECH_LANGUAGES (Exact 11 languages from crimson-toolkit.svg)
    render_ghz_tech_panel(
        comp_id="COMP_05_TECH_LANGUAGES",
        title="GREEN HILL ZONE · ACT 1",
        subtitle="LANGUAGES",
        rows_of_techs=[
            ("WORKING KNOWLEDGE", ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "PHP", "LUA"]),
            ("CURRENTLY LEARNING", ["JAVA", "C++", "C#", "RUST", "KOTLIN", "ASSEMBLY"]),
        ],
        out_gif_path=os.path.join(ASSETS_DIR, "technologies", "tech-languages-ghz.gif"),
        src_overlay_name="tech_monitors_languages_overlay.png",
        height=430,
    )

    # COMP_06_TECH_ECOSYSTEM (Exact 13 frameworks/tools from crimson-ecosystem.svg — 5 + 4 + 4 layout)
    render_ghz_tech_panel(
        comp_id="COMP_06_TECH_ECOSYSTEM",
        title="GREEN HILL ZONE · ACT 2",
        subtitle="JAVASCRIPT & TYPESCRIPT ECOSYSTEM",
        rows_of_techs=[
            (None, ["NODE.JS", "REACT", "NEXT.JS", "VUE", "NUXT"]),
            (None, ["ANGULAR", "SVELTE", "ASTRO", "EXPRESS"]),
            (None, ["NESTJS", "VITE", "TAILWIND", "FASTIFY"]),
        ],
        out_gif_path=os.path.join(ASSETS_DIR, "technologies", "tech-ecosystem-ghz.gif"),
        src_overlay_name="tech_monitors_ecosystem_overlay.png",
        height=420,
    )

    # COMP_07_TECH_TOOLS (Exact 15 web/data/creative tools from crimson-tools.svg — 5 + 5 + 5 layout)
    render_ghz_tech_panel(
        comp_id="COMP_07_TECH_TOOLS",
        title="GREEN HILL ZONE · ACT 3",
        subtitle="WEB · DATA · DEVOPS · CREATIVE TOOLS",
        rows_of_techs=[
            (None, ["HTML5", "CSS3", "POSTGRES", "MYSQL", "SQL SERVER"]),
            (None, ["DOCKER", "GIT", "GITHUB", "LINUX", "VS CODE"]),
            (None, ["VISUAL STUDIO", "BLENDER", "AFTER EFFECTS", "PHOTOSHOP", "HOUDINI"]),
        ],
        out_gif_path=os.path.join(ASSETS_DIR, "technologies", "tech-tools-ghz.gif"),
        src_overlay_name="tech_monitors_tools_overlay.png",
        height=420,
    )


# ============================================================================
# 12. COMPOSITION 08 (TROPHY HEADER) & COMPOSITION 09 (FOOTER + BUTTONS)
# ============================================================================
def build_comp_08_trophy_header():
    W, H = 1200, 110
    frames, durations = [], []
    hdr_timeline = [(False, 250, False)] * 24 + [(True, 100, True)] + [(True, 250, False)] * 24 + [(False, 100, True)]
    for f, (is_corr, dur_ms, is_trans) in enumerate(hdr_timeline):
        img = Image.new("RGBA", (W, H), (5, 3, 5, 255))
        d = ImageDraw.Draw(img)
        d.rectangle([28, 14, W - 28, H - 14], fill=(12, 6, 10, 255), outline=(168, 0, 28, 255) if not is_corr else (255, 15, 43, 255), width=3)
        d.rectangle([36, 22, W - 36, H - 22], outline=(255, 216, 0, 190) if not is_corr else (138, 0, 22, 255), width=1)

        ring = render_ring_sprite(size=36, phase=(f % 4) / 4.0, corrupted=is_corr)
        img.alpha_composite(ring, (64, H // 2 - 18))
        img.alpha_composite(ring, (W - 100, H // 2 - 18))

        draw_pixel_text(
            d,
            W // 2,
            28,
            "TROPHY SELECTION",
            scale=4,
            fill=(255, 216, 0, 255) if not is_corr else (255, 15, 43, 255),
            shadow=(110, 0, 18, 255),
            align="center",
        )
        draw_pixel_text(
            d,
            W // 2,
            68,
            "LIVE GITHUB ACHIEVEMENTS · ORIGINAL RANK THRESHOLDS",
            scale=2,
            fill=(210, 198, 204, 255) if not is_corr else (255, 175, 188, 255),
            shadow=(0, 0, 0, 255),
            align="center",
        )

        if is_trans:
            img = apply_exe_interference(img, intensity=0.55, seed=900 + f)
        durations.append(dur_ms)
        frames.append(apply_crt_scanlines(img, 22))

    out_gif = os.path.join(ASSETS_DIR, "trophies", "trophy-header-exe.gif")
    save_optimized_gif(frames, out_gif, durations)
    frames[0].save(os.path.join(SRC_DIR, "trophy_header_plate.png"))


def build_comp_09_footer():
    # Compact Footer Banner (1200 x 84) + 3 Clickable Menu Buttons (GITHUB, PORTFOLIO, LINKEDIN)
    W, H = 1200, 84
    frames, durations = [], []
    ftr_timeline = [(False, 250, False)] * 24 + [(True, 100, True)] + [(True, 250, False)] * 24 + [(False, 100, True)]
    for f, (is_corr, dur_ms, is_trans) in enumerate(ftr_timeline):
        img = Image.new("RGBA", (W, H), (5, 3, 5, 255))
        d = ImageDraw.Draw(img)

        # Classic Green Hill checkered bottom trim
        for c_i, x in enumerate(range(28, W - 28, 20)):
            c_even = (180, 88, 0, 255) if not is_corr else (72, 16, 14, 255)
            c_odd = (112, 48, 0, 255) if not is_corr else (38, 6, 8, 255)
            d.rectangle([x, H - 22, min(W - 28, x + 19), H - 10], fill=c_even if c_i % 2 == 0 else c_odd)
        d.rectangle([28, H - 28, W - 28, H - 21], fill=(40, 200, 0, 255) if not is_corr else (184, 0, 28, 255))

        draw_pixel_text(
            d,
            W // 2,
            22,
            "EVANDRO · @LLEWXAMDEV",
            scale=3,
            fill=(242, 236, 238, 255) if not is_corr else (255, 15, 43, 255),
            shadow=(0, 0, 0, 255),
            align="center",
        )
        if is_trans:
            img = apply_exe_interference(img, intensity=0.5, seed=950 + f)
        durations.append(dur_ms)
        frames.append(apply_crt_scanlines(img, 20))

    out_gif = os.path.join(ASSETS_DIR, "footer", "footer-banner-exe.gif")
    save_optimized_gif(frames, out_gif, durations)
    frames[0].save(os.path.join(SRC_DIR, "footer_banner_plate.png"))

    # 3 Clickable Sonic.EXE Menu Buttons for Footer (Section 12: GitHub, Portfolio, LinkedIn ONLY)
    render_sonic_exe_menu_button(
        "GITHUB",
        os.path.join(ASSETS_DIR, "footer", "btn-github.gif"),
        os.path.join(SRC_DIR, "btn_footer_github.png"),
        width=280,
        height=52,
    )
    render_sonic_exe_menu_button(
        "PORTFOLIO",
        os.path.join(ASSETS_DIR, "footer", "btn-portfolio.gif"),
        os.path.join(SRC_DIR, "btn_footer_portfolio.png"),
        width=280,
        height=52,
    )
    render_sonic_exe_menu_button(
        "LINKEDIN",
        os.path.join(ASSETS_DIR, "footer", "btn-linkedin.gif"),
        os.path.join(SRC_DIR, "btn_footer_linkedin.png"),
        width=280,
        height=52,
    )


def build_displacement_and_utility_plates():
    # Glitch displacement map for After Effects ADBE Displacement Map
    W, H = 1200, 440
    disp = Image.new("RGBA", (W, H), (128, 128, 128, 255))
    dd = ImageDraw.Draw(disp)
    rng = random.Random(2011)
    for _ in range(36):
        y = rng.randint(0, H - 16)
        h = rng.randint(4, 18)
        val = rng.choice([24, 64, 192, 236])
        dd.rectangle([0, y, W, y + h], fill=(val, 128, 255 - val, 255))
    disp.save(os.path.join(SRC_DIR, "glitch_displacement_map.png"))


if __name__ == "__main__":
    print("[1/6] Building displacement & utility source plates...")
    build_displacement_and_utility_plates()
    print("[2/6] Building COMP_01_HERO (Normal Sonic / 80ms Sonic.EXE loop)...")
    build_comp_01_hero()
    print("[3/6] Building COMP_02_IDENTITY (Sonic idle + real dev identity)...")
    build_comp_02_identity()
    print("[4/6] Building COMP_03_DIVIDERS (Golden Ring, Corrupted Ring, Green Hill Transition)...")
    build_comp_03_dividers()
    print("[5/6] Building COMP_04_PROJECTS & COMP_05..07_TECHNOLOGIES (Green Hill Zone Corrupted)...")
    build_comp_04_projects()
    build_comp_05_06_07_technologies()
    print("[6/6] Building COMP_08_TROPHY_SELECTION Header & COMP_09_FOOTER...")
    build_comp_08_trophy_header()
    build_comp_09_footer()
    print("DONE: All source plates and animated GIFs generated successfully.")
