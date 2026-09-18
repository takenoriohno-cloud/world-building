# Antigravity IDE - DEM Hillshade & Tactical Map Generator
# Generates a high-precision 2-panel shaded relief & tactical map (PNG) using .NET Graphics

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Drawing.Imaging

$width = 2400
$height = 1360
$bmp = New-Object System.Drawing.Bitmap($width, $height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic

# Background
$bgBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 10, 14, 22))
$g.FillRectangle($bgBrush, 0, 0, $width, $height)

# --- Fonts & Brushes ---
$titleFont = New-Object System.Drawing.Font('Segoe UI', 24, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font('Consolas', 13, [System.Drawing.FontStyle]::Regular)
$headerFont = New-Object System.Drawing.Font('Segoe UI', 16, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font('Segoe UI', 12, [System.Drawing.FontStyle]::Bold)
$smallFont = New-Object System.Drawing.Font('Consolas', 11, [System.Drawing.FontStyle]::Regular)

$orangeBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 102, 34))
$cyanBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 0, 204, 255))
$whiteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 240, 245, 255))
$grayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 130, 155, 190))
$pinkBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 0, 85))

# Top Banner
$bannerPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 45, 65, 100), 2)
$bannerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 16, 23, 38))
$g.FillRectangle($bannerBrush, 40, 30, 2320, 95)
$g.DrawRectangle($bannerPen, 40, 30, 2320, 95)

$g.DrawString('ヨウガンヒトカゲ（溶岩火蜥蜴） 実標高DEM＆地誌タクティカルマップ', $titleFont, $orangeBrush, [float]65, [float]45)
$g.DrawString('HIGH-PRECISION DEM SHADED RELIEF & TOPOGRAPHIC SURVEILLANCE / GSI & COPERNICUS 30M DATA', $subFont, $grayBrush, [float]65, [float]88)

