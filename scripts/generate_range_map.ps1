# scripts/generate_range_map.ps1
# Pure ASCII PowerShell script to generate and overlay range maps on base world maps

Add-Type -AssemblyName System.Drawing

function Generate-CreatureRangeMap {
    param(
        [string]$outputPath,
        [string]$titleJa,
        [string]$titleEn,
        [string]$primaryRegion,
        [array]$points,
        [array]$polygons
    )

    $width = 1000
    $height = 500

    $bitmap = New-Object System.Drawing.Bitmap $width, $height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

    # Background Ocean
    $oceanBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(20, 26, 38))
    $graphics.FillRectangle($oceanBrush, 0, 0, $width, $height)

    # Grid Lines
    $gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(28, 36, 54)), 1
    for ($x = 0; $x -lt $width; $x += 40) { $graphics.DrawLine($gridPen, $x, 0, $x, $height) }
    for ($y = 0; $y -lt $height; $y += 40) { $graphics.DrawLine($gridPen, 0, $y, $width, $y) }

    # Equator & Prime Meridian
    $guidePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(40, 52, 75)), 1
    $guidePen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
    $graphics.DrawLine($guidePen, 0, 250, $width, 250)
    $graphics.DrawLine($guidePen, 500, 0, 500, $height)

    # Landmass
    $landBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(40, 51, 71))
    $landPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(62, 77, 107)), 1.2

    # North America
    $pNA = [System.Drawing.PointF[]]@(
        (New-Object System.Drawing.PointF 60, 70),
        (New-Object System.Drawing.PointF 160, 55),
        (New-Object System.Drawing.PointF 225, 90),
        (New-Object System.Drawing.PointF 210, 120),
        (New-Object System.Drawing.PointF 175, 125),
        (New-Object System.Drawing.PointF 210, 200),
        (New-Object System.Drawing.PointF 180, 230),
        (New-Object System.Drawing.PointF 145, 200),
        (New-Object System.Drawing.PointF 80, 140),
        (New-Object System.Drawing.PointF 50, 110)
    )
    $graphics.FillPolygon($landBrush, $pNA)
    $graphics.DrawPolygon($landPen, $pNA)

    # South America
    $pSA = [System.Drawing.PointF[]]@(
        (New-Object System.Drawing.PointF 165, 240),
        (New-Object System.Drawing.PointF 230, 270),
        (New-Object System.Drawing.PointF 255, 310),
        (New-Object System.Drawing.PointF 230, 370),
        (New-Object System.Drawing.PointF 185, 450),
        (New-Object System.Drawing.PointF 165, 380),
        (New-Object System.Drawing.PointF 145, 250)
    )
    $graphics.FillPolygon($landBrush, $pSA)
    $graphics.DrawPolygon($landPen, $pSA)

    # Eurasia
    $pEA = [System.Drawing.PointF[]]@(
        (New-Object System.Drawing.PointF 460, 70),
        (New-Object System.Drawing.PointF 700, 55),
        (New-Object System.Drawing.PointF 890, 95),
        (New-Object System.Drawing.PointF 860, 140),
        (New-Object System.Drawing.PointF 880, 170),
        (New-Object System.Drawing.PointF 830, 200),
        (New-Object System.Drawing.PointF 810, 260),
        (New-Object System.Drawing.PointF 760, 270),
        (New-Object System.Drawing.PointF 690, 240),
        (New-Object System.Drawing.PointF 620, 220),
        (New-Object System.Drawing.PointF 540, 180),
        (New-Object System.Drawing.PointF 460, 120),
        (New-Object System.Drawing.PointF 440, 90)
    )
    $graphics.FillPolygon($landBrush, $pEA)
    $graphics.DrawPolygon($landPen, $pEA)

    # Africa
    $pAF = [System.Drawing.PointF[]]@(
        (New-Object System.Drawing.PointF 465, 175),
        (New-Object System.Drawing.PointF 575, 200),
        (New-Object System.Drawing.PointF 590, 310),
        (New-Object System.Drawing.PointF 520, 420),
        (New-Object System.Drawing.PointF 460, 300),
        (New-Object System.Drawing.PointF 445, 200)
    )
    $graphics.FillPolygon($landBrush, $pAF)
    $graphics.DrawPolygon($landPen, $pAF)

    # Japan Archipelago (Highlighted)
    $jpBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(58, 72, 99))
    $jpPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(99, 179, 237)), 2
    $pJP = [System.Drawing.PointF[]]@(
        (New-Object System.Drawing.PointF 830, 140),
        (New-Object System.Drawing.PointF 870, 145),
        (New-Object System.Drawing.PointF 850, 175),
        (New-Object System.Drawing.PointF 820, 160)
    )
    $graphics.FillPolygon($jpBrush, $pJP)
    $graphics.DrawPolygon($jpPen, $pJP)

    # Australia
    $pAU = [System.Drawing.PointF[]]@(
        (New-Object System.Drawing.PointF 780, 320),
        (New-Object System.Drawing.PointF 885, 345),
        (New-Object System.Drawing.PointF 840, 420),
        (New-Object System.Drawing.PointF 760, 360)
    )
    $graphics.FillPolygon($landBrush, $pAU)
    $graphics.DrawPolygon($landPen, $pAU)

    # Ocean Text
    $fontSea = New-Object System.Drawing.Font ("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
    $seaBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(35, 45, 63))
    $graphics.DrawString("PACIFIC OCEAN", $fontSea, $seaBrush, 350, 230)

    # Polygons (Habitat Range)
    if ($polygons) {
        $polyBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(70, 236, 201, 75))
        $polyPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(200, 236, 201, 75)), 1.5
        $polyPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
        foreach ($poly in $polygons) {
            $pArr = [System.Drawing.PointF[]]$poly
            $graphics.FillPolygon($polyBrush, $pArr)
            $graphics.DrawPolygon($polyPen, $pArr)
        }
    }

    # Points & Pins
    if ($points) {
        foreach ($pt in $points) {
            $px = [float]$pt.X
            $py = [float]$pt.Y
            $label = [string]$pt.Label
            $isPrimary = [bool]$pt.IsPrimary

            $color = if ($isPrimary) { [System.Drawing.Color]::FromArgb(229, 62, 62) } else { [System.Drawing.Color]::FromArgb(236, 201, 75) }
            $glowBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(50, $color.R, $color.G, $color.B))
            $pinBrush = New-Object System.Drawing.SolidBrush ($color)
            $whitePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::White), 1.5

            $graphics.FillEllipse($glowBrush, ($px - 14), ($py - 14), 28, 28)
            $graphics.FillEllipse($pinBrush, ($px - 6), ($py - 6), 12, 12)
            $graphics.DrawEllipse($whitePen, ($px - 6), ($py - 6), 12, 12)

            # Label Box
            $fontLabel = New-Object System.Drawing.Font ("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
            $labelBoxBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(220, 26, 34, 51))
            $labelBorderPen = New-Object System.Drawing.Pen ($color), 1
            $textBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(247, 250, 252))

            $size = $graphics.MeasureString($label, $fontLabel)
            $bx = $px + 12
            $by = $py - 8
            $graphics.FillRectangle($labelBoxBrush, $bx, $by, ($size.Width + 8), ($size.Height + 4))
            $graphics.DrawRectangle($labelBorderPen, $bx, $by, ($size.Width + 8), ($size.Height + 4))
            $graphics.DrawString($label, $fontLabel, $textBrush, ($bx + 4), ($by + 2))
        }
    }

    # Header Box
    $hdrBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(220, 26, 34, 51))
    $hdrPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(45, 55, 72)), 1
    $graphics.FillRectangle($hdrBrush, 15, 15, 970, 46)
    $graphics.DrawRectangle($hdrPen, 15, 15, 970, 46)

    $fontTitle = New-Object System.Drawing.Font ("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
    $fontSub = New-Object System.Drawing.Font ("Segoe UI", 9)
    $textWhite = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(247, 250, 252))
    $textGray = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(160, 174, 192))

    $graphics.DrawString("HABITAT RANGE MAP: $titleJa ($titleEn)", $fontTitle, $textWhite, 25, 20)
    $graphics.DrawString("PRIMARY HABITAT & CONCENTRIC DEFENSE LINE | $primaryRegion", $fontSub, $textGray, 25, 42)

    # Legend Box
    $legBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(220, 26, 34, 51))
    $graphics.FillRectangle($legBrush, 25, 385, 300, 95)
    $graphics.DrawRectangle($hdrPen, 25, 385, 300, 95)

    $fontLeg = New-Object System.Drawing.Font ("Segoe UI", 8.5)
    $graphics.DrawString("LEGEND", (New-Object System.Drawing.Font ("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)), $textWhite, 35, 395)

    $redBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(229, 62, 62))
    $graphics.FillEllipse($redBrush, 38, 420, 10, 10)
    $graphics.DrawString("Primary Habitat (Abyss Singularity)", $fontLeg, $textGray, 55, 418)

    $goldBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(236, 201, 75))
    $graphics.FillEllipse($goldBrush, 38, 442, 10, 10)
    $graphics.DrawString("Migration / Outland Bloom Area", $fontLeg, $textGray, 55, 440)

    $dashPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(66, 153, 225)), 2
    $dashPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
    $graphics.DrawLine($dashPen, 35, 468, 50, 468)
    $graphics.DrawString("Concentric Defense Network Boundary", $fontLeg, $textGray, 55, 462)

    # Save PNG
    $dir = Split-Path -Path $outputPath
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }
    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

    $graphics.Dispose()
    $bitmap.Dispose()
    Write-Host "Range map successfully generated: $outputPath"
}

# 1. Output Base World Map
$basePath = "assets/templates/base_map_world.png"
Generate-CreatureRangeMap -outputPath $basePath -titleJa "Base World Map" -titleEn "Template" -primaryRegion "Global" -points @() -polygons @()

# 2. Output Astral Nebula Jelly Range Map
$jellyPath = "assets/creatures/008_astral_nebula_jelly/astral_jelly_range_map.png"
$pts008 = @(
    @{ X = 875; Y = 255; Label = "Mariana Trench Abyss (1,000-3,000m)"; IsPrimary = $true },
    @{ X = 850; Y = 160; Label = "Tokyo Bay Uraga Strait"; IsPrimary = $false }
)
$poly008 = @(
    @(
        (New-Object System.Drawing.PointF 850, 160),
        (New-Object System.Drawing.PointF 875, 255),
        (New-Object System.Drawing.PointF 960, 270),
        (New-Object System.Drawing.PointF 920, 190)
    )
)
Generate-CreatureRangeMap -outputPath $jellyPath -titleJa "Astral Nebula Jelly" -titleEn "Aurelia astralis" -primaryRegion "Pacific Abyss to Tokyo Bay" -points $pts008 -polygons $poly008
