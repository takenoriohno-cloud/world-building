# -*- coding: utf-8 -*-
"""
QGIS Automated Tactical GEOINT Engine (SDD Pipeline)
Generates high-precision, 2-panel tactical surveillance maps (EPSG:3857)
Panel A: Primary Wildlife Habitat (Mythological Origin / Overseas Primary Zone)
Panel B: Domestic Containment / Fortified Outland Zone (Japan Model)

Features organic eco-contour dual-zone polygons (Core Sanctuary + Buffer Range)
with smooth Bézier geometry modeling real-world wildlife distribution.
"""

import sys
import os
import math
import argparse
import importlib

def parse_args():
    parser = argparse.ArgumentParser(description="QGIS Tactical Map Automated Renderer")
    parser.add_argument("--id", required=True, help="Creature ID (e.g. 006_carbuncle)")
    parser.add_argument("--title", required=True, help="Map Title Japanese (e.g. ベニビタイオポッサム 生息・保護タクティカルマップ)")
    parser.add_argument("--primary-name", required=True, help="Primary Habitat Name (e.g. 南米ギアナ高地・ロライマ山塊)")
    parser.add_argument("--primary-bbox", required=True, help="minLon,minLat,maxLon,maxLat (e.g. -61.0,5.0,-60.5,5.4)")
    parser.add_argument("--domestic-name", required=True, help="Domestic Zone Name (e.g. 奥多摩・丹沢山系特別保護区)")
    parser.add_argument("--domestic-bbox", required=True, help="minLon,minLat,maxLon,maxLat (e.g. 138.9,35.6,139.3,35.9)")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--mana-freq", default="520nm / 180 mU/m³", help="Mana Resonance Frequency & Density")
    parser.add_argument("--threat-level", default="Threat Level: I〜II", help="Threat Level string")
    return parser.parse_args()

def create_organic_geometries(qgis_core, rect, seed_offset=0.0):
    """
    Generates natural, organic eco-contour dual-zone polygons (Outer Buffer & Inner Core)
    using harmonic wave modulation and Bézier smoothing instead of artificial rectangles.
    """
    QgsPointXY = getattr(qgis_core, "QgsPointXY")
    QgsGeometry = getattr(qgis_core, "QgsGeometry")

    cx = (rect.xMinimum() + rect.xMaximum()) / 2.0
    cy = (rect.yMinimum() + rect.yMaximum()) / 2.0
    rx = rect.width() / 2.0 * 0.88
    ry = rect.height() / 2.0 * 0.88

    num_pts = 20

    # 1. Outer Buffer Zone (Wobble ~15-25%)
    pts_outer = []
    for i in range(num_pts):
        th = 2.0 * math.pi * i / num_pts
        wobble = 1.0 + 0.16 * math.sin(3 * th + seed_offset) + 0.10 * math.cos(5 * th + seed_offset * 1.4)
        px = cx + rx * math.cos(th) * wobble
        py = cy + ry * math.sin(th) * wobble
        pts_outer.append(QgsPointXY(px, py))
    pts_outer.append(pts_outer[0]) # close ring

    # 2. Inner Core Zone (Radius ~55%, different harmonic offset)
    pts_inner = []
    for i in range(num_pts):
        th = 2.0 * math.pi * i / num_pts
        wobble = 0.55 * (1.0 + 0.20 * math.cos(3 * th + seed_offset + 0.8) + 0.12 * math.sin(4 * th + 1.2))
        px = cx + rx * math.cos(th) * wobble
        py = cy + ry * math.sin(th) * wobble
        pts_inner.append(QgsPointXY(px, py))
    pts_inner.append(pts_inner[0]) # close ring

    geom_outer = QgsGeometry.fromPolygonXY([pts_outer]).smooth(2, 0.25)
    geom_inner = QgsGeometry.fromPolygonXY([pts_inner]).smooth(2, 0.25)

    return geom_outer, geom_inner

