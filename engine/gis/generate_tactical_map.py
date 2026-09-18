# -*- coding: utf-8 -*-
"""
QGIS Automated Tactical GEOINT Engine (Offline Render Mode)
Renders high-precision, 2-panel tactical surveillance maps (EPSG:3857)
Panel A: Primary Wildlife Habitat (Mythological Origin / Overseas Primary Zone)
Panel B: Domestic Containment / Fortified Outland Zone (Japan Model)

Features:
- Consumes pre-fetched local high-resolution CartoDB / OSM basemap rasters
- Completely isolated from external network (BypassSandbox: false compliant)
- Organic eco-contour dual-zone polygons (Core Sanctuary + Buffer Range)
- Tactical dark HUD styling with glowing overlays
"""

import sys
import os
import math
import argparse
import importlib

# Mechanical Sandbox Security Guardrail:
# Ensure external network is 100% CUT OFF before initiating offline tactical render
try:
    from assert_network_isolated import check_isolation_boolean
except ImportError:
    # If run from root directory
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from assert_network_isolated import check_isolation_boolean

def parse_args():
    parser = argparse.ArgumentParser(description="QGIS Tactical Map Automated Offline Renderer")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 019_forest_mirage_chameleon)")
    parser.add_argument("--title", required=True, help="Map Title Japanese")
    parser.add_argument("--primary-name", required=True, help="Primary Habitat Name")
    parser.add_argument("--primary-bbox", required=True, help="minLon,minLat,maxLon,maxLat")
    parser.add_argument("--domestic-name", required=True, help="Domestic Zone Name")
    parser.add_argument("--domestic-bbox", required=True, help="minLon,minLat,maxLon,maxLat")
    parser.add_argument("--tile-dir", required=True, help="Directory containing pre-fetched basemap tiles")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--mana-freq", default="490-530nm / 220 mU/m³", help="Mana Resonance Frequency")
    parser.add_argument("--threat-level", default="Threat Level: III", help="Threat Level string")
    return parser.parse_args()

def create_organic_geometries(qgis_core, rect, seed_offset=0.0):
    QgsPointXY = getattr(qgis_core, "QgsPointXY")
    QgsGeometry = getattr(qgis_core, "QgsGeometry")

    cx = (rect.xMinimum() + rect.xMaximum()) / 2.0
    cy = (rect.yMinimum() + rect.yMaximum()) / 2.0
    rx = rect.width() / 2.0 * 0.85
    ry = rect.height() / 2.0 * 0.85

    num_pts = 20

    # 1. Outer Buffer Zone
    pts_outer = []
    for i in range(num_pts):
        th = 2.0 * math.pi * i / num_pts
        wobble = 1.0 + 0.16 * math.sin(3 * th + seed_offset) + 0.10 * math.cos(5 * th + seed_offset * 1.4)
        px = cx + rx * math.cos(th) * wobble
        py = cy + ry * math.sin(th) * wobble
        pts_outer.append(QgsPointXY(px, py))
    pts_outer.append(pts_outer[0])

    # 2. Inner Core Zone
    pts_inner = []
    for i in range(num_pts):
        th = 2.0 * math.pi * i / num_pts
        wobble = 0.52 * (1.0 + 0.20 * math.cos(3 * th + seed_offset + 0.8) + 0.12 * math.sin(4 * th + 1.2))
        px = cx + rx * math.cos(th) * wobble
        py = cy + ry * math.sin(th) * wobble
        pts_inner.append(QgsPointXY(px, py))
    pts_inner.append(pts_inner[0])

    geom_outer = QgsGeometry.fromPolygonXY([pts_outer]).smooth(2, 0.25)
    geom_inner = QgsGeometry.fromPolygonXY([pts_inner]).smooth(2, 0.25)

    return geom_outer, geom_inner

