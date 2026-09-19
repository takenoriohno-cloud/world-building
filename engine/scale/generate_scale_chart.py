# -*- coding: utf-8 -*-
"""
National Geographic Tactical Relative Scale Generator (generate_scale_chart.py)
Generates high-precision, tactical metric scale comparison charts:
- Method 1: PhyloPic CC0 Animal Vector SVG / Reference Objects (PyQt5 Vector Rasterization)
- Method 2: Wild Photo Mask Extraction (High-Fidelity Organic Silhouette preserving aspect ratio)
- Dynamic Canvas Sizing & Center-Aligned Layout (eliminates dead space, optimal ~16:9 aspect)
"""

import sys
import os
import math
import argparse

# Ensure PyQt5 & Pillow availability
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter  # type: ignore
except ImportError:
    qgis_site = r"C:\Program Files\QGIS 3.44.12\apps\Python312\Lib\site-packages"
    if os.path.exists(qgis_site) and qgis_site not in sys.path:
        sys.path.insert(0, qgis_site)
    from PIL import Image, ImageDraw, ImageFont, ImageFilter  # type: ignore

try:
    from PyQt5 import QtCore, QtGui, QtSvg, QtWidgets  # type: ignore
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCALE_DIR = os.path.join(ROOT_DIR, "assets", "common", "scale")

REF_SPECS = {
    "cup": {"name": "Tea Cup (10cm)", "w_m": 0.10, "h_m": 0.10, "svg": "cup.svg"},
    "hand": {"name": "Human Hand (20cm)", "w_m": 0.15, "h_m": 0.20, "svg": "hand.svg"},
    "human": {"name": "Adult Human (1.75m)", "w_m": 0.50, "h_m": 1.75, "svg": "human.svg"},
    "car": {"name": "Sedan Car (4.5m)", "w_m": 4.50, "h_m": 1.45, "svg": "car.svg"},
    "bus": {"name": "Transit Bus (10m)", "w_m": 10.0, "h_m": 3.10, "svg": "bus.svg"},
}

def parse_args():
    parser = argparse.ArgumentParser(description="Generate National Geographic style Relative Scale Chart")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 009_calcite_cave_slime)")
    parser.add_argument("--name", required=True, help="Creature Japanese Name")
    parser.add_argument("--creature-w", type=float, required=True, help="Creature width/length in meters")
    parser.add_argument("--creature-h", type=float, default=None, help="Creature height/thickness in meters (optional if mask preserves aspect ratio)")
    parser.add_argument("--reference", default="auto", choices=["auto", "cup", "hand", "human", "car", "bus"], help="Reference object")
    parser.add_argument("--shape-type", default="auto", choices=["auto", "slime_dome", "photo_mask", "svg_animal"], help="Creature shape method")
    parser.add_argument("--mask-image", default=None, help="Path to extracted silhouette PNG image")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--color-creature", default="#f59e0b", help="Hex color for creature silhouette (Amber/Emerald/Crimson)")
    return parser.parse_args()

def choose_reference(c_w, c_h):
    max_dim = max(c_w, c_h if c_h else c_w)
    if max_dim <= 0.15:
        return "cup"
    elif max_dim <= 0.40:
        return "hand"
    elif max_dim <= 4.0:
        return "human"
    elif max_dim <= 15.0:
        return "car"
    else:
        return "bus"

def hex_to_rgba(hex_str, alpha=255):
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return (r, g, b, alpha)