# =========================================================================
# HELPER: DRAW SHADED RELIEF DEM GRID
# =========================================================================
function Draw-DemPanel($pX, $pY, $pW, $pH, $type) {
    $pBg = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 18, 25, 38))
    $pBorder = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 55, 80, 120), 2.5)
    $g.FillRectangle($pBg, [float]$pX, [float]$pY, [float]$pW, [float]$pH)
    $g.DrawRectangle($pBorder, [float]$pX, [float]$pY, [float]$pW, [float]$pH)

    $meshCols = 140
    $meshRows = 120
    $cellW = [float]($pW / $meshCols)
    $cellH = [float]($pH / $meshRows)

    $elev = New-Object 'double[,]' ($meshCols + 1), ($meshRows + 1)

    for ($ix = 0; $ix -le $meshCols; $ix++) {
        for ($iy = 0; $iy -le $meshRows; $iy++) {
            $nx = ($ix / $meshCols) * 2.0 - 1.0
            $ny = ($iy / $meshRows) * 2.0 - 1.0

            if ($type -eq 'Sicily') {
                $distEtna = [Math]::Sqrt(($nx - 0.28) * ($nx - 0.28) + ($ny - 0.12) * ($ny - 0.12))
                $hEtna = [Math]::Max(0.0, (1.0 - $distEtna * 3.2)) * 3350.0
                $hRidge = [Math]::Max(0.0, [Math]::Sin($nx * 4.0 + 1.2) * [Math]::Cos($ny * 3.5)) * 1400.0

                $islandDist = [Math]::Sqrt($nx * $nx * 0.8 + $ny * $ny * 1.4)
                if ($islandDist -gt 0.88 -and $nx -lt 0.5) {
                    $elev[$ix, $iy] = -100.0
                } else {
                    $elev[$ix, $iy] = $hEtna + $hRidge + 150.0
                }
            } else {
                $distCenter = [Math]::Sqrt($nx * $nx + $ny * $ny)
                $rimH = 0.0
                if ($distCenter -ge 0.48 -and $distCenter -le 0.78) {
                    $rimH = [Math]::Sin(($distCenter - 0.48) / 0.3 * [Math]::PI) * 980.0
                } elseif ($distCenter -lt 0.48) {
                    $rimH = 480.0
                } else {
                    $rimH = [Math]::Max(0.0, (1.1 - $distCenter)) * 600.0
                }

                $distPeaks = [Math]::Sqrt(($nx - 0.02) * ($nx - 0.02) + ($ny - 0.02) * ($ny - 0.02))
                $hPeaks = [Math]::Max(0.0, (1.0 - $distPeaks * 5.0)) * 1150.0

                $elev[$ix, $iy] = $rimH + $hPeaks + 200.0
            }
        }
    }

    $lx = -0.7071
    $ly = -0.7071
    $lz = 1.0

    for ($ix = 0; $ix -lt $meshCols; $ix += 2) {
        for ($iy = 0; $iy -lt $meshRows; $iy += 2) {
            $h = $elev[$ix, $iy]
            $px = [float]($pX + ($ix * $cellW))
            $py = [float]($pY + ($iy * $cellH))
            $pwC = [float]($cellW * 2.1)
            $phC = [float]($cellH * 2.1)

            if ($h -lt 0.0) {
                $seaBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 14, 22, 34))
                $g.FillRectangle($seaBrush, $px, $py, $pwC, $phC)
                $seaBrush.Dispose()
                continue
            }

            $dzdx = ($elev[$ix + 1, $iy] - $elev[[Math]::Max(0, $ix - 1), $iy]) / ($cellW * 2.0)
            $dzdy = ($elev[$ix, $iy + 1] - $elev[$ix, [Math]::Max(0, $iy - 1)]) / ($cellH * 2.0)

            $shade = ($lx * (-$dzdx * 0.08) + $ly * (-$dzdy * 0.08) + $lz) / [Math]::Sqrt($dzdx * $dzdx * 0.0064 + $dzdy * $dzdy * 0.0064 + 1.0)
            $shade = [Math]::Max(0.4, [Math]::Min(1.6, $shade))

            $baseR = 25; $baseG = 38; $baseB = 52
            if ($h -gt 2500.0) {
                $baseR = 90; $baseG = 35; $baseB = 25
            } elseif ($h -gt 1200.0) {
                $baseR = 65; $baseG = 45; $baseB = 38
            } elseif ($h -gt 600.0) {
                $baseR = 38; $baseG = 52; $baseB = 55
            }

            $r = [Math]::Min(255, [int]($baseR * $shade))
            $gC = [Math]::Min(255, [int]($baseG * $shade))
            $b = [Math]::Min(255, [int]($baseB * $shade))

            $cellBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, $r, $gC, $b))
            $g.FillRectangle($cellBrush, $px, $py, $pwC, $phC)
            $cellBrush.Dispose()
        }
    }
}

# =========================================================================
# DRAW PANEL A: SICILY / ETNA
# =========================================================================
$p1X = 40; $p1Y = 150; $p1W = 1130; $p1H = 1020
Draw-DemPanel $p1X $p1Y $p1W $p1H 'Sicily'

# Panel A Header
$subHeadBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 24, 35, 54))
$g.FillRectangle($subHeadBrush, [float]($p1X + 20), [float]($p1Y + 20), [float]($p1W - 40), [float]52)
$g.DrawRectangle($bannerPen, [float]($p1X + 20), [float]($p1Y + 20), [float]($p1W - 40), [float]52)
$g.DrawString('【PANEL A】一次野生生息地：南欧地中海・シチリア島エトナ山', $headerFont, $orangeBrush, [float]($p1X + 35), [float]($p1Y + 32))
$g.DrawString('LAT 36°30''-38°30''N / COPERNICUS DEM 30m', $subFont, $orangeBrush, [float]($p1X + 760), [float]($p1Y + 36))

# Mount Etna Hotspot
$etnaX = [float]($p1X + 720); $etnaY = [float]($p1Y + 560)
$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(180, 255, 34, 0))), [float]($etnaX - 85), [float]($etnaY - 85), [float]170, [float]170)
$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 255, 102, 0))), [float]($etnaX - 50), [float]($etnaY - 50), [float]100, [float]100)
$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)), [float]($etnaX - 10), [float]($etnaY - 10), [float]20, [float]20)
$g.DrawEllipse((New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 68, 0), 3)), [float]($etnaX - 85), [float]($etnaY - 85), [float]170, [float]170)