def render_map():
    args = parse_args()

    print("\n[SECURITY AUDIT] Mechanically verifying Sandbox Network Isolation...")
    if not check_isolation_boolean(verbose=True):
        print("\n[CRITICAL ERROR / SECURITY BLOCK] External network connection detected!")
        print("Tactical map rendering is strictly BLOCKED while external network is active.")
        print("Ensure BypassSandbox is false and network port is completely closed before rendering.")
        return False
    print("  ✓ Sandbox network isolation confirmed. Proceeding with offline QGIS render.\n")

    try:
        qgis_core = importlib.import_module("qgis.core")
        QgsApplication = getattr(qgis_core, "QgsApplication")
        QgsProject = getattr(qgis_core, "QgsProject")
        QgsLayout = getattr(qgis_core, "QgsLayout")
        QgsLayoutItemMap = getattr(qgis_core, "QgsLayoutItemMap")
        QgsLayoutItemLabel = getattr(qgis_core, "QgsLayoutItemLabel")
        QgsLayoutItemShape = getattr(qgis_core, "QgsLayoutItemShape")
        QgsLayoutExporter = getattr(qgis_core, "QgsLayoutExporter")
        QgsLayoutPoint = getattr(qgis_core, "QgsLayoutPoint")
        QgsLayoutSize = getattr(qgis_core, "QgsLayoutSize")
        QgsUnitTypes = getattr(qgis_core, "QgsUnitTypes")
        QgsCoordinateReferenceSystem = getattr(qgis_core, "QgsCoordinateReferenceSystem")
        QgsCoordinateTransform = getattr(qgis_core, "QgsCoordinateTransform")
        QgsRectangle = getattr(qgis_core, "QgsRectangle")
        QgsFeature = getattr(qgis_core, "QgsFeature")
        QgsVectorLayer = getattr(qgis_core, "QgsVectorLayer")
        QgsRasterLayer = getattr(qgis_core, "QgsRasterLayer")
        QgsFillSymbol = getattr(qgis_core, "QgsFillSymbol")
        QgsCategorizedSymbolRenderer = getattr(qgis_core, "QgsCategorizedSymbolRenderer")
        QgsRendererCategory = getattr(qgis_core, "QgsRendererCategory")

        pyqt_gui = importlib.import_module("qgis.PyQt.QtGui")
        QColor = getattr(pyqt_gui, "QColor")
        QFont = getattr(pyqt_gui, "QFont")
    except ImportError as e:
        print(f"[ERROR] PyQGIS import failed: {e}")
        return False

    prefix = os.environ.get("QGIS_PREFIX_PATH", r"C:\Program Files\QGIS 3.44.12\apps\qgis-ltr")
    QgsApplication.setPrefixPath(prefix, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    output_png = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output_png), exist_ok=True)

    project = QgsProject.instance()
    project.clear()
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    project.setCrs(crs_3857)

    transform_4326_to_3857 = QgsCoordinateTransform(crs_4326, crs_3857, project)

    # 1. Parse Bounding Boxes
    p_coords = [float(x.strip()) for x in args.primary_bbox.split(",")]
    d_coords = [float(x.strip()) for x in args.domestic_bbox.split(",")]

    p_rect_4326 = QgsRectangle(p_coords[0], p_coords[1], p_coords[2], p_coords[3])
    d_rect_4326 = QgsRectangle(d_coords[0], d_coords[1], d_coords[2], d_coords[3])

    p_rect_3857 = transform_4326_to_3857.transformBoundingBox(p_rect_4326)
    d_rect_3857 = transform_4326_to_3857.transformBoundingBox(d_rect_4326)

    # 2. Load Pre-fetched Local Basemaps
    basemap_p_path = os.path.join(args.tile_dir, f"{args.id}_basemap_panel_a.png")
    basemap_d_path = os.path.join(args.tile_dir, f"{args.id}_basemap_panel_b.png")

    raster_p = None
    raster_d = None

    if os.path.exists(basemap_p_path):
        raster_p = QgsRasterLayer(basemap_p_path, "Basemap Panel A")
        if raster_p.isValid():
            raster_p.setCrs(crs_3857)
            project.addMapLayer(raster_p)
            print(f"[INFO] Successfully loaded and attached Panel A basemap raster: {basemap_p_path}")
        else:
            print(f"[WARN] raster_p exists but failed to validate: {basemap_p_path}")

    if os.path.exists(basemap_d_path):
        raster_d = QgsRasterLayer(basemap_d_path, "Basemap Panel B")
        if raster_d.isValid():
            raster_d.setCrs(crs_3857)
            project.addMapLayer(raster_d)
            print(f"[INFO] Successfully loaded and attached Panel B basemap raster: {basemap_d_path}")
        else:
            print(f"[WARN] raster_d exists but failed to validate: {basemap_d_path}")

    # 3. Dynamic Organic Habitat Layer (Memory Vector)
    mem_poly = QgsVectorLayer("Polygon?crs=EPSG:3857&field=zone_type:string", "Organic Habitat Zones", "memory")
    pr_poly = mem_poly.dataProvider()

    p_geom_outer, p_geom_inner = create_organic_geometries(qgis_core, p_rect_3857, seed_offset=1.2)
    d_geom_outer, d_geom_inner = create_organic_geometries(qgis_core, d_rect_3857, seed_offset=3.7)

    features = []
    for geom, ztype in [(p_geom_outer, "buffer_zone"), (p_geom_inner, "core_zone"),
                        (d_geom_outer, "buffer_zone"), (d_geom_inner, "core_zone")]:
        feat = QgsFeature()
        feat.setGeometry(geom)
        feat.setAttributes([ztype])
        features.append(feat)

    pr_poly.addFeatures(features)
    mem_poly.updateExtents()

    # Styling for Buffer vs Core (High transparency for topographic clarity)
    sym_buffer = QgsFillSymbol.createSimple({
        "color": "0,180,255,75",           # Translucent Cyan
        "outline_color": "0,200,255,255",  # Vibrant Cyan Border
        "outline_width": "1.0",
        "outline_style": "dash"
    })
    sym_core = QgsFillSymbol.createSimple({
        "color": "0,200,130,95",           # Translucent Emerald Green
        "outline_color": "0,255,160,255",  # Vibrant Green Border
        "outline_width": "1.2",
        "outline_style": "solid"
    })

    categories = [
        QgsRendererCategory("buffer_zone", sym_buffer, "広域回遊・監視バッファー域 (Buffer Range)"),
        QgsRendererCategory("core_zone", sym_core, "高密度マナ共鳴・繁殖コア域 (Core Sanctuary)")
    ]
    renderer = QgsCategorizedSymbolRenderer("zone_type", categories)
    mem_poly.setRenderer(renderer)
    project.addMapLayer(mem_poly)

    # 4. Print Layout Setup (480 x 280 mm)
    layout = QgsLayout(project)
    layout.initializeDefaults()

    page = layout.pageCollection().pages()[0]
    page.setPageSize(QgsLayoutSize(480, 280, QgsUnitTypes.LayoutMillimeters))

    # Background: Tactical Dark Outer Frame
    bg_shape = QgsLayoutItemShape(layout)
    bg_shape.setShapeType(QgsLayoutItemShape.Rectangle)
    try:
        bg_shape.symbol().setColor(QColor(10, 15, 22))
    except Exception:
        pass
    bg_shape.attemptMove(QgsLayoutPoint(0, 0, QgsUnitTypes.LayoutMillimeters))
    bg_shape.attemptResize(QgsLayoutSize(480, 280, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(bg_shape)

    # Main Header Label
    title_lbl = QgsLayoutItemLabel(layout)
    title_lbl.setText(f"ECOLOGICAL SANCTUARY GEOINT // {args.id.upper()} [{args.title}]\n[QGIS 3.44 OFFICIAL ENGINE // GLOBAL TERRAIN SHADED RELIEF + DUAL-ZONE ECO-CONTOUR VECTORS]")
    try:
        title_lbl.setFont(QFont("Arial", 14, QFont.Bold))
    except Exception:
        pass
    title_lbl.setFontColor(QColor(240, 245, 255))
    title_lbl.attemptMove(QgsLayoutPoint(15, 8, QgsUnitTypes.LayoutMillimeters))
    title_lbl.attemptResize(QgsLayoutSize(450, 22, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(title_lbl)

    # Panel A Label
    lbl_a = QgsLayoutItemLabel(layout)
    lbl_a.setText(f"PANEL A: PRIMARY NATURAL HABITAT - {args.primary_name}\nCOORDS BBOX [{args.primary_bbox}] // {args.threat_level} // MANA: {args.mana_freq}\n[GREEN: 高密度繁殖コア域 / CYAN: 広域回遊バッファー帯]")
    try:
        lbl_a.setFont(QFont("Arial", 9, QFont.Bold))
    except Exception:
        pass
    lbl_a.setFontColor(QColor(0, 255, 180))
    lbl_a.attemptMove(QgsLayoutPoint(15, 26, QgsUnitTypes.LayoutMillimeters))
    lbl_a.attemptResize(QgsLayoutSize(220, 14, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(lbl_a)

    # Panel B Label
    lbl_b = QgsLayoutItemLabel(layout)
    lbl_b.setText(f"PANEL B: DOMESTIC CONTAINMENT - {args.domestic_name}\nCOORDS BBOX [{args.domestic_bbox}] // 多層結界防衛網＆メガコーポ研究ドーム\n[GREEN: 国内隔離保護コア域 / CYAN: 警戒監視バッファー帯]")
    try:
        lbl_b.setFont(QFont("Arial", 9, QFont.Bold))
    except Exception:
        pass
    lbl_b.setFontColor(QColor(0, 210, 255))
    lbl_b.attemptMove(QgsLayoutPoint(245, 26, QgsUnitTypes.LayoutMillimeters))
    lbl_b.attemptResize(QgsLayoutSize(220, 14, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(lbl_b)

    # --- MAP PANEL 1: Primary Habitat (Left) ---
    map1 = QgsLayoutItemMap(layout)
    map1.attemptMove(QgsLayoutPoint(15, 42, QgsUnitTypes.LayoutMillimeters))
    map1.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    map1.setCrs(crs_3857)
    map1.setExtent(p_rect_3857.buffered(p_rect_3857.width() * 0.15))
    map1.setBackgroundColor(QColor(230, 235, 240))
    layers_1 = [mem_poly]
    if raster_p and raster_p.isValid():
        layers_1.append(raster_p)
    map1.setLayers(layers_1)
    map1.setKeepLayerSet(True)
    map1.setFrameEnabled(True)
    layout.addLayoutItem(map1)

    # --- MAP PANEL 2: Domestic Zone (Right) ---
    map2 = QgsLayoutItemMap(layout)
    map2.attemptMove(QgsLayoutPoint(245, 42, QgsUnitTypes.LayoutMillimeters))
    map2.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    map2.setCrs(crs_3857)
    map2.setExtent(d_rect_3857.buffered(d_rect_3857.width() * 0.15))
    map2.setBackgroundColor(QColor(230, 235, 240))
    layers_2 = [mem_poly]
    if raster_d and raster_d.isValid():
        layers_2.append(raster_d)
    map2.setLayers(layers_2)
    map2.setKeepLayerSet(True)
    map2.setFrameEnabled(True)
    layout.addLayoutItem(map2)

    # 5. Export Layout to PNG
    exporter = QgsLayoutExporter(layout)
    settings = QgsLayoutExporter.ImageExportSettings()
    settings.dpi = 150

    res = exporter.exportToImage(output_png, settings)
    if res == QgsLayoutExporter.Success:
        print(f"[SUCCESS] QGIS Tactical Map Exported: {output_png}")
        print(f"[INFO] Image Size: {os.path.getsize(output_png):,} bytes")
        qgs.exitQgis()
        return True
    else:
        print(f"[ERROR] Export failed with error code: {res}")
        qgs.exitQgis()
        return False

if __name__ == "__main__":
    if render_map():
        sys.exit(0)
    else:
        sys.exit(1)
