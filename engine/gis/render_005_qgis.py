# -*- coding: utf-8 -*-
"""
PyQGIS Automated Map Renderer for 005 Dew Sprite (アサツユセイレイ)
Generates high-precision QGIS maps for Schwarzwald (Germany) and Aokigahara / Fuji (Japan).
"""

import sys
import os
import importlib

def render_005_map():
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
        QgsRectangle = getattr(qgis_core, "QgsRectangle")
        QgsVectorLayer = getattr(qgis_core, "QgsVectorLayer")
        QgsRasterLayer = getattr(qgis_core, "QgsRasterLayer")
        QgsFillSymbol = getattr(qgis_core, "QgsFillSymbol")
        QgsMarkerSymbol = getattr(qgis_core, "QgsMarkerSymbol")
        QgsSingleSymbolRenderer = getattr(qgis_core, "QgsSingleSymbolRenderer")
        pyqt_gui = importlib.import_module("qgis.PyQt.QtGui")
        QColor = getattr(pyqt_gui, "QColor")
        QFont = getattr(pyqt_gui, "QFont")
    except ImportError as e:
        print(f"[ERROR] PyQGIS import failed: {e}")
        return False

    QgsApplication.setPrefixPath(os.environ.get("QGIS_PREFIX_PATH", r"C:\Program Files\QGIS 3.44.12\apps\qgis-ltr"), True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_png = os.path.abspath(os.path.join(script_dir, "../../assets/creatures/005_dew_sprite/005_dew_sprite_range_map.png"))

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_png), exist_ok=True)

    project = QgsProject.instance()
    project.clear()
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    project.setCrs(crs_3857)

    # Base Map (OpenStreetMap)
    osm_url = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
    osm_layer = QgsRasterLayer(osm_url, "OpenStreetMap Base", "wms")
    if osm_layer.isValid():
        project.addMapLayer(osm_layer)

    # Layers
    layers_dir = os.path.join(script_dir, "layers")
    schwarz_geojson = os.path.join(layers_dir, "005_schwarzwald_habitat.geojson")
    aoki_geojson = os.path.join(layers_dir, "005_aokigahara_habitat.geojson")

    schwarz_layer = QgsVectorLayer(schwarz_geojson, "Schwarzwald Habitat", "ogr")
    if schwarz_layer.isValid():
        sym_s = QgsFillSymbol.createSimple({
            'color': '0,200,150,85',           # Translucent Emerald
            'outline_color': '0,255,180,255',   # Vibrant Cyan-Green
            'outline_width': '0.9',
            'outline_style': 'dash'
        })
        schwarz_layer.setRenderer(QgsSingleSymbolRenderer(sym_s))
        project.addMapLayer(schwarz_layer)

    aoki_layer = QgsVectorLayer(aoki_geojson, "Aokigahara Habitat", "ogr")
    if aoki_layer.isValid():
        sym_a = QgsFillSymbol.createSimple({
            'color': '0,180,255,85',           # Translucent Cyan
            'outline_color': '0,220,255,255',  # Vibrant Cyan Border
            'outline_width': '0.9',
            'outline_style': 'dash'
        })
        aoki_layer.setRenderer(QgsSingleSymbolRenderer(sym_a))
        project.addMapLayer(aoki_layer)

    # Build Print Layout
    layout = QgsLayout(project)
    layout.initializeDefaults()

    page = layout.pageCollection().pages()[0]
    page.setPageSize(QgsLayoutSize(480, 280, QgsUnitTypes.LayoutMillimeters))

    # Background Dark HUD Board
    bg = QgsLayoutItemShape(layout)
    bg.setShapeType(QgsLayoutItemShape.Rectangle)
    try:
        bg.symbol().setColor(QColor(12, 16, 22))
    except Exception:
        pass
    bg.attemptMove(QgsLayoutPoint(0, 0, QgsUnitTypes.LayoutMillimeters))
    bg.attemptResize(QgsLayoutSize(480, 280, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(bg)

    # Main Header Label
    title_label = QgsLayoutItemLabel(layout)
    title_label.setText("ECOLOGICAL SANCTUARY GEOINT // 005 DEW SPRITE [アサツユセイレイ]\n[QGIS 3.44 OFFICIAL ENGINE // OPENSTREETMAP BASE TILES + IUCN SANCTUARY VECTORS]")
    try:
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
    except Exception:
        pass
    title_label.setFontColor(QColor(240, 245, 255))
    title_label.attemptMove(QgsLayoutPoint(15, 8, QgsUnitTypes.LayoutMillimeters))
    title_label.attemptResize(QgsLayoutSize(380, 22, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(title_label)

    # Panel A Label: Germany Schwarzwald
    lbl_a = QgsLayoutItemLabel(layout)
    lbl_a.setText("PANEL A: PRIMARY NATURAL SANCTUARY - SCHWARZWALD (BADEN-WÜRTTEMBERG, GERMANY)\nFREIBURG / TITISEE / FELDBERG MIST ZONE // LAT 47°54'N, LON 8°08'E [ELEV 800-1,200m]")
    try:
        lbl_a.setFont(QFont("Arial", 10, QFont.Bold))
    except Exception:
        pass
    lbl_a.setFontColor(QColor(0, 255, 180))
    lbl_a.attemptMove(QgsLayoutPoint(15, 28, QgsUnitTypes.LayoutMillimeters))
    lbl_a.attemptResize(QgsLayoutSize(220, 10, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(lbl_a)

    # Panel B Label: Japan Aokigahara & Fuji Five Lakes
    lbl_b = QgsLayoutItemLabel(layout)
    lbl_b.setText("PANEL B: DOMESTIC SACRED SANCTUARY - AOKIGAHARA & FUJI FIVE LAKES (YAMANASHI, JAPAN)\nLAKE SAIKO / SHOJIKO / ROUTE 139 MOSS CORRIDOR // LAT 35°28'N, LON 138°38'E")
    try:
        lbl_b.setFont(QFont("Arial", 10, QFont.Bold))
    except Exception:
        pass
    lbl_b.setFontColor(QColor(0, 210, 255))
    lbl_b.attemptMove(QgsLayoutPoint(245, 28, QgsUnitTypes.LayoutMillimeters))
    lbl_b.attemptResize(QgsLayoutSize(220, 10, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(lbl_b)

    # Coordinate Transform
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    transform = qgis_core.QgsCoordinateTransform(crs_4326, crs_3857, project)

    # Map Panel 1: Schwarzwald (Freiburg, Titisee, Feldberg)
    map1 = QgsLayoutItemMap(layout)
    map1.attemptMove(QgsLayoutPoint(15, 40, QgsUnitTypes.LayoutMillimeters))
    map1.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    rect_schwarz = transform.transformBoundingBox(QgsRectangle(7.82, 47.78, 8.32, 48.06))
    map1.setCrs(crs_3857)
    map1.setExtent(rect_schwarz)
    if osm_layer.isValid() and schwarz_layer.isValid():
        map1.setLayers([schwarz_layer, osm_layer])
        map1.setKeepLayerSet(True)
    map1.setFrameEnabled(True)
    layout.addLayoutItem(map1)

    # Map Panel 2: Aokigahara / Fuji Five Lakes (Saiko, Shojiko, Motosuko)
    map2 = QgsLayoutItemMap(layout)
    map2.attemptMove(QgsLayoutPoint(245, 40, QgsUnitTypes.LayoutMillimeters))
    map2.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    rect_aoki = transform.transformBoundingBox(QgsRectangle(138.54, 35.40, 138.74, 35.54))
    map2.setCrs(crs_3857)
    map2.setExtent(rect_aoki)
    if osm_layer.isValid() and aoki_layer.isValid():
        map2.setLayers([aoki_layer, osm_layer])
        map2.setKeepLayerSet(True)
    map2.setFrameEnabled(True)
    layout.addLayoutItem(map2)

    # Export
    exporter = QgsLayoutExporter(layout)
    settings = QgsLayoutExporter.ImageExportSettings()
    settings.dpi = 150

    res = exporter.exportToImage(output_png, settings)
    if res == QgsLayoutExporter.Success:
        print(f"[SUCCESS] QGIS 005 Sanctuary Map rendered: {output_png}")
    else:
        print(f"[ERROR] Export failed with error code: {res}")

    qgs.exitQgis()
    return True

if __name__ == "__main__":
    render_005_map()