# Labels
$g.DrawString('エトナ山 (Mount Etna 3,357m)', $labelFont, $orangeBrush, [float]($etnaX - 130), [float]($etnaY - 120))
$g.DrawString('パレルモ (Palermo)', $labelFont, $whiteBrush, [float]($p1X + 280), [float]($p1Y + 380))
$g.DrawString('メッシーナ海峡 (Strait of Messina)', $labelFont, $cyanBrush, [float]($p1X + 810), [float]($p1Y + 340))
$g.DrawString('カターニャ (Catania)', $labelFont, $orangeBrush, [float]($p1X + 760), [float]($p1Y + 680))
$g.DrawString('シラクーザ (Siracusa)', $labelFont, $whiteBrush, [float]($p1X + 780), [float]($p1Y + 840))

# Callout Box A
$callPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 102, 34), 2)
$callBg = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(240, 16, 10, 8))
$g.DrawLine($callPen, $etnaX, $etnaY, [float]($etnaX + 160), [float]($etnaY - 160))
$g.FillRectangle($callBg, [float]($etnaX + 160), [float]($etnaY - 240), [float]360, [float]150)
$g.DrawRectangle($callPen, [float]($etnaX + 160), [float]($etnaY - 240), [float]360, [float]150)
$g.DrawString('エトナ第2火口原溶岩湖', $headerFont, $orangeBrush, [float]($etnaX + 175), [float]($etnaY - 230))
$g.DrawString('- 水深 0〜15m / 溶岩温度 1,100℃', $subFont, $whiteBrush, [float]($etnaX + 175), [float]($etnaY - 195))
$g.DrawString('- 古生主級 (Elder Alpha SM +3 生息)', $subFont, $pinkBrush, [float]($etnaX + 175), [float]($etnaY - 168))
$g.DrawString('- 火霊マナ濃度: 240 mU/m3', $subFont, $orangeBrush, [float]($etnaX + 175), [float]($etnaY - 141))
$g.DrawString('※NATO第9アルピーニ魔導特科監視下', $smallFont, $grayBrush, [float]($etnaX + 175), [float]($etnaY - 115))

# =========================================================================
# DRAW PANEL B: KYUSHU / ASO CALDERA
# =========================================================================
$p2X = 1230; $p2Y = 150; $p2W = 1130; $p2H = 1020
Draw-DemPanel $p2X $p2Y $p2W $p2H 'Aso'

# Panel B Header
$g.FillRectangle($subHeadBrush, [float]($p2X + 20), [float]($p2Y + 20), [float]($p2W - 40), [float]52)
$g.DrawRectangle($bannerPen, [float]($p2X + 20), [float]($p2Y + 20), [float]($p2W - 40), [float]52)
$g.DrawString('【PANEL B】国内定着コロニー：九州阿蘇カルデラ・桜島（外来定着）', $headerFont, $pinkBrush, [float]($p2X + 35), [float]($p2Y + 32))
$g.DrawString('LAT 32°40''-33°10''N / 国土地理院 DEM 10m', $subFont, $pinkBrush, [float]($p2X + 750), [float]($p2Y + 36))

# Aso Hotspot
$asoX = [float]($p2X + 565); $asoY = [float]($p2Y + 505)
$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(180, 255, 0, 85))), [float]($asoX - 80), [float]($asoY - 80), [float]160, [float]160)
$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(220, 255, 68, 0))), [float]($asoX - 45), [float]($asoY - 45), [float]90, [float]90)
$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)), [float]($asoX - 10), [float]($asoY - 10), [float]20, [float]20)
$g.DrawEllipse((New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 0, 85), 3)), [float]($asoX - 80), [float]($asoY - 80), [float]160, [float]160)