def render_map():
    args = parse_args()

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
        QgsField = getattr(qgis_core, "QgsField")
        QgsFields = getattr(qgis_core, "QgsFields")
        QgsVectorLayer = getattr(qgis_core, "QgsVectorLayer")
        QgsRasterLayer = getattr(qgis_core, "QgsRasterLayer")
        QgsFillSymbol = getattr(qgis_core, "QgsFillSymbol")
        QgsCategorizedSymbolRenderer = getattr(qgis_core, "QgsCategorizedSymbolRenderer")
        QgsRendererCategory = getattr(qgis_core, "QgsRendererCategory")

        pyqt_gui = importlib.import_module("qgis.PyQt.QtGui")
        QColor = getattr(pyqt_gui, "QColor")
        QFont = getattr(pyqt_gui, "QFont")
        pyqt_core = importlib.import_module("qgis.PyQt.QtCore")
        QVariant = getattr(pyqt_core, "QVariant")
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

    # 1. Base Map (OpenStreetMap XYZ)
    osm_url = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
    osm_layer = QgsRasterLayer(osm_url, "OpenStreetMap Base", "wms")
    if osm_layer.isValid():
        project.addMapLayer(osm_layer)

    # 2. Parse Bounding Boxes
    p_coords = [float(x.strip()) for x in args.primary_bbox.split(",")]
    d_coords = [float(x.strip()) for x in args.domestic_bbox.split(",")]

    p_rect_4326 = QgsRectangle(p_coords[0], p_coords[1], p_coords[2], p_coords[3])
    d_rect_4326 = QgsRectangle(d_coords[0], d_coords[1], d_coords[2], d_coords[3])

    p_rect_3857 = transform_4326_to_3857.transformBoundingBox(p_rect_4326)
    d_rect_3857 = transform_4326_to_3857.transformBoundingBox(d_rect_4326)

    # 3. Dynamic Organic Habitat Layer (Memory Vector with Categories)
    mem_poly = QgsVectorLayer("Polygon?crs=EPSG:3857&field=zone_type:string", "Organic Habitat Zones", "memory")
    pr_poly = mem_poly.dataProvider()

    # Generate organic geometries with distinct seeds
    p_geom_outer, p_geom_inner = create_organic_geometries(qgis_core, p_rect_3857, seed_offset=1.2)
    d_geom_outer, d_geom_inner = create_organic_geometries(qgis_core, d_rect_3857, seed_offset=3.7)

    features = []
    # Primary Features
    f_p_out = QgsFeature()
    f_p_out.setGeometry(p_geom_outer)
    f_p_out.setAttributes(["buffer_zone"])
    features.append(f_p_out)

    f_p_in = QgsFeature()
    f_p_in.setGeometry(p_geom_inner)
    f_p_in.setAttributes(["core_zone"])
    features.append(f_p_in)

    # Domestic Features
    f_d_out = QgsFeature()
    f_d_out.setGeometry(d_geom_outer)
    f_d_out.setAttributes(["buffer_zone"])
    features.append(f_d_out)

    f_d_in = QgsFeature()
    f_d_in.setGeometry(d_geom_inner)
    f_d_in.setAttributes(["core_zone"])
    features.append(f_d_in)

    pr_poly.addFeatures(features)
    mem_poly.updateExtents()

    # Categorized Styling for Buffer vs Core
    sym_buffer = QgsFillSymbol.createSimple({
        "color": "0,204,255,40",           # Translucent Cyan
        "outline_color": "0,220,255,220",  # Cyan dashed boundary
        "outline_width": "0.7",
        "outline_style": "dash"
    })
    sym_core = QgsFillSymbol.createSimple({
        "color": "0,255,180,80",           # Vibrant Emerald Green (Core Sanctuary)
        "outline_color": "0,255,200,255",  # Sharp Glowing Border
        "outline_width": "0.9",
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

    # Background: Tactical Dark
    bg_shape = QgsLayoutItemShape(layout)
    bg_shape.setShapeType(QgsLayoutItemShape.Rectangle)
    try:
        bg_shape.symbol().setColor(QColor(12, 16, 22))
    except Exception:
        pass
    bg_shape.attemptMove(QgsLayoutPoint(0, 0, QgsUnitTypes.LayoutMillimeters))
    bg_shape.attemptResize(QgsLayoutSize(480, 280, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(bg_shape)

    # Main Header Label
    title_lbl = QgsLayoutItemLabel(layout)
    title_lbl.setText(f"ECOLOGICAL SANCTUARY GEOINT // {args.id.upper()} [{args.title}]\n[QGIS 3.44 OFFICIAL ENGINE // OPENSTREETMAP BASE TILES + DUAL-ZONE ECO-CONTOUR VECTORS]")
    try:
        title_lbl.setFont(QFont("Arial", 14, QFont.Bold))
    except Exception:
        pass
    title_lbl.setFontColor(QColor(240, 245, 255))
    title_lbl.attemptMove(QgsLayoutPoint(15, 8, QgsUnitTypes.LayoutMillimeters))
    title_lbl.attemptResize(QgsLayoutSize(450, 22, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(title_lbl)

    # Panel A Label: Primary Habitat (Left)
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

    # Panel B Label: Domestic Zone (Right)
    lbl_b = QgsLayoutItemLabel(layout)
    lbl_b.setText(f"PANEL B: DOMESTIC ZONE - {args.domestic_name}\nCOORDS BBOX [{args.domestic_bbox}] // 多層結界防衛網＆アウトランド警戒回廊\n[GREEN: 国内保護コア域 / CYAN: 監視網バッファー帯]")
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
    map1.setExtent(p_rect_3857.buffered(p_rect_3857.width() * 0.18))
    if osm_layer.isValid() and mem_poly.isValid():
        map1.setLayers([mem_poly, osm_layer])
        map1.setKeepLayerSet(True)
    map1.setFrameEnabled(True)
    layout.addLayoutItem(map1)

    # --- MAP PANEL 2: Domestic Zone (Right) ---
    map2 = QgsLayoutItemMap(layout)
    map2.attemptMove(QgsLayoutPoint(245, 42, QgsUnitTypes.LayoutMillimeters))
    map2.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    map2.setCrs(crs_3857)
    map2.setExtent(d_rect_3857.buffered(d_rect_3857.width() * 0.18))
    if osm_layer.isValid() and mem_poly.isValid():
        map2.setLayers([mem_poly, osm_layer])
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
