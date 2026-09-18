# -*- coding: utf-8 -*-
"""
External Map Tile Downloader (fetch_map_tiles.py)
Dedicated single-purpose script to fetch map tiles from authorized tile servers.
Runs strictly during the isolated network-window (BypassSandbox: true).
Downloads tiles for given BBOX, stitches them into a georeferenced raster, and saves locally.
"""

import sys
import os
import math
import ssl
import urllib.request
import argparse
try:
    from PIL import Image  # type: ignore
except ImportError:
    # Auto-fallback to QGIS site-packages if run outside QGIS python environment
    qgis_site = r"C:\Program Files\QGIS 3.44.12\apps\Python312\Lib\site-packages"
    if os.path.exists(qgis_site) and qgis_site not in sys.path:
        sys.path.insert(0, qgis_site)
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        Image = None

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and stitch map tiles for BBOX")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 019_forest_mirage_chameleon)")
    parser.add_argument("--primary-bbox", required=True, help="minLon,minLat,maxLon,maxLat")
    parser.add_argument("--domestic-bbox", required=True, help="minLon,minLat,maxLon,maxLat")
    parser.add_argument("--output-dir", required=True, help="Output directory for stitched basemaps")
    parser.add_argument("--zoom-p", type=int, default=10, help="Zoom level for primary panel")
    parser.add_argument("--zoom-d", type=int, default=12, help="Zoom level for domestic panel")
    parser.add_argument("--tile-source", default="google_terrain", choices=["google_terrain", "esri_topo", "esri_dark", "esri_imagery", "carto_dark", "osm"], help="Tile source provider")
    return parser.parse_args()

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def download_and_stitch(bbox_str, zoom, out_file, tile_source="google_terrain"):
    coords = [float(x.strip()) for x in bbox_str.split(",")]
    min_lon, min_lat, max_lon, max_lat = coords[0], coords[1], coords[2], coords[3]

    # Add 15% margin
    w_margin = (max_lon - min_lon) * 0.15
    h_margin = (max_lat - min_lat) * 0.15
    min_lon -= w_margin
    max_lon += w_margin
    min_lat -= h_margin
    max_lat += h_margin

    x_min, y_min = deg2num(max_lat, min_lon, zoom)
    x_max, y_max = deg2num(min_lat, max_lon, zoom)

    # Ensure valid bounds
    x_start, x_end = min(x_min, x_max), max(x_min, x_max)
    y_start, y_end = min(y_min, y_max), max(y_min, y_max)

    # Clamp tile span to avoid huge downloads (max 8x8)
    if (x_end - x_start + 1) > 8:
        x_end = x_start + 7
    if (y_end - y_start + 1) > 8:
        y_end = y_start + 7

    cols = x_end - x_start + 1
    rows = y_end - y_start + 1

    tile_w, tile_h = 256, 256
    stitched = Image.new("RGBA", (cols * tile_w, rows * tile_h), (238, 236, 230, 255))

    ctx = ssl._create_unverified_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 TacticalGEOINT/2.0"
    }

    success_count = 0
    total_tiles = cols * rows

    print(f"[TILES] Fetching {cols}x{rows} ({total_tiles}) tiles for BBOX [{bbox_str}] at zoom {zoom} (Source: {tile_source})...")

    for r, y in enumerate(range(y_start, y_end + 1)):
        for c, x in enumerate(range(x_start, x_end + 1)):
            if tile_source == "google_terrain":
                url = f"https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={zoom}"
            elif tile_source == "esri_topo":
                url = f"https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{zoom}/{y}/{x}"
            elif tile_source == "esri_dark":
                url = f"https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{zoom}/{y}/{x}"
            elif tile_source == "esri_imagery":
                url = f"https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"
            elif tile_source == "carto_dark":
                url = f"https://a.basemaps.cartocdn.com/dark_all/{zoom}/{x}/{y}.png"
            elif tile_source == "osm":
                url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
            else:
                url = f"https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={zoom}"

            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, context=ctx, timeout=7) as resp:
                    if resp.status == 200:
                        from io import BytesIO
                        img_data = BytesIO(resp.read())
                        tile_img = Image.open(img_data).convert("RGBA")
                        stitched.paste(tile_img, (c * tile_w, r * tile_h))
                        success_count += 1
            except Exception as e:
                print(f"  ! Tile {zoom}/{x}/{y} error: {e}")

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    stitched.save(out_file, "PNG")
    
    # Generate ESRI World File (.pgw) and .prj for perfect EPSG:3857 georeferencing in QGIS
    initial_resolution = 40075016.68557849 / 256.0
    res = initial_resolution / (2 ** zoom)
    origin_shift = 20037508.342789244
    
    x_min_3857 = (x_start * 256.0 * res) - origin_shift
    y_max_3857 = origin_shift - (y_start * 256.0 * res)
    
    # Center of top-left pixel
    ul_x = x_min_3857 + (res / 2.0)
    ul_y = y_max_3857 - (res / 2.0)
    
    pgw_file = os.path.splitext(out_file)[0] + ".pgw"
    with open(pgw_file, "w", encoding="utf-8") as pf:
        pf.write(f"{res:.10f}\n0.0000000000\n0.0000000000\n{-res:.10f}\n{ul_x:.10f}\n{ul_y:.10f}\n")

    prj_file = os.path.splitext(out_file)[0] + ".prj"
    wkt_3857 = 'PROJCS["WGS 84 / Pseudo-Mercator",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Mercator_1SP"],PARAMETER["central_meridian",0],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","3857"]]]'
    with open(prj_file, "w", encoding="utf-8") as prjf:
        prjf.write(wkt_3857)

    # Save metadata text for reference
    top_lat, left_lon = num2deg(x_start, y_start, zoom)
    bottom_lat, right_lon = num2deg(x_end + 1, y_end + 1, zoom)
    meta_file = out_file + ".meta.txt"
    with open(meta_file, "w", encoding="utf-8") as mf:
        mf.write(f"{left_lon},{bottom_lat},{right_lon},{top_lat}")

    print(f"[SUCCESS] Stitched basemap saved: {out_file} ({success_count}/{total_tiles} tiles, size: {os.path.getsize(out_file):,} bytes)")
    print(f"  ✓ Georeference World File generated: {pgw_file}")
    print(f"  ✓ Projection File generated: {prj_file}")
    return True

def main():
    args = parse_args()
    print(f"\n========================================================")
    print(f"  Executing On-Demand Map Tile Ingestion (Bypass Window)")
    print(f"  Target: {args.id}")
    print(f"========================================================")

    out_p = os.path.join(args.output_dir, f"{args.id}_basemap_panel_a.png")
    out_d = os.path.join(args.output_dir, f"{args.id}_basemap_panel_b.png")

    print("\n[Panel A: Primary Habitat Ingestion]")
    download_and_stitch(args.primary_bbox, args.zoom_p, out_p, tile_source=args.tile_source)

    print("\n[Panel B: Domestic Containment Ingestion]")
    download_and_stitch(args.domestic_bbox, args.zoom_d, out_d, tile_source=args.tile_source)

    print("\n[TILE INGESTION COMPLETED - IMMEDIATE NETWORK CUTOFF REQUIRED]")
    sys.exit(0)

if __name__ == "__main__":
    main()
