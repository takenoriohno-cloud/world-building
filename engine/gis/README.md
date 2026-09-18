# QGIS 戦術地理情報パイプライン (QGIS Tactical GEOINT Pipeline)

本ディレクトリは、オープンソースGISの業界標準である **QGIS (Quantum GIS)** を用いて、魔獣生息分布図・作戦タクティカルマップを高精度レンダリングするための公式GIS資産および自動化スクリプト群です。

---

## 📁 ディレクトリ構成

- **`project/magma_salamander_tactical.qgs`**: 
  - QGIS公式プロジェクトファイル（XML形式）。
  - WGS84 / WebMercator (EPSG:3857) 投影法。
  - 国土地理院（淡色地図/標高タイル）、OpenStreetMap、および各GeoJSONレイヤーを統合。
  - 印刷レイアウト（Print Layout）`Magma_Salamander_Tactical_Geoint` を定義済み。
- **`layers/`**: 
  - 本プロジェクトの正史地理ベクターデータ（GeoJSON形式）。
  - `etna_habitat.geojson`: エトナ山第2火口原、溶岩湖、火霊マナ共鳴円、ボヴェ渓谷回廊。
  - `aso_habitat.geojson`: 阿蘇中岳第1火口原、大外輪山防護壁ライン、地熱発電所警戒区。
  - `defense_infrastructure.geojson`: カターニャ軍港、メッシーナ海峡ゲート、阿蘇大観峰レーダー神殿など。
- **`render_qgis.py`**:
  - PyQGIS (Python API) による完全ヘッドレス自動レンダリングスクリプト。
- **`render-qgis-map.ps1`**:
  - Windows環境向けワンクリック実行スクリプト。PC内のQGISインストールを自動検知してエクスポートを実行します。

---

## 🚀 使い方

### 1. QGISデスクトップアプリでGUI編集する場合
1. [QGIS公式サイト (qgis.org)](https://qgis.org/) から QGIS（推奨: 3.34 LTR 以上）をダウンロード・インストールします。
2. `project/magma_salamander_tactical.qgs` をダブルクリック（またはQGISから「プロジェクトを開く」）。
3. 地理院地図やOSMの上に、エトナ山や阿蘇山の生息域・軍事拠点が正確な緯度経度でプロットされます。
4. メニューの「プロジェクト」→「レイアウトマネージャ」から、定義済みのプリントレイアウトを開いてPDF/画像出力や自由なレイアウト編集が可能です。

### 2. コマンドラインから全自動レンダリングする場合
PowerShellから以下のスクリプトを実行するだけで、高精細PNG画像が一撃で生成されます：
```powershell
powershell -ExecutionPolicy Bypass -File .\engine\gis\render-qgis-map.ps1
```