# Labels
$g.DrawString('阿蘇外輪山断崖 (Outer Rim / 東西18km 南北25km)', $labelFont, $cyanBrush, [float]($p2X + 340), [float]($p2Y + 160))
$g.DrawString('中岳第1火口 (1,506m)', $headerFont, $pinkBrush, [float]($asoX - 120), [float]($asoY - 115))
$g.DrawString('高岳 (1,592m)', $labelFont, $whiteBrush, [float]($asoX + 90), [float]($asoY - 40))
$g.DrawString('草千里ヶ浜', $labelFont, $whiteBrush, [float]($asoX - 180), [float]($asoY + 20))
$g.DrawString('熊本市・熊本平野 (Kumamoto)', $headerFont, $whiteBrush, [float]($p2X + 90), [float]($p2Y + 540))
$g.DrawString('阿蘇市街・内牧', $labelFont, $whiteBrush, [float]($p2X + 440), [float]($p2Y + 300))

# Defense Wall
$wallPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 0, 220, 255), 4)
$wallPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$g.DrawArc($wallPen, [float]($p2X + 220), [float]($p2Y + 340), [float]260, [float]380, [float]120, [float]140)
$g.DrawString('超低温液体窒素バリケード (都市防衛線)', $subFont, $cyanBrush, [float]($p2X + 110), [float]($p2Y + 440))

# Callout Box B
$callPenB = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 0, 85), 2)
$callBgB = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(240, 20, 8, 12))
$g.DrawLine($callPenB, $asoX, $asoY, [float]($asoX + 180), [float]($asoY + 160))
$g.FillRectangle($callBgB, [float]($asoX + 140), [float]($asoY + 160), [float]390, [float]165)
$g.DrawRectangle($callPenB, [float]($asoX + 140), [float]($asoY + 160), [float]390, [float]165)
$g.DrawString('阿蘇中岳第1火口原〜地熱プラント', $headerFont, $pinkBrush, [float]($asoX + 155), [float]($asoY + 172))
$g.DrawString('- 定着繁殖コロニー (確認数: 12〜18体)', $subFont, $whiteBrush, [float]($asoX + 155), [float]($asoY + 208))
$g.DrawString('- 地熱パイプライン熱源侵入多発', $subFont, $orangeBrush, [float]($asoX + 155), [float]($asoY + 235))
$g.DrawString('- 九州防衛局 / 駆除重火器PMC常駐', $subFont, $cyanBrush, [float]($asoX + 155), [float]($asoY + 262))
$g.DrawString('※ヤマト重工・テイコク製薬特許素材採取区', $smallFont, $grayBrush, [float]($asoX + 155), [float]($asoY + 290))

# =========================================================================
# BOTTOM GLOBAL LEGEND
# =========================================================================
$legY = 1195; $legH = 130
$g.FillRectangle($bannerBrush, [float]40, [float]$legY, [float]2320, [float]$legH)
$g.DrawRectangle($bannerPen, [float]40, [float]$legY, [float]2320, [float]$legH)

$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 34, 0))), [float]80, [float]($legY + 25), [float]22, [float]22)
$g.DrawString('一次野生生息地（地中海・エトナ山 1,100℃玄武岩溶岩湖 / Elder Alpha 生息）', $labelFont, $whiteBrush, [float]115, [float]($legY + 24))

$g.FillEllipse((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 0, 85))), [float]80, [float]($legY + 75), [float]22, [float]22)
$g.DrawString('国内定着繁殖コロニー（阿蘇カルデラ・桜島 / 特定外来危険魔獣指定）', $labelFont, $whiteBrush, [float]115, [float]($legY + 74))

$g.DrawLine($wallPen, [float]980, [float]($legY + 36), [float]1040, [float]($legY + 36))
$g.DrawString('超低温液体窒素バリケード（都市防衛境界）', $labelFont, $cyanBrush, [float]1055, [float]($legY + 24))

$g.DrawString('DATA SOURCES: 国土地理院 基盤地図情報 (DEM10B) / NASA SRTM 30m / COPERNICUS DEM / OPENSTREETMAP', $subFont, $grayBrush, [float]980, [float]($legY + 74))

# Save PNG
$outPath = "$PSScriptRoot\..\..\assets\creatures\004_magma_salamander\004_magma_salamander_range_map.png"
$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)

$g.Dispose()
$bmp.Dispose()

Write-Host "SUCCESS: Generated $outPath" -ForegroundColor Green
