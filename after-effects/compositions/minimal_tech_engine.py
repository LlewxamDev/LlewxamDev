#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLEW MINIMAL TECH SHOWCASE — GRAPHIC DESIGN (PHOTOSHOP PLATES) & MOTION COMPOSITING ENGINE
==========================================================================================
Direction: "Minimal Tech Showcase — Clean Tech (Sophisticated Crimson & Obsidian Edition)"
Palette:
  - Obsidian Void:     #09090C (RGB 9, 9, 12)
  - Graphite Surface:  #111116 (RGB 17, 17, 22)
  - Graphite Elevated: #181820 (RGB 24, 24, 32)
  - Graphite Border:   #262632 (RGB 38, 38, 50)
  - Crimson Primary:   #E11D48 (RGB 225, 29, 72)
  - Crimson Bright:    #FF2A55 (RGB 255, 42, 85)
  - Crimson Deep:      #881337 (RGB 136, 19, 55)
  - Alabaster White:   #F4F4F6 (RGB 244, 244, 246)
  - Technical Silver:  #A1A1AA (RGB 161, 161, 170)
  - Muted Slate:       #71717A (RGB 113, 113, 122)
"""

import os
import math
import base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ROOT_WORKSPACE = os.path.abspath(os.path.join(BASE_DIR, ".."))
AE_DIR = os.path.join(BASE_DIR, "after-effects")
SRC_MIN_DIR = os.path.join(AE_DIR, "assets-source-minimal")
LOGOS_DIR = os.path.join(AE_DIR, "assets-source", "tech_logos")
PROJ_LOGOS_DIR = os.path.join(BASE_DIR, "assets", "projects", "logos")
RENDERS_DIR = os.path.join(AE_DIR, "renders")
MINIMAL_ASSETS_DIR = os.path.join(BASE_DIR, "assets", "minimal")
PS_DIR = os.path.join(BASE_DIR, "photoshop")

for d in [SRC_MIN_DIR, RENDERS_DIR, MINIMAL_ASSETS_DIR, PS_DIR]:
    os.makedirs(d, exist_ok=True)

# Color Constants
C_OBSIDIAN = (9, 9, 12, 255)
C_GRAPHITE = (16, 16, 22, 255)
C_ELEVATED = (23, 23, 31, 255)
C_BORDER = (38, 38, 50, 255)
C_CRIMSON = (225, 29, 72, 255)
C_CRIMSON_HI = (255, 46, 92, 255)
C_CRIMSON_DEEP = (125, 16, 48, 255)
C_WHITE = (244, 244, 246, 255)
C_SILVER = (168, 168, 179, 255)
C_MUTED = (113, 113, 126, 255)
C_EMERALD = (16, 185, 129, 255)


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono:
        candidates = [
            r"C:\Windows\Fonts\consolab.ttf" if bold else r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\courbd.ttf" if bold else r"C:\Windows\Fonts\cour.ttf",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def ease_in_out_sine(t: float) -> float:
    return -(math.cos(math.pi * t) - 1.0) / 2.0


def load_logo_rgba(folder: str, filename: str, target_size: tuple) -> Image.Image:
    p = os.path.join(folder, filename)
    if not os.path.exists(p):
        return Image.new("RGBA", target_size, (0, 0, 0, 0))
    img = Image.open(p).convert("RGBA")
    img.thumbnail(target_size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    ox = (target_size[0] - img.width) // 2
    oy = (target_size[1] - img.height) // 2
    canvas.paste(img, (ox, oy), img)
    return canvas


def encode_file_base64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def save_fast_gif(rgb_frames: list, out_path: str, fps: int, colors: int = 96):
    """Quantizes frames against a clean shared palette so GIFs stay small (< 650 KB) and sharp."""
    master_pal = rgb_frames[0].quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q_frames = [
        fr.quantize(palette=master_pal, dither=Image.Dither.NONE)
        for fr in rgb_frames
    ]
    q_frames[0].save(
        out_path,
        save_all=True,
        append_images=q_frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )


# ============================================================================
# 1. HERO BANNER PLATES & ANIMATION (1200 x 340, 18fps, 54 frames = 3.0s loop)
# ============================================================================
HERO_W, HERO_H = 1200, 340
HERO_FPS = 18
HERO_FRAMES = 54

CIRCUIT_PATHS = [
    [(640, 48), (740, 48), (780, 88), (940, 88), (975, 53), (1140, 53)],
    [(680, 125), (810, 125), (845, 160), (1020, 160), (1060, 120), (1165, 120)],
    [(620, 215), (755, 215), (790, 180), (915, 180), (955, 220), (1130, 220)],
    [(710, 285), (860, 285), (895, 250), (1045, 250), (1080, 285), (1175, 285)],
    [(830, 20), (830, 70), (865, 105), (990, 105)],
    [(930, 320), (930, 270), (965, 235), (1110, 235)],
    [(540, 295), (630, 295), (660, 265), (745, 265)],
]

CONSTELLATION_NODES = [
    (740, 72, 14.0, 10.0, 0.0, 3.0),
    (835, 58, -12.0, 14.0, 1.1, 2.5),
    (920, 118, 14.0, -12.0, 2.3, 3.5),
    (1035, 78, -15.0, 10.0, 0.7, 2.8),
    (1125, 108, 10.0, 15.0, 3.5, 2.6),
    (775, 168, -13.0, -10.0, 1.9, 3.2),
    (885, 198, 16.0, 12.0, 4.2, 3.6),
    (985, 172, -14.0, 14.0, 2.8, 2.8),
    (1085, 195, 12.0, -14.0, 5.1, 3.4),
    (725, 255, 12.0, 9.0, 0.4, 2.5),
    (845, 272, -14.0, -12.0, 3.1, 3.0),
    (960, 268, 12.0, 12.0, 1.5, 3.5),
    (1065, 275, -10.0, 12.0, 4.7, 2.8),
    (1148, 242, 9.0, -10.0, 2.1, 2.4),
]


def point_along_polyline(pts, progress: float):
    segs = []
    total_len = 0.0
    for i in range(len(pts) - 1):
        dx = pts[i + 1][0] - pts[i][0]
        dy = pts[i + 1][1] - pts[i][1]
        d = math.hypot(dx, dy)
        segs.append((pts[i], pts[i + 1], d))
        total_len += d
    if total_len <= 1e-5:
        return pts[0]
    target = (progress % 1.0) * total_len
    acc = 0.0
    for p0, p1, d in segs:
        if acc + d >= target:
            local_t = (target - acc) / max(1e-5, d)
            return (
                p0[0] + (p1[0] - p0[0]) * local_t,
                p0[1] + (p1[1] - p0[1]) * local_t,
            )
        acc += d
    return pts[-1]


def build_hero_plates_and_gif():
    bg_inner = Image.new("RGBA", (HERO_W, HERO_H), C_OBSIDIAN)
    bg_draw = ImageDraw.Draw(bg_inner)

    for gx in range(0, HERO_W, 32):
        alpha = 14 if gx % 128 != 0 else 24
        bg_draw.line([(gx, 0), (gx, HERO_H)], fill=(45, 45, 60, alpha), width=1)
    for gy in range(0, HERO_H, 32):
        alpha = 14 if gy % 128 != 0 else 24
        bg_draw.line([(0, gy), (HERO_W, gy)], fill=(45, 45, 60, alpha), width=1)

    glow_layer = Image.new("RGBA", (HERO_W, HERO_H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    g_draw.ellipse([680, -60, 1240, 400], fill=(190, 18, 60, 38))
    g_draw.ellipse([820, 40, 1140, 300], fill=(225, 29, 72, 30))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=52))
    bg_inner = Image.alpha_composite(bg_inner, glow_layer)

    frame_draw = ImageDraw.Draw(bg_inner)
    frame_draw.rectangle([0, 0, HERO_W - 1, HERO_H - 1], outline=(42, 42, 56, 255), width=2)
    frame_draw.rectangle([0, 0, 5, HERO_H - 1], fill=C_CRIMSON)
    for tx in range(1060, 1170, 18):
        frame_draw.line([(tx, 16), (tx + 8, 16)], fill=(225, 29, 72, 140), width=2)

    bg_inner.save(os.path.join(SRC_MIN_DIR, "hero_bg_obsidian_plate.png"))

    circuit_plate = Image.new("RGBA", (HERO_W, HERO_H), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(circuit_plate)
    for path in CIRCUIT_PATHS:
        c_draw.line(path, fill=(48, 48, 66, 175), width=2)
        for pt in (path[0], path[-1]):
            x, y = pt
            c_draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(18, 18, 26, 255), outline=(140, 25, 58, 200), width=2)
    circuit_plate.save(os.path.join(SRC_MIN_DIR, "hero_circuit_traces_plate.png"))

    typo_plate = Image.new("RGBA", (HERO_W, HERO_H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(typo_plate)

    f_tag = load_font(12, bold=True, mono=True)
    f_name = load_font(42, bold=True, mono=False)
    f_role = load_font(17, bold=True, mono=False)
    f_bio = load_font(14, bold=False, mono=False)
    f_pill = load_font(12, bold=True, mono=True)

    t_draw.rectangle([48, 42, 56, 54], fill=C_CRIMSON)
    t_draw.text((66, 40), "LLEWXAMDEV  //  SYSTEMS & SOFTWARE ENGINEERING", font=f_tag, fill=C_CRIMSON_HI)
    t_draw.text((48, 68), "Evandro Silva Amorim", font=f_name, fill=C_WHITE)

    y_role = 128
    rx = 48
    role_segments = [
        ("Desenvolvimento de Sistemas", C_WHITE),
        ("   ·   ", C_CRIMSON_HI),
        ("Software", C_WHITE),
        ("   ·   ", C_CRIMSON_HI),
        ("Automação", C_WHITE),
    ]
    for seg_text, seg_col in role_segments:
        t_draw.text((rx, y_role), seg_text, font=f_role, fill=seg_col)
        bbox = t_draw.textbbox((rx, y_role), seg_text, font=f_role)
        rx = bbox[2]

    t_draw.line([(48, 164), (580, 164)], fill=(45, 45, 62, 255), width=1)
    t_draw.line([(48, 164), (136, 164)], fill=C_CRIMSON, width=2)

    t_draw.text(
        (48, 180),
        "Arquitetura de back-end, motores de segurança, automações de alta velocidade",
        font=f_bio,
        fill=C_SILVER,
    )
    t_draw.text(
        (48, 202),
        "e aplicações web interativas orientadas a performance e código limpo.",
        font=f_bio,
        fill=C_SILVER,
    )

    hero_chips = ["TypeScript", "Python", "Rust", "Node.js", "NestJS", "Fastify", "React"]
    cx = 48
    cy = 256
    for chip in hero_chips:
        tb = t_draw.textbbox((0, 0), chip, font=f_pill)
        cw = (tb[2] - tb[0]) + 24
        ch = 28
        t_draw.rounded_rectangle(
            [cx, cy, cx + cw, cy + ch],
            radius=4,
            fill=(20, 20, 28, 240),
            outline=(52, 52, 70, 255),
            width=1,
        )
        t_draw.rectangle([cx, cy + 6, cx + 2, cy + ch - 6], fill=C_CRIMSON)
        t_draw.text((cx + 12, cy + 7), chip, font=f_pill, fill=C_WHITE)
        cx += cw + 10

    typo_plate.save(os.path.join(SRC_MIN_DIR, "hero_typography_plate.png"))

    frames = []
    for f_idx in range(HERO_FRAMES):
        t_norm = f_idx / float(HERO_FRAMES)
        angle = 2.0 * math.pi * t_norm

        frame = Image.alpha_composite(bg_inner.copy(), circuit_plate)
        overlay = Image.new("RGBA", (HERO_W, HERO_H), (0, 0, 0, 0))
        o_draw = ImageDraw.Draw(overlay)

        for p_i, path in enumerate(CIRCUIT_PATHS):
            prog = (t_norm + p_i * 0.17) % 1.0
            for step in range(6):
                sub_p = (prog - step * 0.014) % 1.0
                px, py = point_along_polyline(path, sub_p)
                alpha = int(210 * (1.0 - step / 6.0))
                r = 2.5 if step == 0 else 1.8
                col = (255, 55, 100, alpha) if step < 2 else (225, 29, 72, alpha)
                o_draw.ellipse([px - r, py - r, px + r, py + r], fill=col)

        live_nodes = []
        for (nx, ny, ax, ay, phase, rad) in CONSTELLATION_NODES:
            px = nx + math.sin(angle + phase) * ax
            py = ny + math.cos(angle + phase * 1.3) * ay
            live_nodes.append((px, py, rad, phase))

        for i in range(len(live_nodes)):
            x1, y1, _, _ = live_nodes[i]
            for j in range(i + 1, len(live_nodes)):
                x2, y2, _, _ = live_nodes[j]
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist < 155.0:
                    strength = 1.0 - (dist / 155.0)
                    line_alpha = int(125 * (strength ** 1.4))
                    o_draw.line([(x1, y1), (x2, y2)], fill=(215, 32, 74, line_alpha), width=1)

        for (px, py, rad, phase) in live_nodes:
            pulse = 0.65 + 0.35 * math.sin(angle * 2.0 + phase)
            halo_r = rad * 2.8
            o_draw.ellipse(
                [px - halo_r, py - halo_r, px + halo_r, py + halo_r],
                fill=(225, 29, 72, int(42 * pulse)),
            )
            o_draw.ellipse(
                [px - rad, py - rad, px + rad, py + rad],
                fill=(255, 60, 105, int(230 * pulse)),
            )
            o_draw.ellipse(
                [px - 1.2, py - 1.2, px + 1.2, py + 1.2],
                fill=(255, 240, 245, 255),
            )

        frame = Image.alpha_composite(frame, overlay)
        frame = Image.alpha_composite(frame, typo_plate)

        if f_idx == 0:
            frame.save(os.path.join(SRC_MIN_DIR, "hero_master_preview.png"))
        frames.append(frame.convert("RGB"))

    gif_path = os.path.join(MINIMAL_ASSETS_DIR, "hero-banner.gif")
    save_fast_gif(frames, gif_path, HERO_FPS, colors=64)
    print(f"[OK] Hero Banner generated: {gif_path} ({os.path.getsize(gif_path) // 1024} KB)")


# ============================================================================
# 2. FEATURED PROJECT LIVE DEMO GIFS (640 x 360, 16fps, 48 frames = 3.0s loop)
# ============================================================================
DEMO_W, DEMO_H = 640, 360
DEMO_FPS = 16
DEMO_FRAMES = 48


def create_demo_base_frame(title: str, subtitle: str, tag: str, logo_file: str = None) -> Image.Image:
    base = Image.new("RGBA", (DEMO_W, DEMO_H), C_OBSIDIAN)
    draw = ImageDraw.Draw(base)

    for gx in range(0, DEMO_W, 24):
        draw.line([(gx, 0), (gx, DEMO_H)], fill=(36, 36, 48, 14), width=1)
    for gy in range(0, DEMO_H, 24):
        draw.line([(0, gy), (DEMO_W, gy)], fill=(36, 36, 48, 14), width=1)

    draw.rectangle([0, 0, DEMO_W - 1, 52], fill=C_GRAPHITE)
    draw.line([(0, 52), (DEMO_W, 52)], fill=C_BORDER, width=1)
    draw.rectangle([0, 0, 4, DEMO_H], fill=C_CRIMSON)

    text_x = 20
    if logo_file:
        logo_img = load_logo_rgba(PROJ_LOGOS_DIR, logo_file, (32, 32))
        base.paste(logo_img, (18, 10), logo_img)
        text_x = 60

    f_title = load_font(15, bold=True)
    f_sub = load_font(11, bold=False, mono=True)
    f_tag = load_font(10, bold=True, mono=True)

    draw.text((text_x, 9), title, font=f_title, fill=C_WHITE)
    draw.text((text_x, 29), subtitle, font=f_sub, fill=C_SILVER)

    tb = draw.textbbox((0, 0), tag, font=f_tag)
    tw = (tb[2] - tb[0]) + 18
    draw.rounded_rectangle(
        [DEMO_W - tw - 16, 14, DEMO_W - 16, 38],
        radius=4,
        fill=(32, 14, 24, 255),
        outline=C_CRIMSON_DEEP,
        width=1,
    )
    draw.text((DEMO_W - tw - 7, 20), tag, font=f_tag, fill=C_CRIMSON_HI)
    draw.rectangle([0, 0, DEMO_W - 1, DEMO_H - 1], outline=C_BORDER, width=1)
    return base


def build_demo_aegiscore():
    base = create_demo_base_frame(
        "AegisCore  ·  Hybrid Web-Defense Engine",
        "Fastify API Gateway  +  Rust Native Risk-Scoring Crates",
        "TS + RUST + FASTIFY",
        "logo-aegiscore.png",
    )

    f_mono_b = load_font(11, bold=True, mono=True)
    f_mono = load_font(11, bold=False, mono=True)
    f_num = load_font(22, bold=True, mono=True)
    f_lbl = load_font(10, bold=True, mono=True)

    requests_data = [
        ("POST /api/v1/auth/session", "ip:192.0.2.14 · tls:1.3", 0.06, "ALLOW", "0.9ms", C_EMERALD),
        ("GET  /api/v1/user/profile", "sid:aeg_8f92c · csrf:ok", 0.04, "ALLOW", "0.7ms", C_EMERALD),
        ("POST /api/v1/upload/asset", "mime:image/png · guard:ok", 0.14, "ALLOW", "1.4ms", C_EMERALD),
        ("POST /api/v1/auth/callback", "payload:UNION SELECT *--", 0.94, "BLOCK", "0.6ms", C_CRIMSON_HI),
        ("GET  /api/v1/admin/export", "rate_burst:142/s · anomaly", 0.89, "BLOCK", "0.5ms", C_CRIMSON_HI),
    ]

    frames = []
    for f_idx in range(DEMO_FRAMES):
        t = f_idx / float(DEMO_FRAMES)
        fr = base.copy()
        d = ImageDraw.Draw(fr)

        stages = ["1. Fastify Edge", "2. Payload Normalizer", "3. Rust Risk Crate", "4. Policy Engine"]
        active_stage = int((t * 8.0) % 4)
        for s_i, st_name in enumerate(stages):
            sx = 18 + s_i * 154
            sy = 66
            is_act = s_i == active_stage
            d.rounded_rectangle(
                [sx, sy, sx + 142, sy + 34],
                radius=4,
                fill=(34, 14, 24, 255) if is_act else C_ELEVATED,
                outline=C_CRIMSON if is_act else C_BORDER,
                width=1,
            )
            d.text((sx + 10, sy + 10), st_name, font=f_lbl, fill=C_WHITE if is_act else C_SILVER)
            if s_i < 3:
                d.line([(sx + 143, sy + 17), (sx + 153, sy + 17)], fill=C_CRIMSON if is_act else C_BORDER, width=2)

        d.rounded_rectangle([18, 114, 428, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((30, 124), "LIVE HTTP INSPECTION & RUST FFI RISK SCORING", font=f_lbl, fill=C_SILVER)
        d.line([(18, 144), (428, 144)], fill=C_BORDER, width=1)

        highlight_row = int(t * len(requests_data)) % len(requests_data)
        for r_i, (route, meta, score, action, lat, col) in enumerate(requests_data):
            ry = 154 + r_i * 36
            is_hi = r_i == highlight_row
            if is_hi:
                d.rectangle([22, ry - 3, 424, ry + 29], fill=(28, 16, 24, 255))
                d.rectangle([22, ry - 3, 25, ry + 29], fill=col)

            d.text((32, ry), route, font=f_mono_b, fill=C_WHITE)
            d.text((32, ry + 14), meta, font=f_mono, fill=C_MUTED)

            bar_x = 246
            bar_w = 78
            d.rectangle([bar_x, ry + 8, bar_x + bar_w, ry + 16], fill=(28, 28, 38, 255))
            anim_fill = score * (0.85 + 0.15 * math.sin(t * 2 * math.pi + r_i))
            d.rectangle([bar_x, ry + 8, bar_x + int(bar_w * anim_fill), ry + 16], fill=col)

            d.text((334, ry + 5), f"{score:.2f}", font=f_mono_b, fill=col)
            d.text((374, ry + 5), action, font=f_mono_b, fill=col)

        d.rounded_rectangle([442, 114, 622, 222], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((454, 124), "MEDIAN LATENCY (FFI)", font=f_lbl, fill=C_SILVER)
        lat_val = 0.78 + 0.06 * math.sin(t * 2 * math.pi)
        d.text((454, 148), f"{lat_val:.2f} ms", font=f_num, fill=C_WHITE)
        d.text((454, 184), "Zero-copy Rust parser", font=f_mono, fill=C_EMERALD)
        d.text((454, 200), "Redis Sliding Window", font=f_mono, fill=C_MUTED)

        d.rounded_rectangle([442, 234, 622, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((454, 244), "THREAT MITIGATION", font=f_lbl, fill=C_SILVER)
        d.text((454, 268), "99.4%", font=f_num, fill=C_CRIMSON_HI)
        d.text((454, 304), "SQLi / XSS / CSRF Guard", font=f_mono, fill=C_SILVER)
        d.text((454, 320), "13 Modular Packages", font=f_mono, fill=C_MUTED)

        if f_idx == 0:
            fr.save(os.path.join(SRC_MIN_DIR, "demo_aegiscore_plate.png"))
        frames.append(fr.convert("RGB"))

    out_gif = os.path.join(MINIMAL_ASSETS_DIR, "demo-aegiscore.gif")
    save_fast_gif(frames, out_gif, DEMO_FPS, colors=64)
    print(f"[OK] AegisCore Demo generated: {out_gif} ({os.path.getsize(out_gif) // 1024} KB)")


def build_demo_aegishub():
    base = create_demo_base_frame(
        "AegisHub  ·  GitHub Repository Security Analyzer",
        "Rust Static Analysis Core  +  Fastify/BullMQ  +  React Dashboard",
        "RUST + FASTIFY + REACT",
        "logo-aegishub.png",
    )

    f_mono_b = load_font(11, bold=True, mono=True)
    f_mono = load_font(11, bold=False, mono=True)
    f_score = load_font(28, bold=True, mono=True)
    f_lbl = load_font(10, bold=True, mono=True)

    scan_items = [
        ("[AST-01]", "Secret & Token Entropy Scanner", "0 leaks found", C_EMERALD),
        ("[DEP-02]", "Cargo.lock & package-lock CVE Audit", "42 deps clean", C_EMERALD),
        ("[SAST-3]", "Unsafe Shell / Eval Injection Check", "Verified safe", C_EMERALD),
        ("[CI-04] ", "GitHub Actions Workflow Permissions", "Hardened (Read-Only)", C_CRIMSON_HI),
    ]

    frames = []
    for f_idx in range(DEMO_FRAMES):
        t = f_idx / float(DEMO_FRAMES)
        fr = base.copy()
        d = ImageDraw.Draw(fr)

        d.rounded_rectangle([18, 68, 418, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((30, 78), "$ aegishub scan --repo LlewxamDev/AegisCore --deep", font=f_mono_b, fill=C_CRIMSON_HI)
        d.line([(18, 98), (418, 98)], fill=C_BORDER, width=1)

        prog = 0.72 + 0.28 * ease_in_out_sine(math.sin(t * math.pi))
        d.text((30, 108), f"Rust Core Walker: 184 files analyzed ({int(prog * 100)}%)", font=f_mono, fill=C_SILVER)
        d.rectangle([30, 128, 404, 136], fill=(28, 28, 38, 255))
        d.rectangle([30, 128, 30 + int(374 * prog), 136], fill=C_CRIMSON)

        for idx, (code, name, status, col) in enumerate(scan_items):
            iy = 154 + idx * 44
            d.rounded_rectangle([28, iy, 406, iy + 36], radius=4, fill=C_ELEVATED, outline=C_BORDER, width=1)
            d.text((38, iy + 6), f"{code} {name}", font=f_mono_b, fill=C_WHITE)
            d.text((38, iy + 20), f"Status: {status}", font=f_mono, fill=col)

        d.rounded_rectangle([432, 68, 622, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((448, 78), "SECURITY SCORE", font=f_lbl, fill=C_SILVER)

        cx, cy, r = 527, 165, 52
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(38, 38, 52, 255), width=8)
        arc_deg = int(345 * (0.92 + 0.04 * math.sin(t * 2 * math.pi)))
        d.arc([cx - r, cy - r, cx + r, cy + r], start=-90, end=-90 + arc_deg, fill=C_CRIMSON, width=8)
        d.text((cx - 28, cy - 16), "96", font=f_score, fill=C_WHITE)
        d.text((cx - 30, cy + 16), "GRADE A+", font=f_lbl, fill=C_EMERALD)

        d.line([(444, 238), (610, 238)], fill=C_BORDER, width=1)
        d.text((448, 250), "BullMQ Worker: Active", font=f_mono, fill=C_WHITE)
        d.text((448, 270), "SARIF Report:  Ready", font=f_mono, fill=C_SILVER)
        d.text((448, 290), "Scan Duration: 340ms", font=f_mono, fill=C_CRIMSON_HI)
        d.text((448, 312), "Monorepo: 5 Packages", font=f_mono, fill=C_MUTED)

        if f_idx == 0:
            fr.save(os.path.join(SRC_MIN_DIR, "demo_aegishub_plate.png"))
        frames.append(fr.convert("RGB"))

    out_gif = os.path.join(MINIMAL_ASSETS_DIR, "demo-aegishub.gif")
    save_fast_gif(frames, out_gif, DEMO_FPS, colors=64)
    print(f"[OK] AegisHub Demo generated: {out_gif} ({os.path.getsize(out_gif) // 1024} KB)")


def build_demo_bots_automation():
    base = create_demo_base_frame(
        "Soul-List & LWX Lab  ·  Real-Time Bot Architectures",
        "Baileys Multi-Device WebSockets  +  Discord.js Workflow Engine",
        "NODE.JS + TS + DRIZZLE",
        "logo-soullist.png",
    )

    f_mono_b = load_font(11, bold=True, mono=True)
    f_mono = load_font(10, bold=False, mono=True)
    f_lbl = load_font(10, bold=True, mono=True)
    f_big = load_font(20, bold=True, mono=True)

    frames = []
    for f_idx in range(DEMO_FRAMES):
        t = f_idx / float(DEMO_FRAMES)
        fr = base.copy()
        d = ImageDraw.Draw(fr)

        d.rounded_rectangle([18, 68, 312, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.rectangle([18, 68, 312, 96], fill=C_ELEVATED)
        d.text((28, 77), "SOUL-LIST // BAILEYS WEBSOCKET ENGINE", font=f_lbl, fill=C_CRIMSON_HI)

        lat = 11 + int(2 * math.sin(t * 2 * math.pi))
        d.text((28, 108), "1,420+ Commands", font=f_big, fill=C_WHITE)
        d.text((28, 134), f"O(1) Hash Dispatch  ·  {lat}ms avg", font=f_mono, fill=C_EMERALD)

        soul_logs = [
            ("!menu", "18 categories loaded (11ms)"),
            ("!sticker crop", "Sharp WebP buffer -> Sent (38ms)"),
            ("!group antilink", "Rule enforced via Drizzle/LibSQL"),
            ("!status", "RAM: 62MB · Socket: Connected"),
        ]
        active_log = int(t * 4) % 4
        for l_i, (cmd, resp) in enumerate(soul_logs):
            ly = 164 + l_i * 42
            is_act = l_i == active_log
            d.rounded_rectangle(
                [28, ly, 302, ly + 36],
                radius=4,
                fill=(32, 16, 24, 255) if is_act else C_ELEVATED,
                outline=C_CRIMSON if is_act else C_BORDER,
                width=1,
            )
            d.text((36, ly + 5), f"> {cmd}", font=f_mono_b, fill=C_WHITE)
            d.text((36, ly + 19), resp, font=f_mono, fill=C_SILVER)

        d.rounded_rectangle([328, 68, 622, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.rectangle([328, 68, 622, 96], fill=C_ELEVATED)
        d.text((338, 77), "LWX LAB // DISCORD WORKFLOW & AI BOT", font=f_lbl, fill=C_CRIMSON_HI)

        d.text((338, 108), "Order & Ticket Pipeline", font=f_big, fill=C_WHITE)
        d.text((338, 134), "Discord.js v14  ·  Automated Triage", font=f_mono, fill=C_SILVER)

        lwx_steps = [
            ("01. /lwx order create", "Channel #lwx-409 & Role provisioned"),
            ("02. Briefing Modal", "Structured client scope saved"),
            ("03. /lwx quote approve", "Status -> In Production · Team pinged"),
            ("04. /lwx delivery send", "Assets verified & audit logged"),
        ]
        for s_i, (step_t, step_d) in enumerate(lwx_steps):
            sy = 164 + s_i * 42
            is_act = s_i == active_log
            d.rounded_rectangle(
                [338, sy, 612, sy + 36],
                radius=4,
                fill=(32, 16, 24, 255) if is_act else C_ELEVATED,
                outline=C_CRIMSON if is_act else C_BORDER,
                width=1,
            )
            d.text((346, sy + 5), step_t, font=f_mono_b, fill=C_WHITE)
            d.text((346, sy + 19), step_d, font=f_mono, fill=C_SILVER)

        if f_idx == 0:
            fr.save(os.path.join(SRC_MIN_DIR, "demo_bots_plate.png"))
        frames.append(fr.convert("RGB"))

    out_gif = os.path.join(MINIMAL_ASSETS_DIR, "demo-bots-automation.gif")
    save_fast_gif(frames, out_gif, DEMO_FPS, colors=64)
    print(f"[OK] Bots Automation Demo generated: {out_gif} ({os.path.getsize(out_gif) // 1024} KB)")


def build_demo_hyperflow_polybech():
    base = create_demo_base_frame(
        "HyperFlow 3D & Polybech  ·  Systems & Graphics Lab",
        "Blender 5.2+ C++/Python Suite  +  Multi-Language Algorithm Benchmarks",
        "PYTHON + C++ + RUST",
        "logo-polybech.png",
    )

    f_mono_b = load_font(11, bold=True, mono=True)
    f_mono = load_font(10, bold=False, mono=True)
    f_lbl = load_font(10, bold=True, mono=True)

    bench_langs = [
        ("Rust (release)", 0.96, "1.02 ms", C_CRIMSON_HI),
        ("C++20 (O3 SIMD)", 0.94, "1.05 ms", C_CRIMSON),
        ("x86-64 Assembly", 0.98, "0.98 ms", C_EMERALD),
        ("TypeScript (V8)", 0.68, "4.10 ms", C_SILVER),
        ("Python 3.12", 0.42, "12.4 ms", C_MUTED),
    ]

    frames = []
    for f_idx in range(DEMO_FRAMES):
        t = f_idx / float(DEMO_FRAMES)
        fr = base.copy()
        d = ImageDraw.Draw(fr)

        d.rounded_rectangle([18, 68, 308, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((28, 78), "HYPERFLOW 3D // BLENDER 5.2+ SUITE", font=f_lbl, fill=C_CRIMSON_HI)
        d.line([(18, 98), (308, 98)], fill=C_BORDER, width=1)

        cx, cy = 163, 174
        for ring in range(1, 5):
            rx = ring * 26
            ry = ring * 14
            rot = t * 2.0 * math.pi
            pts = []
            for k in range(16):
                a = (k / 16.0) * 2.0 * math.pi + rot * (0.25 if ring % 2 == 0 else -0.25)
                px = cx + math.cos(a) * rx
                py = cy + math.sin(a) * ry + math.sin(a * 3 + rot) * 4.0
                pts.append((px, py))
            pts.append(pts[0])
            col = C_CRIMSON if ring == 3 else (75, 75, 98, 220)
            d.line(pts, fill=col, width=2 if ring == 3 else 1)

        d.rounded_rectangle([28, 248, 298, 330], radius=4, fill=C_ELEVATED, outline=C_BORDER, width=1)
        d.text((38, 256), "Quad Retopo + PBR Baker:  PASS", font=f_mono_b, fill=C_EMERALD)
        d.text((38, 274), "Temporal OIDN Stabilizer: 0.0% flicker", font=f_mono, fill=C_WHITE)
        d.text((38, 292), "Nanite Frustum Guard:     -64% VRAM", font=f_mono, fill=C_SILVER)
        d.text((38, 310), "3 Core C++ Patches + Python API", font=f_mono, fill=C_MUTED)

        d.rounded_rectangle([324, 68, 622, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((336, 78), "POLYBECH // ALGORITHM THROUGHPUT", font=f_lbl, fill=C_CRIMSON_HI)
        d.line([(324, 98), (622, 98)], fill=C_BORDER, width=1)

        for b_i, (lang, ratio, time_str, col) in enumerate(bench_langs):
            by = 114 + b_i * 44
            d.text((336, by), lang, font=f_mono_b, fill=C_WHITE)
            d.text((548, by), time_str, font=f_mono_b, fill=col)

            bar_w = 268
            d.rectangle([336, by + 18, 336 + bar_w, by + 28], fill=(26, 26, 36, 255))
            anim_r = ratio * (0.94 + 0.06 * math.sin(t * 2 * math.pi + b_i))
            d.rectangle([336, by + 18, 336 + int(bar_w * anim_r), by + 28], fill=col)

        if f_idx == 0:
            fr.save(os.path.join(SRC_MIN_DIR, "demo_hyperflow_polybech_plate.png"))
        frames.append(fr.convert("RGB"))

    out_gif = os.path.join(MINIMAL_ASSETS_DIR, "demo-hyperflow-polybech.gif")
    save_fast_gif(frames, out_gif, DEMO_FPS, colors=64)
    print(f"[OK] HyperFlow & Polybech Demo generated: {out_gif} ({os.path.getsize(out_gif) // 1024} KB)")


def build_demo_portfolio_webgl():
    """Demo 5: LLEWXAM.ME — Interactive 2.5D WebGL & GLSL Shader Portfolio."""
    base = create_demo_base_frame(
        "LLEWXAM.ME  ·  Interactive 2.5D WebGL Portfolio",
        "Custom GLSL Shaders  +  Multi-Plane Depth Parallax  +  React/TS",
        "WEBGL + GLSL + REACT",
        None,
    )

    f_mono_b = load_font(11, bold=True, mono=True)
    f_mono = load_font(10, bold=False, mono=True)
    f_lbl = load_font(10, bold=True, mono=True)

    city_ref_path = os.path.join(ROOT_WORKSPACE, "public", "assets", "reference", "oc-city-full.jpg")
    city_img = None
    if os.path.exists(city_ref_path):
        raw_city = Image.open(city_ref_path).convert("RGBA")
        raw_city = raw_city.resize((410, 265), Image.Resampling.LANCZOS)
        # Apply sophisticated dark-crimson grading so it harmonizes with the showcase
        tint = Image.new("RGBA", raw_city.size, (14, 10, 18, 85))
        city_img = Image.alpha_composite(raw_city, tint)

    frames = []
    for f_idx in range(DEMO_FRAMES):
        t = f_idx / float(DEMO_FRAMES)
        fr = base.copy()
        d = ImageDraw.Draw(fr)

        # Left Viewport: 2.5D WebGL Camera & GLSL Visor Bloom Preview
        d.rounded_rectangle([18, 68, 396, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        if city_img:
            # Subtle 2.5D camera pan crop
            ox = int(12 + 10 * math.sin(t * 2 * math.pi))
            oy = int(8 + 6 * math.cos(t * 2 * math.pi))
            cropped = city_img.crop((ox, oy, ox + 362, oy + 234))
            fr.paste(cropped, (26, 98))

        d.text((28, 76), "VIEWPORT // 2.5D DEPTH PARALLAX & GLSL VISOR", font=f_lbl, fill=C_CRIMSON_HI)
        # Animated HUD reticle inside viewport
        rx = int(205 + 14 * math.sin(t * 2 * math.pi))
        ry = int(195 + 8 * math.cos(t * 2 * math.pi))
        d.ellipse([rx - 14, ry - 14, rx + 14, ry + 14], outline=C_CRIMSON_HI, width=1)
        d.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=C_CRIMSON_HI)

        # Right Panel: Shader Uniforms & State Machine Telemetry
        d.rounded_rectangle([410, 68, 622, 342], radius=5, fill=C_GRAPHITE, outline=C_BORDER, width=1)
        d.text((422, 78), "GLSL SHADER PIPELINE", font=f_lbl, fill=C_CRIMSON_HI)
        d.line([(410, 98), (622, 98)], fill=C_BORDER, width=1)

        u_bloom = 0.75 + 0.22 * math.sin(t * 2 * math.pi)
        u_z = -1.02 - 0.18 * math.cos(t * 2 * math.pi)
        metrics = [
            ("uVisorEmission", f"{u_bloom:.2f}", C_CRIMSON_HI),
            ("uCameraZDepth", f"{u_z:.2f}", C_WHITE),
            ("Domain-Warped FBM", "60 FPS Lock", C_EMERALD),
            ("State Machine", "12 States", C_SILVER),
            ("Flipbook Engine", "Canvas 2D", C_SILVER),
            ("Live Domain", "llewxam.me", C_CRIMSON_HI),
        ]
        for m_i, (k_name, v_str, col) in enumerate(metrics):
            my = 110 + m_i * 37
            d.rounded_rectangle([420, my, 612, my + 30], radius=4, fill=C_ELEVATED, outline=C_BORDER, width=1)
            d.text((428, my + 8), k_name, font=f_mono, fill=C_SILVER)
            d.text((536, my + 8), v_str, font=f_mono_b, fill=col)

        if f_idx == 0:
            fr.save(os.path.join(SRC_MIN_DIR, "demo_portfolio_webgl_plate.png"))
        frames.append(fr.convert("RGB"))

    out_gif = os.path.join(MINIMAL_ASSETS_DIR, "demo-portfolio-webgl.gif")
    save_fast_gif(frames, out_gif, DEMO_FPS, colors=96)
    print(f"[OK] WebGL Portfolio Demo generated: {out_gif} ({os.path.getsize(out_gif) // 1024} KB)")


# ============================================================================
# 3. BESPOKE MINIMALIST SVGs (NAVIGATION, TECH STACK, FOOTER)
# ============================================================================
def build_navigation_svgs():
    nav_buttons = [
        ("nav-portfolio.svg", "PORTFÓLIO", "llewxam.me", True),
        ("nav-linkedin.svg", "LINKEDIN", "in/evandro-silva-amorimm", False),
        ("nav-projects.svg", "PROJETOS", "05 selecionados", False),
        ("nav-contact.svg", "GITHUB", "@LlewxamDev", False),
    ]
    for filename, label, sub, is_primary in nav_buttons:
        accent = "#E11D48" if is_primary else "#525266"
        bg = "#141016" if is_primary else "#0E0E13"
        border = "#881337" if is_primary else "#242430"
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="210" height="44" viewBox="0 0 210 44" fill="none">
  <rect x="0.5" y="0.5" width="209" height="43" rx="4" fill="{bg}" stroke="{border}"/>
  <rect x="0" y="0" width="4" height="44" rx="2" fill="#E11D48"/>
  <text x="18" y="19" fill="#F4F4F6" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="700" letter-spacing="1.2">{label}</text>
  <text x="18" y="34" fill="#9E9EA9" font-family="'JetBrains Mono', Consolas, monospace" font-size="10">{sub}</text>
  <path d="M184 18L190 22L184 26" stroke="{accent}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""
        with open(os.path.join(MINIMAL_ASSETS_DIR, filename), "w", encoding="utf-8") as f:
            f.write(svg)


def build_tech_stack_svg():
    categories = [
        (
            "01 // LINGUAGENS PRINCIPAIS",
            "Mais utilizadas nos repositórios e sistemas em produção",
            [
                ("TypeScript", "typescript.png", "Tipagem estrita & Back-end"),
                ("JavaScript", "javascript.png", "ESNext & Runtimes Web"),
                ("Python", "python.png", "Automação, IA & Blender API"),
                ("Rust", "rust.png", "Segurança, FFI & Análise Estática"),
                ("C++", "cpp.png", "Módulos Nativos & Computação 3D"),
                ("SQL", "postgres.png", "Modelagem Relacional & Queries"),
            ],
        ),
        (
            "02 // BACK-END, APIS & DADOS",
            "Arquitetura de servidores, alta vazão e persistência",
            [
                ("Node.js", "nodejs.png", "Runtime Assíncrono"),
                ("NestJS", "nestjs.png", "Arquitetura Modular & Enterprise"),
                ("Fastify", "fastify.png", "APIs HTTP de Baixa Latência"),
                ("Express", "express.png", "REST APIs & Middlewares"),
                ("PostgreSQL", "postgres.png", "Prisma & Drizzle ORM"),
                ("MySQL / Redis", "mysql.png", "Filas BullMQ & Cache"),
            ],
        ),
        (
            "03 // FRONT-END & GRÁFICOS INTERATIVOS",
            "Interfaces modernas, dashboards e experiências 2.5D / 3D",
            [
                ("React", "react.png", "Dashboards & SPAs"),
                ("Next.js", "nextjs.png", "Full-Stack Web & SSR"),
                ("Vite", "vite.png", "Build & Bundling Rápido"),
                ("Tailwind CSS", "tailwind.png", "Design Systems Escaláveis"),
                ("HTML5", "html5.png", "Semântica & Canvas 2D"),
                ("CSS3 / WebGL", "css3.png", "Shaders GLSL & Motion"),
            ],
        ),
        (
            "04 // AUTOMAÇÃO, INFRAESTRUTURA & AMBIENTE",
            "Ecossistemas de bots, containers e fluxo de engenharia",
            [
                ("Git", "git.png", "Versionamento & Branches"),
                ("GitHub", "github.png", "CI/CD, Actions & Security"),
                ("Docker", "docker.png", "Containers & Ambientes"),
                ("Linux / Bash", "linux.png", "Servidores & Shell Scripts"),
                ("VS Code", "vs_code.png", "Ambiente Principal & Debug"),
                ("After Effects & PS", "after_effects.png", "Motion Design & Assets"),
            ],
        ),
    ]

    width = 1200
    row_h = 126
    total_h = len(categories) * row_h + 24

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{total_h}" viewBox="0 0 {width} {total_h}" fill="none">',
        f'  <rect width="{width}" height="{total_h}" rx="8" fill="#09090C"/>',
        f'  <rect x="0.5" y="0.5" width="{width - 1}" height="{total_h - 1}" rx="7.5" stroke="#22222E"/>',
    ]

    for c_idx, (cat_title, cat_sub, items) in enumerate(categories):
        y0 = 16 + c_idx * row_h
        svg_parts.append(f'  <rect x="24" y="{y0 + 2}" width="3" height="14" fill="#E11D48"/>')
        svg_parts.append(
            f'  <text x="36" y="{y0 + 13}" fill="#F4F4F6" font-family="\'Segoe UI\', -apple-system, sans-serif" font-size="12" font-weight="700" letter-spacing="1.0">{cat_title}</text>'
        )
        svg_parts.append(
            f'  <text x="310" y="{y0 + 13}" fill="#71717A" font-family="\'JetBrains Mono\', Consolas, monospace" font-size="11">{cat_sub}</text>'
        )

        card_w = 182
        card_h = 68
        gap = 12
        start_x = 24
        cy = y0 + 26

        for i_idx, (name, logo_fn, desc) in enumerate(items):
            cx = start_x + i_idx * (card_w + gap)
            b64 = encode_file_base64(os.path.join(LOGOS_DIR, logo_fn))
            svg_parts.append(
                f'  <rect x="{cx}" y="{cy}" width="{card_w}" height="{card_h}" rx="5" fill="#111117" stroke="#232330"/>'
            )
            svg_parts.append(
                f'  <rect x="{cx}" y="{cy + 14}" width="2" height="{card_h - 28}" fill="#E11D48" opacity="0.85"/>'
            )
            if b64:
                svg_parts.append(
                    f'  <image x="{cx + 12}" y="{cy + 14}" width="22" height="22" href="data:image/png;base64,{b64}"/>'
                )
            svg_parts.append(
                f'  <text x="{cx + 42}" y="{cy + 29}" fill="#F4F4F6" font-family="\'Segoe UI\', -apple-system, sans-serif" font-size="13" font-weight="600">{name}</text>'
            )
            svg_parts.append(
                f'  <text x="{cx + 12}" y="{cy + 52}" fill="#8E8E9E" font-family="\'Segoe UI\', -apple-system, sans-serif" font-size="10.5">{desc}</text>'
            )

        if c_idx < len(categories) - 1:
            sep_y = y0 + row_h - 10
            svg_parts.append(f'  <line x1="24" y1="{sep_y}" x2="{width - 24}" y2="{sep_y}" stroke="#1B1B24"/>')

    svg_parts.append("</svg>")
    out_svg = os.path.join(MINIMAL_ASSETS_DIR, "tech-stack-showcase.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"[OK] Curated Tech Stack SVG generated: {out_svg} ({os.path.getsize(out_svg) // 1024} KB)")


def build_footer_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="72" viewBox="0 0 1200 72" fill="none">
  <rect width="1200" height="72" rx="6" fill="#09090C"/>
  <rect x="0.5" y="0.5" width="1199" height="71" rx="5.5" stroke="#22222E"/>
  <rect x="0" y="0" width="4" height="72" rx="2" fill="#E11D48"/>
  <text x="32" y="32" fill="#F4F4F6" font-family="'Segoe UI', -apple-system, sans-serif" font-size="14" font-weight="700" letter-spacing="0.6">Construindo, aprendendo e evoluindo.</text>
  <text x="32" y="52" fill="#8E8E9E" font-family="'JetBrains Mono', Consolas, monospace" font-size="11">Evandro Silva Amorim (@LlewxamDev)  ·  Desenvolvimento de Sistemas, Software &amp; Automação</text>
  <circle cx="1156" cy="36" r="4" fill="#E11D48"/>
  <circle cx="1172" cy="36" r="4" fill="#272732"/>
</svg>"""
    out_svg = os.path.join(MINIMAL_ASSETS_DIR, "footer-minimal.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[OK] Footer SVG generated: {out_svg}")