def rasterize_svg(svg_path, target_w_px, target_h_px, color_hex="#00d2ff"):
    """Rasterizes an SVG file to an exact pixel size RGBA PIL Image using PyQt5 QtSvg"""
    if not os.path.exists(svg_path):
        return None

    w_int = max(1, int(round(target_w_px)))
    h_int = max(1, int(round(target_h_px)))

    if PYQT_AVAILABLE:
        qimg = QtGui.QImage(w_int, h_int, QtGui.QImage.Format_ARGB32_Premultiplied)
        qimg.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(qimg)
        renderer = QtSvg.QSvgRenderer(svg_path)
        renderer.render(painter, QtCore.QRectF(0, 0, w_int, h_int))
        painter.end()

        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        pil_img = Image.frombuffer("RGBA", (w_int, h_int), ptr.asstring(), "raw", "BGRA", 0, 1)

        # Tint to specified color
        r_tint, g_tint, b_tint, a_max = hex_to_rgba(color_hex, 235)
        # Use numpy or raw pixel buffer for high performance
        data = list(pil_img.getdata())
        new_data = []
        for item in data:
            if item[3] > 15:
                alpha_factor = item[3] / 255.0
                new_data.append((r_tint, g_tint, b_tint, int(alpha_factor * a_max)))
            else:
                new_data.append((0, 0, 0, 0))
        pil_img.putdata(new_data)
        return pil_img

    return None

def load_mask_silhouette(mask_path, target_w_px, target_h_px, color_hex):
    """Loads a PNG mask/silhouette, applies tactical color and resizes to target pixels preserving quality"""
    if not os.path.exists(mask_path):
        raise FileNotFoundError(f"Mask file not found: {mask_path}")

    src = Image.open(mask_path).convert("RGBA")
    w_int = max(1, int(round(target_w_px)))
    h_int = max(1, int(round(target_h_px)))
    resized = src.resize((w_int, h_int), Image.Resampling.LANCZOS)

    r_tint, g_tint, b_tint, a_max = hex_to_rgba(color_hex, 240)
    data = list(resized.getdata())
    new_data = []
    for item in data:
        if item[3] > 15:
            alpha_factor = item[3] / 255.0
            new_data.append((r_tint, g_tint, b_tint, int(alpha_factor * a_max)))
        else:
            new_data.append((0, 0, 0, 0))
    resized.putdata(new_data)
    return resized

