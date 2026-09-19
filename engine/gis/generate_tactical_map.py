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

def create_circuit_geometries(qgis_core, crs_src, crs_dest):
    """
    Renders a true Continental Great Circuit (Loop Corridor) across Eurasia and the Middle East.
    """
    QgsPointXY = getattr(qgis_core, "QgsPointXY")
    QgsGeometry = getattr(qgis_core, "QgsGeometry")
    QgsCoordinateTransform = getattr(qgis_core, "QgsCoordinateTransform")
    QgsProject = getattr(qgis_core, "QgsProject")

    xform = QgsCoordinateTransform(crs_src, crs_dest, QgsProject.instance())

    # Great Circuit Waypoints (Lon, Lat) across Tibet, Tien Shan, Urals, Caucasus, Levant, Arabia, Iran, Himalayas
    circuit_pts_wgs84 = [
        (85.0, 35.0),   # 1. チベット高原・崑崙山脈（一次コア）
        (88.0, 43.5),   # 2. 天山山脈東部・ジュンガル盆地
        (76.0, 45.0),   # 3. バルハシ湖・カザフステップ
        (62.0, 50.0),   # 4. トルガイ回廊・南ウラル山脈
        (50.0, 47.0),   # 5. カスピ海北岸・ヴォルガ低地
        (43.0, 42.0),   # 6. コーカサス大山脈
        (37.0, 37.0),   # 7. アナトリア東部・メソポタミア北縁
        (36.0, 30.0),   # 8. レバント大断層・紅海地溝帯北端
        (45.0, 24.5),   # 9. アラビア内陸霊脈
        (55.0, 27.5),   # 10. ペルシャ湾・ホルムズ北嶺
        (60.0, 33.0),   # 11. イラン高原・ザグロス東嶺
        (68.0, 34.5),   # 12. ヒンドゥークシュ山脈
        (76.0, 33.0),   # 13. カシミール・カラコルム
        (84.0, 28.5),   # 14. ヒマラヤ中央・ネパール主嶺
        (92.0, 31.0),   # 15. チベット東南部・横断山脈
        (85.0, 35.0),   # 16. 崑崙・チベットへ帰還（閉塞サーキット）
    ]

    pts_3857 = []
    for lon, lat in circuit_pts_wgs84:
        pt = xform.transform(QgsPointXY(lon, lat))
        pts_3857.append(pt)

    line_geom = QgsGeometry.fromPolylineXY(pts_3857)

    # Buffer in EPSG:3857 meters
    geom_outer = line_geom.buffer(280000.0, 8).smooth(2, 0.25)  # 280km buffer
    geom_inner = line_geom.buffer(120000.0, 8).smooth(2, 0.25)  # 120km core corridor

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

    # 3. Dynamic Organic Habitat Layers (Separate Memory Vectors for Panel A and B)
    p_geom_outer, p_geom_inner = create_organic_geometries(qgis_core, p_rect_3857, seed_offset=1.2)
    if "020" in args.id:
        d_geom_outer, d_geom_inner = create_circuit_geometries(qgis_core, crs_4326, crs_3857)
    else:
        d_geom_outer, d_geom_inner = create_organic_geometries(qgis_core, d_rect_3857, seed_offset=3.7)

    # 3.1 Panel A Vector Layer
    mem_poly_a = QgsVectorLayer("Polygon?crs=EPSG:3857&field=zone_type:string", "Habitat Zones Panel A", "memory")
    pr_poly_a = mem_poly_a.dataProvider()
    feat_a_buf = QgsFeature()
    feat_a_buf.setGeometry(p_geom_outer)
    feat_a_buf.setAttributes(["buffer_zone"])
    feat_a_core = QgsFeature()
    feat_a_core.setGeometry(p_geom_inner)
    feat_a_core.setAttributes(["core_zone"])
    pr_poly_a.addFeatures([feat_a_buf, feat_a_core])
    mem_poly_a.updateExtents()

    # 3.2 Panel B Vector Layer
    mem_poly_b = QgsVectorLayer("Polygon?crs=EPSG:3857&field=zone_type:string", "Habitat Zones Panel B", "memory")
    pr_poly_b = mem_poly_b.dataProvider()
    feat_b_buf = QgsFeature()
    feat_b_buf.setGeometry(d_geom_outer)
    feat_b_buf.setAttributes(["buffer_zone"])
    feat_b_core = QgsFeature()
    feat_b_core.setGeometry(d_geom_inner)
    feat_b_core.setAttributes(["core_zone"])
    pr_poly_b.addFeatures([feat_b_buf, feat_b_core])
    mem_poly_b.updateExtents()

    # Styling for Buffer vs Core
    sym_buffer = QgsFillSymbol.createSimple({
        "color": "0,180,255,85",           # Translucent Cyan
        "outline_color": "0,210,255,255",  # Vibrant Cyan Border
        "outline_width": "1.2",
        "outline_style": "dash"
    })
    sym_core = QgsFillSymbol.createSimple({
        "color": "0,220,130,120",          # Translucent Emerald Green
        "outline_color": "0,255,160,255",  # Vibrant Green Border
        "outline_width": "1.5",
        "outline_style": "solid"
    })

    categories_a = [
        QgsRendererCategory("buffer_zone", sym_buffer.clone(), "広域回遊・監視バッファー域"),
        QgsRendererCategory("core_zone", sym_core.clone(), "高密度マナ共鳴・繁殖コア域")
    ]
    mem_poly_a.setRenderer(QgsCategorizedSymbolRenderer("zone_type", categories_a))
    project.addMapLayer(mem_poly_a)

    buffer_b_label = "超大陸グレート・サーキット巡回域 (Great Circuit Range)" if "020" in args.id else "広域監視バッファー帯"
    core_b_label = "一次霊脈・地殻コア回廊帯 (Primary Leyline Core)" if "020" in args.id else "国内隔離保護コア域"

    categories_b = [
        QgsRendererCategory("buffer_zone", sym_buffer.clone(), buffer_b_label),
        QgsRendererCategory("core_zone", sym_core.clone(), core_b_label)
    ]
    mem_poly_b.setRenderer(QgsCategorizedSymbolRenderer("zone_type", categories_b))
    project.addMapLayer(mem_poly_b)

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
    if "020" in args.id or "サーキット" in args.domestic_name or "巡回" in args.domestic_name:
        lbl_b.setText(f"PANEL B: CONTINENTAL GREAT CIRCUIT - {args.domestic_name}\nCOORDS BBOX [{args.domestic_bbox}] // 超大陸マナ・レイライン閉塞回廊帯\n[GREEN: 一次霊脈コア回廊帯 / CYAN: 超大陸グレート・サーキット巡回域]")
    else:
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
    layers_1 = [mem_poly_a]
    if raster_p and raster_p.isValid():
        layers_1.append(raster_p)
    map1.setLayers(layers_1)
    map1.setKeepLayerSet(True)
    map1.setFrameEnabled(True)
    layout.addLayoutItem(map1)

    # --- MAP PANEL 2: Domestic Zone / Continental Circuit (Right) ---
    map2 = QgsLayoutItemMap(layout)
    map2.attemptMove(QgsLayoutPoint(245, 42, QgsUnitTypes.LayoutMillimeters))
    map2.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    map2.setCrs(crs_3857)
    map2.setExtent(d_rect_3857.buffered(d_rect_3857.width() * 0.05))
    map2.setBackgroundColor(QColor(230, 235, 240))
    layers_2 = [mem_poly_b]
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
