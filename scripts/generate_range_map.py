#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生息・分布マップ自動生成スクリプト (generate_range_map.py)
ナショナルジオグラフィック風の生息分布図（クォータ消費ゼロ）をPillowでローカル生成・合成するユーティリティ。
"""

import sys
import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_base_range_map(output_path, title_ja, title_en, primary_region, points=None, polygons=None, map_type="world"):
    """
    ナショジオ風配色（ダークネイビー背景、ゴールド/イエローハイライト、赤色特異点ピン）で分布図を生成
    """
    width = 900
    height = 500
    
    # ベース画像作成 (ダークテーマ)
    bg_color = (26, 32, 44)       # #1a202c
    grid_color = (45, 55, 72)     # #2d3748
    land_color = (40, 50, 68)     # #283244
    ocean_color = (20, 26, 38)    # #141a26
    highlight_color = (236, 201, 75, 160)  # #ecc94b 半透明イエロー
    primary_color = (229, 62, 62, 220)    # #e53e3e 半透明レッド
    text_white = (247, 250, 252)
    text_gray = (160, 174, 192)
    
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img, "RGBA")
    
    # グリッド描画
    grid_size = 40
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
        
    # 外枠
    draw.rectangle([(10, 10), (width - 10, height - 10)], outline=(74, 85, 104), width=2)
    
    # ヘッダー情報描画
    draw.rectangle([(20, 20), (width - 20, 80)], fill=(33, 41, 57, 200), outline=(74, 85, 104), width=1)
    
    # タイトル
    # フォントのフォールバック
    try:
        font_title = ImageFont.truetype("meiryo.ttc", 20)
        font_sub = ImageFont.truetype("arial.ttf", 12)
        font_label = ImageFont.truetype("meiryo.ttc", 13)
        font_legend = ImageFont.truetype("meiryo.ttc", 11)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_legend = ImageFont.load_default()

    draw.text((35, 30), f"HABITAT RANGE MAP: {title_ja}", fill=text_white, font=font_title)
    draw.text((35, 56), f"SCIENTIFIC NAME / RANGE: {title_en} | {primary_region}", fill=text_gray, font=font_sub)
    
    # 簡易大陸シェイプ（極東・太平洋エリアのシンボリック描画）
    if map_type == "pacific" or map_type == "world":
        # ユーラシア東岸
        draw.polygon([(60, 100), (220, 100), (260, 180), (240, 260), (180, 320), (100, 320), (60, 200)], fill=land_color, outline=(74, 85, 104))
        # 日本列島
        draw.polygon([(260, 170), (290, 150), (330, 170), (320, 210), (280, 220), (250, 190)], fill=land_color, outline=(90, 105, 130))
        # 北米西岸
        draw.polygon([(680, 100), (840, 100), (840, 320), (760, 320), (700, 220), (660, 150)], fill=land_color, outline=(74, 85, 104))
        # オーストラリア
        draw.polygon([(280, 360), (400, 350), (420, 440), (320, 460), (260, 410)], fill=land_color, outline=(74, 85, 104))
        
        # 海洋ラベリング
        draw.text((450, 230), "PACIFIC OCEAN", fill=(55, 68, 92), font=font_sub)
        draw.text((160, 220), "EAST ASIA", fill=(70, 85, 110), font=font_sub)
        draw.text((720, 200), "NORTH AMERICA", fill=(70, 85, 110), font=font_sub)

    # ハイライトポリゴン描画
    if polygons:
        for poly in polygons:
            draw.polygon(poly, fill=highlight_color, outline=(236, 201, 75, 240), width=2)
            
    # 特異点・ピン描画
    if points:
        for pt, label, is_primary in points:
            px, py = pt
            color = primary_color if is_primary else highlight_color
            # 外輪パルス
            draw.ellipse([(px - 14, py - 14), (px + 14, py + 14)], fill=(color[0], color[1], color[2], 50))
            draw.ellipse([(px - 8, py - 8), (px + 8, py + 8)], fill=color, outline=(255, 255, 255, 220), width=2)
            draw.text((px + 15, py - 8), label, fill=text_white, font=font_label)

    # 凡例ボックス (右下)
    leg_x = width - 280
    leg_y = height - 125
    draw.rectangle([(leg_x, leg_y), (width - 30, height - 30)], fill=(33, 41, 57, 220), outline=(74, 85, 104), width=1)
    draw.text((leg_x + 15, leg_y + 10), "凡例 (LEGEND)", fill=text_white, font=font_legend)
    
    # 凡例アイコン
    draw.ellipse([(leg_x + 15, leg_y + 35), (leg_x + 27, leg_y + 47)], fill=(229, 62, 62, 220), outline=(255, 255, 255))
    draw.text((leg_x + 35, leg_y + 34), "一次生息地（特異点・原産地）", fill=text_gray, font=font_legend)
    
    draw.ellipse([(leg_x + 15, leg_y + 60), (leg_x + 27, leg_y + 72)], fill=(236, 201, 75, 220), outline=(255, 255, 255))
    draw.text((leg_x + 35, leg_y + 59), "回遊・出現警戒エリア", fill=text_gray, font=font_legend)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Range map successfully generated: {output_path}")

if __name__ == "__main__":
    # テスト生成: 幽光星海月の分布図
    test_out = "assets/creatures/008_astral_nebula_jelly/astral_jelly_range_map.png"
    sample_points = [
        ((380, 290), "マリアナ海溝（太平洋アビス）", True),
        ((310, 185), "東京湾口（浦賀水道）", False),
    ]
    sample_polygons = [
        # 太平洋回遊回廊
        [(360, 270), (410, 280), (330, 180), (290, 180)]
    ]
    create_base_range_map(test_out, "幽光星海月（ユウコウホシクラゲ）", "Aurelia astralis", "Pacific Abyss to Tokyo Bay", sample_points, sample_polygons, "pacific")