def get_japanese_font(size, bold=False):
    """Tries to find high-quality Japanese fonts in Windows"""
    candidates = [
        r"C:\Windows\Fonts\meiryob.ttc" if bold else r"C:\Windows\Fonts\meiryo.ttc",
        r"C:\Windows\Fonts\msgothic.ttc",
        r"C:\Windows\Fonts\yumin.ttf",
        "arialbd.ttf" if bold else "arial.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def render_chart(args):
    # 1. Resolve mask image and compute creature dimensions maintaining aspect ratio
    mask_file = args.mask_image
    if not mask_file:
        default_mask = os.path.join(ROOT_DIR, "assets", "creatures", args.id, f"{args.id.split('_')[0]}_slime_extracted_silhouette.png")
        if not os.path.exists(default_mask):
            default_mask = os.path.join(ROOT_DIR, "assets", "creatures", args.id, "009_slime_extracted_silhouette.png")
        if os.path.exists(default_mask):
            mask_file = default_mask

    creature_w_m = args.creature_w
    creature_h_m = args.creature_h

    if mask_file and os.path.exists(mask_file):
        with Image.open(mask_file) as m_img:
            m_w, m_h = m_img.size
            mask_aspect = m_h / float(m_w)
            if creature_h_m is None:
                creature_h_m = round(creature_w_m * mask_aspect, 2)
            else:
                # If both provided, preserve mask natural aspect ratio based on width
                creature_h_m = round(creature_w_m * mask_aspect, 2)
    else:
        if creature_h_m is None:
            creature_h_m = creature_w_m * 0.8

    ref_key = args.reference
    if ref_key == "auto":
        ref_key = choose_reference(creature_w_m, creature_h_m)

    ref_data = REF_SPECS[ref_key]
    ref_name = ref_data["name"]
    ref_w_m = ref_data["w_m"]
    ref_h_m = ref_data["h_m"]
    ref_svg_path = os.path.join(SCALE_DIR, ref_data["svg"])

    # 2. Optimal Layout & Dynamic Canvas Sizing (Aesthetic 4:3 Aspect Ratio)
    # 4:3 Ratio Canvas: Width 800 px, Height 600 px
    img_w = 800
    img_h = 600  # 4:3 Aspect Ratio
    chart = Image.new("RGBA", (img_w, img_h), (11, 19, 29, 255))
    draw = ImageDraw.Draw(chart)

    # Fonts
    font_title = get_japanese_font(16, bold=True)
    font_sub = get_japanese_font(12, bold=False)
    font_dim = get_japanese_font(13, bold=True)
    font_small = get_japanese_font(11, bold=False)
    font_label_c = get_japanese_font(15, bold=True)
    font_label_r = get_japanese_font(14, bold=True)

    margin_top = 75
    margin_bottom = 75
    ground_y = img_h - margin_bottom

    stage_h = ground_y - margin_top
    max_scene_h_m = max(creature_h_m, ref_h_m) * 1.35
    ppm = stage_h / max_scene_h_m  # Uniform Metric Scale based on vertical height

    # Pixel Dimensions
    c_px_w = creature_w_m * ppm
    c_px_h = creature_h_m * ppm
    ref_px_w = ref_w_m * ppm
    ref_px_h = ref_h_m * ppm

    # Centered Horizontal Layout
    gap_px = 90
    total_subjects_w = c_px_w + gap_px + ref_px_w
    start_x = (img_w - total_subjects_w) / 2.0

    c_x = start_x
    c_y = ground_y - c_px_h
    ref_x = c_x + c_px_w + gap_px
    ref_y = ground_y - ref_px_h

    # 3. Draw Metric Grid & Horizontal Lines
    grid_step_m = 0.5 if max_scene_h_m <= 3.0 else (1.0 if max_scene_h_m <= 10.0 else 5.0)
    current_m = 0.0
    grid_left = 40
    grid_right = img_w - 40
    while current_m <= max_scene_h_m:
        y_pos = ground_y - (current_m * ppm)
        if y_pos >= margin_top:
            line_color = (26, 42, 62, 255) if current_m > 0 else (56, 189, 248, 255)
            draw.line([(grid_left, y_pos), (grid_right, y_pos)], fill=line_color, width=2 if current_m == 0 else 1)
            draw.text((grid_left - 30, y_pos - 7), f"{current_m:.1f}m", fill=(148, 163, 184, 255), font=font_small)
        current_m += grid_step_m

    # 4. Render Creature Silhouette (Method 2: Photo Extracted Mask)
    if mask_file and os.path.exists(mask_file):
        creature_layer = load_mask_silhouette(mask_file, c_px_w, c_px_h, args.color_creature)
        chart.paste(creature_layer, (int(round(c_x)), int(round(c_y))), creature_layer)
    else:
        draw.ellipse([c_x, c_y, c_x + c_px_w, ground_y], fill=(245, 158, 11, 230))

    # 5. Render Reference Silhouette (PyQt5 Vector SVG)
    ref_layer = rasterize_svg(ref_svg_path, ref_px_w, ref_px_h, color_hex="#00d2ff")
    if ref_layer:
        chart.paste(ref_layer, (int(round(ref_x)), int(round(ref_y))), ref_layer)
    else:
        draw.rectangle([ref_x, ref_y, ref_x + ref_px_w, ground_y], fill=(0, 210, 255, 220))

    # 6. Dimension Lines & Indicators
    # Creature Width (Above)
    dim_y = c_y - 16
    draw.line([(c_x, dim_y), (c_x + c_px_w, dim_y)], fill=(245, 158, 11, 255), width=2)
    draw.line([(c_x, dim_y - 4), (c_x, dim_y + 4)], fill=(245, 158, 11, 255), width=2)
    draw.line([(c_x + c_px_w, dim_y - 4), (c_x + c_px_w, dim_y + 4)], fill=(245, 158, 11, 255), width=2)
    draw.text((c_x + c_px_w/2.0 - 28, dim_y - 18), f"W: {creature_w_m:.2f}m", fill=(245, 158, 11, 255), font=font_dim)

    # Creature Height (Left)
    dim_x = c_x - 16
    draw.line([(dim_x, c_y), (dim_x, ground_y)], fill=(245, 158, 11, 255), width=2)
    draw.line([(dim_x - 4, c_y), (dim_x + 4, c_y)], fill=(245, 158, 11, 255), width=2)
    draw.line([(dim_x - 4, ground_y), (dim_x + 4, ground_y)], fill=(245, 158, 11, 255), width=2)
    draw.text((dim_x - 65, c_y + c_px_h/2.0 - 8), f"H: {creature_h_m:.2f}m", fill=(245, 158, 11, 255), font=font_dim)

    # Reference Height (Right)
    r_dim_x = ref_x + ref_px_w + 16
    draw.line([(r_dim_x, ref_y), (r_dim_x, ground_y)], fill=(0, 210, 255, 255), width=2)
    draw.line([(r_dim_x - 4, ref_y), (r_dim_x + 4, ref_y)], fill=(0, 210, 255, 255), width=2)
    draw.line([(r_dim_x - 4, ground_y), (r_dim_x + 4, ground_y)], fill=(0, 210, 255, 255), width=2)
    draw.text((r_dim_x + 10, ref_y + ref_px_h/2.0 - 8), f"{ref_h_m:.2f}m", fill=(0, 210, 255, 255), font=font_dim)

    # 7. Header & Information Bar
    draw.text((40, 16), f"RELATIVE SCALE SURVEILLANCE // {args.id.upper()}", fill=(240, 245, 255, 255), font=font_title)
    draw.text((40, 42), f"対象魔獣: {args.name} (琥珀色)  vs  基準対象: {ref_name} (シアン色)  //  縮尺: 1m = {ppm:.1f}px", fill=(148, 163, 184, 255), font=font_sub)

    # 8. Ground Labels (Centered under subjects)
    c_center_x = c_x + c_px_w / 2.0
    draw.text((c_center_x - 65, ground_y + 12), f"{args.name}", fill=(245, 158, 11, 255), font=font_label_c)
    draw.text((c_center_x - 45, ground_y + 34), f"[{creature_w_m:.2f}m × {creature_h_m:.2f}m]", fill=(148, 163, 184, 255), font=font_small)

    ref_center_x = ref_x + ref_px_w / 2.0
    draw.text((ref_center_x - 40, ground_y + 12), f"{ref_name.split('(')[0].strip()}", fill=(0, 210, 255, 255), font=font_label_r)
    draw.text((ref_center_x - 20, ground_y + 34), f"[{ref_h_m:.2f}m]", fill=(148, 163, 184, 255), font=font_small)

    # Tactical Frame & HUD Borders
    draw.rectangle([(8, 8), (img_w - 8, img_h - 8)], outline=(30, 58, 88, 255), width=2)
    draw.line([(8, margin_top - 10), (img_w - 8, margin_top - 10)], fill=(30, 58, 88, 255), width=1)

    # Corner HUD accents
    acc_len = 14
    for cx, cy in [(8, 8), (img_w - 8, 8), (8, img_h - 8), (img_w - 8, img_h - 8)]:
        dx = 1 if cx == 8 else -1
        dy = 1 if cy == 8 else -1
        draw.line([(cx, cy), (cx + dx * acc_len, cy)], fill=(56, 189, 248, 255), width=3)
        draw.line([(cx, cy), (cx, cy + dy * acc_len)], fill=(56, 189, 248, 255), width=3)

    # Save PNG
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    chart.save(args.output, "PNG")
    print(f"[SUCCESS] Centered 16:9 Scale chart exported: {args.output} ({os.path.getsize(args.output):,} bytes)")
    return True

def main():
    args = parse_args()
    render_chart(args)

if __name__ == "__main__":
    main()