def write_layered_psd(psd_path: str, width: int, height: int, layers: list, composite_img: Image.Image):
    """
    Writes an authentic Adobe Photoshop (.PSD, 8BPS v1) file containing multiple
    named RGBA layers and a full merged composite preview image.
    `layers` is a list of (layer_name, rgba_pil_image).
    """
    import struct

    # 1. File Header Section (26 bytes)
    # Signature '8BPS', Version 1, 6 reserved bytes, 4 channels (RGBA), height, width, depth 8, mode 3 (RGB)
    header = struct.pack(">4sH6sHIIHH", b"8BPS", 1, b"\x00" * 6, 4, height, width, 8, 3)

    # 2. Color Mode Data Section (4 bytes: length 0)
    color_mode_section = struct.pack(">I", 0)

    # 3. Image Resources Section (4 bytes: length 0)
    image_resources_section = struct.pack(">I", 0)

    # 4. Layer and Mask Information Section
    layer_records = bytearray()
    channel_image_data = bytearray()

    for name, img in layers:
        rgba = img.convert("RGBA")
        if rgba.size != (width, height):
            rgba = rgba.resize((width, height), Image.Resampling.LANCZOS)
        r_ch, g_ch, b_ch, a_ch = [ch.tobytes() for ch in rgba.split()]
        ch_bytes_len = width * height + 2  # +2 for compression method (0 = raw)

        # Layer bounds: top=0, left=0, bottom=height, right=width, num_channels=4
        layer_records.extend(struct.pack(">iiiiH", 0, 0, height, width, 4))
        # Channel info: id (0=R, 1=G, 2=B, -1=A), length
        for ch_id in (0, 1, 2, -1):
            layer_records.extend(struct.pack(">hi", ch_id, ch_bytes_len))

        # Blend mode signature '8BIM', key 'norm', opacity 255, clipping 0, flags 0, filler 0
        layer_records.extend(struct.pack(">4s4sBBBB", b"8BIM", b"norm", 255, 0, 0, 0))

        # Extra data field: layer mask data (0 bytes) + blending ranges (0 bytes) + Pascal name padded to 4 bytes
        name_bytes = name.encode("latin1", errors="replace")[:31]
        pascal_len = len(name_bytes)
        total_name_field = 1 + pascal_len
        pad_len = (4 - (total_name_field % 4)) % 4
        extra_data = struct.pack(">II", 0, 0) + struct.pack(">B", pascal_len) + name_bytes + (b"\x00" * pad_len)

        layer_records.extend(struct.pack(">I", len(extra_data)))
        layer_records.extend(extra_data)

        # Append raw uncompressed channel data for R, G, B, A
        for raw_ch in (r_ch, g_ch, b_ch, a_ch):
            channel_image_data.extend(struct.pack(">H", 0))  # Compression 0 = Raw
            channel_image_data.extend(raw_ch)

    layer_info_payload = bytearray()
    layer_info_payload.extend(struct.pack(">h", len(layers)))
    layer_info_payload.extend(layer_records)
    layer_info_payload.extend(channel_image_data)
    if len(layer_info_payload) % 2 != 0:
        layer_info_payload.append(0)

    layer_and_mask_payload = bytearray()
    layer_and_mask_payload.extend(struct.pack(">I", len(layer_info_payload)))
    layer_and_mask_payload.extend(layer_info_payload)
    layer_and_mask_payload.extend(struct.pack(">I", 0))  # Global layer mask info = 0

    layer_and_mask_section = struct.pack(">I", len(layer_and_mask_payload)) + bytes(layer_and_mask_payload)

    # 5. Composite Merged Image Data Section
    comp_rgba = composite_img.convert("RGBA")
    if comp_rgba.size != (width, height):
        comp_rgba = comp_rgba.resize((width, height), Image.Resampling.LANCZOS)
    cr, cg, cb, ca = [ch.tobytes() for ch in comp_rgba.split()]
    image_data_section = struct.pack(">H", 0) + cr + cg + cb + ca

    with open(psd_path, "wb") as fp:
        fp.write(header)
        fp.write(color_mode_section)
        fp.write(image_resources_section)
        fp.write(layer_and_mask_section)
        fp.write(image_data_section)
    print(f"[OK] Multi-Layer Photoshop PSD generated: {psd_path} ({os.path.getsize(psd_path) // 1024} KB)")


