# -*- coding: utf-8 -*-
"""
PyQGIS Automated Tactical Map Exporter (Stylized Edition)
Applies semi-transparent styling, neon borders, and tactical labels.
"""

import sys
import os
import importlib

def render_qgis_layout():
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
    output_png = os.path.abspath(os.path.join(script_dir, "../../assets/creatures/004_magma_salamander/004_magma_salamander_qgis_map.png"))
    output_range_png = os.path.abspath(os.path.join(script_dir, "../../assets/creatures/004_magma_salamander/004_magma_salamander_range_map.png"))

    project = QgsProject.instance()
    project.clear()
    crs_3857 = QgsCoordinateReferenceSystem("EPSG:3857")
    project.setCrs(crs_3857)

    # Base Maps
    osm_url = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"
    osm_layer = QgsRasterLayer(osm_url, "OpenStreetMap Base", "wms")
    if osm_layer.isValid():
        project.addMapLayer(osm_layer)

    layers_dir = os.path.join(script_dir, "layers")
    etna_geojson = os.path.join(layers_dir, "etna_habitat.geojson")
    aso_geojson = os.path.join(layers_dir, "aso_habitat.geojson")
    defense_geojson = os.path.join(layers_dir, "defense_infrastructure.geojson")

    # Vector Layers & Styles
    etna_layer = QgsVectorLayer(etna_geojson, "Etna Habitat", "ogr")
    if etna_layer.isValid():
        sym_etna = QgsFillSymbol.createSimple({
            'color': '255,107,43,90',        # Semi-transparent orange
            'outline_color': '255,107,43,255', # Vibrant orange border
            'outline_width': '0.8',
            'outline_style': 'dash'
        })
        etna_layer.setRenderer(QgsSingleSymbolRenderer(sym_etna))
        project.addMapLayer(etna_layer)

    aso_layer = QgsVectorLayer(aso_geojson, "Aso Habitat", "ogr")
    if aso_layer.isValid():
        sym_aso = QgsFillSymbol.createSimple({
            'color': '255,0,110,80',          # Semi-transparent magenta
            'outline_color': '255,0,110,255',  # Vibrant pink border
            'outline_width': '0.8',
            'outline_style': 'dash'
        })
        aso_layer.setRenderer(QgsSingleSymbolRenderer(sym_aso))
        project.addMapLayer(aso_layer)

    defense_layer = QgsVectorLayer(defense_geojson, "Defense Infrastructure", "ogr")
    if defense_layer.isValid():
        sym_def = QgsMarkerSymbol.createSimple({
            'name': 'circle',
            'color': '0,210,255,230',          # Cyan radar dots
            'outline_color': '255,255,255,255',
            'outline_width': '0.4',
            'size': '3.5'
        })
        defense_layer.setRenderer(QgsSingleSymbolRenderer(sym_def))
        project.addMapLayer(defense_layer)

    # Build Print Layout
    layout = QgsLayout(project)
    layout.initializeDefaults()

    page = layout.pageCollection().pages()[0]
    page.setPageSize(QgsLayoutSize(480, 280, QgsUnitTypes.LayoutMillimeters))

    # Background Dark HUD Board
    bg = QgsLayoutItemShape(layout)
    bg.setShapeType(QgsLayoutItemShape.Rectangle)
    try:
        bg.symbol().setColor(QColor(14, 18, 24))
    except Exception:
        pass
    bg.attemptMove(QgsLayoutPoint(0, 0, QgsUnitTypes.LayoutMillimeters))
    bg.attemptResize(QgsLayoutSize(480, 280, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(bg)

    # Title Header
    title_label = QgsLayoutItemLabel(layout)
    title_label.setText("HABITAT & DEPLOYMENT TACTICAL GEOINT // 004 MAGMA SALAMANDER\n[QGIS 3.44 OFFICIAL ENGINE // OPENSTREETMAP & GSI GEO-TILES + VECTOR TELEMETRY]")
    try:
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
    except Exception:
        pass
    title_label.setFontColor(QColor(240, 245, 255))
    title_label.attemptMove(QgsLayoutPoint(15, 8, QgsUnitTypes.LayoutMillimeters))
    title_label.attemptResize(QgsLayoutSize(360, 22, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(title_label)

    # Panel A Label
    lbl_a = QgsLayoutItemLabel(layout)
    lbl_a.setText("PANEL A: PRIMARY NATURAL HABITAT - MT. ETNA (SICILY, ITALY)\nLAT 37°45'N, LON 14°59'E // CRATER 2 MAGMA LAKE [ELDER ALPHA SM +3]")
    try:
        lbl_a.setFont(QFont("Arial", 10, QFont.Bold))
    except Exception:
        pass
    lbl_a.setFontColor(QColor(255, 107, 43))
    lbl_a.attemptMove(QgsLayoutPoint(15, 28, QgsUnitTypes.LayoutMillimeters))
    lbl_a.attemptResize(QgsLayoutSize(220, 10, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(lbl_a)

    # Panel B Label
    lbl_b = QgsLayoutItemLabel(layout)
    lbl_b.setText("PANEL B: JAPAN COLONY - ASO CALDERA (KUMAMOTO, JAPAN)\nLAT 32°53'N, LON 131°05'E // NAKADAKE CRATER 1 FERAL BREEDING [CLASS-B]")
    try:
        lbl_b.setFont(QFont("Arial", 10, QFont.Bold))
    except Exception:
        pass
    lbl_b.setFontColor(QColor(255, 0, 110))
    lbl_b.attemptMove(QgsLayoutPoint(245, 28, QgsUnitTypes.LayoutMillimeters))
    lbl_b.attemptResize(QgsLayoutSize(220, 10, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(lbl_b)

    # Transform coordinates
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
    transform = qgis_core.QgsCoordinateTransform(crs_4326, crs_3857, project)

    # Map Panel 1: Mt. Etna
    map1 = QgsLayoutItemMap(layout)
    map1.attemptMove(QgsLayoutPoint(15, 40, QgsUnitTypes.LayoutMillimeters))
    map1.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    rect_etna = transform.transformBoundingBox(QgsRectangle(14.86, 37.64, 15.22, 37.86))
    map1.setCrs(crs_3857)
    map1.setExtent(rect_etna)
    map1.setFrameEnabled(True)
    layout.addLayoutItem(map1)

    # Map Panel 2: Mt. Aso
    map2 = QgsLayoutItemMap(layout)
    map2.attemptMove(QgsLayoutPoint(245, 40, QgsUnitTypes.LayoutMillimeters))
    map2.attemptResize(QgsLayoutSize(220, 225, QgsUnitTypes.LayoutMillimeters))
    rect_aso = transform.transformBoundingBox(QgsRectangle(130.98, 32.81, 131.20, 32.96))
    map2.setCrs(crs_3857)
    map2.setExtent(rect_aso)
    map2.setFrameEnabled(True)
    layout.addLayoutItem(map2)

    # Export to Image
    exporter = QgsLayoutExporter(layout)
    settings = QgsLayoutExporter.ImageExportSettings()
    settings.dpi = 150

    res = exporter.exportToImage(output_png, settings)
    if res == QgsLayoutExporter.Success:
        print(f"[SUCCESS] Styled QGIS Tactical Map exported: {output_png}")
        import shutil
        shutil.copyfile(output_png, output_range_png)
        print(f"[SUCCESS] Updated creature entry map: {output_range_png}")
    else:
        print(f"[ERROR] Export failed with code: {res}")

    qgs.exitQgis()
    return True

if __name__ == "__main__":
    render_qgis_layout()