def build_photoshop_master_psds():
    hero_bg = Image.open(os.path.join(SRC_MIN_DIR, "hero_bg_obsidian_plate.png"))
    hero_circ = Image.open(os.path.join(SRC_MIN_DIR, "hero_circuit_traces_plate.png"))
    hero_typo = Image.open(os.path.join(SRC_MIN_DIR, "hero_typography_plate.png"))
    hero_comp = Image.open(os.path.join(SRC_MIN_DIR, "hero_master_preview.png"))

    write_layered_psd(
        os.path.join(PS_DIR, "LLEW_Minimal_Hero_Banner.psd"),
        HERO_W,
        HERO_H,
        [
            ("01_OBSIDIAN_AND_CRIMSON_RIM", hero_bg),
            ("02_CIRCUIT_TRACES_LAYER", hero_circ),
            ("03_TYPOGRAPHY_EVANDRO_SILVA", hero_typo),
        ],
        hero_comp,
    )

    p1 = Image.open(os.path.join(SRC_MIN_DIR, "demo_aegiscore_plate.png"))
    p2 = Image.open(os.path.join(SRC_MIN_DIR, "demo_aegishub_plate.png"))
    p3 = Image.open(os.path.join(SRC_MIN_DIR, "demo_bots_plate.png"))
    p4 = Image.open(os.path.join(SRC_MIN_DIR, "demo_hyperflow_polybech_plate.png"))
    p5 = Image.open(os.path.join(SRC_MIN_DIR, "demo_portfolio_webgl_plate.png"))

    write_layered_psd(
        os.path.join(PS_DIR, "LLEW_Minimal_Project_Showcase.psd"),
        DEMO_W,
        DEMO_H,
        [
            ("05_PORTFOLIO_WEBGL_SHOWCASE", p5),
            ("04_HYPERFLOW_POLYBECH_SHOWCASE", p4),
            ("03_SOULLIST_LWXLAB_SHOWCASE", p3),
            ("02_AEGISHUB_SHOWCASE", p2),
            ("01_AEGISCORE_SHOWCASE", p1),
        ],
        p1,
    )


if __name__ == "__main__":
    build_hero_plates_and_gif()
    build_demo_aegiscore()
    build_demo_aegishub()
    build_demo_bots_automation()
    build_demo_hyperflow_polybech()
    build_demo_portfolio_webgl()
    build_navigation_svgs()
    build_tech_stack_svg()
    build_footer_svg()
    build_photoshop_master_psds()

