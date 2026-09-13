# scripts/generate_south_america_map.ps1
# Natural Earth 50m高精細データから南米大陸・アンデス山脈のリージョナル生息マップを生成

Add-Type -AssemblyName System.Drawing

$json = Get-Content 'assets/templates/ne_50m_countries.json' -Raw | ConvertFrom-Json

$width = 960
$height = 850
$lonMin = -85.0
$lonMax = -34.0
$latMax = 14.0
$latMin = -56.0

function Project-Point($lon, $lat) {
    $px = [Math]::Round((($lon - $lonMin) / ($lonMax - $lonMin)) * ($width - 60) + 30, 1)
    $py = [Math]::Round((($latMax - $lat) / ($latMax - $latMin)) * ($height - 60) + 30, 1)
    return @{ X = $px; Y = $py }
}

function Convert-RingToPath($ring) {
    $sb = New-Object System.Text.StringBuilder
    $first = $true
    foreach ($pt in $ring) {
        $lon = [double]$pt[0]
        $lat = [double]$pt[1]
        $p = Project-Point $lon $lat
        if ($first) {
            [void]$sb.Append(('M {0},{1}' -f $p.X, $p.Y))
            $first = $false
        } else {
            [void]$sb.Append((' L {0},{1}' -f $p.X, $p.Y))
        }
    }
    [void]$sb.Append(' Z')
    return $sb.ToString()
}

$saCountries = @('Peru', 'Ecuador', 'Colombia', 'Bolivia', 'Chile', 'Argentina', 'Brazil', 'Venezuela', 'Paraguay', 'Uruguay', 'Guyana', 'Suriname')

$allLandPaths = New-Object System.Text.StringBuilder
$countryPolys = @()

foreach ($feat in $json.features) {
    $name = $feat.properties.NAME
    if (-not $name) { $name = $feat.properties.ADMIN }
    if ($saCountries -contains $name) {
        if ($feat.geometry.type -eq 'Polygon') {
            foreach ($ring in $feat.geometry.coordinates) {
                $path = Convert-RingToPath $ring
                [void]$allLandPaths.Append($path + ' ')
                $countryPolys += ,$ring
            }
        } elseif ($feat.geometry.type -eq 'MultiPolygon') {
            foreach ($poly in $feat.geometry.coordinates) {
                foreach ($ring in $poly) {
                    $path = Convert-RingToPath $ring
                    [void]$allLandPaths.Append($path + ' ')
                    $countryPolys += ,$ring
                }
            }
        }
    }
}

# Andes Mountain Range Topographic Cloud Forest Polygon (Elevation 2,500 - 3,500m)
$andesCoords = @(
    @(-78.5, 1.0),
    @(-77.0, -0.5),
    @(-76.5, -3.0),
    @(-75.5, -6.5),
    @(-73.5, -11.0),
    @(-70.5, -14.5),
    @(-67.0, -17.5),
    @(-65.5, -19.0),
    @(-66.5, -21.0),
    @(-68.5, -20.0),
    @(-70.0, -17.0),
    @(-72.5, -15.5),
    @(-75.5, -14.0),
    @(-78.0, -8.5),
    @(-79.5, -5.0),
    @(-80.0, -2.5),
    @(-79.5, 0.0)
)
$andesPath = Convert-RingToPath $andesCoords

# Hotspot Locations
$pQuito = Project-Point -78.5 -0.2
$pCusco = Project-Point -71.9 -13.5
$pYungas = Project-Point -67.5 -16.2
$pCaves = Project-Point -75.0 -10.0

# 1. Build High-Precision SVG
$sbSvg = New-Object System.Text.StringBuilder
[void]$sbSvg.AppendLine('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 850" width="100%" height="100%">')
[void]$sbSvg.AppendLine('  <defs>')
[void]$sbSvg.AppendLine('    <linearGradient id="oceanGradSa" x1="0%" y1="0%" x2="0%" y2="100%">')
[void]$sbSvg.AppendLine('      <stop offset="0%" stop-color="#0b1329" />')
[void]$sbSvg.AppendLine('      <stop offset="100%" stop-color="#020617" />')
[void]$sbSvg.AppendLine('    </linearGradient>')
[void]$sbSvg.AppendLine('    <linearGradient id="andesCorridorGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
[void]$sbSvg.AppendLine('      <stop offset="0%" stop-color="#e11d48" stop-opacity="0.8" />')
[void]$sbSvg.AppendLine('      <stop offset="100%" stop-color="#be123c" stop-opacity="0.45" />')
[void]$sbSvg.AppendLine('    </linearGradient>')
[void]$sbSvg.AppendLine('    <filter id="glowPink" x="-20%" y="-20%" width="140%" height="140%">')
[void]$sbSvg.AppendLine('      <feGaussianBlur stdDeviation="4" result="blur" />')
[void]$sbSvg.AppendLine('      <feComposite in="SourceGraphic" in2="blur" operator="over" />')
[void]$sbSvg.AppendLine('    </filter>')
[void]$sbSvg.AppendLine('  </defs>')

[void]$sbSvg.AppendLine('  <!-- Ocean Background -->')
[void]$sbSvg.AppendLine('  <rect width="960" height="850" fill="url(#oceanGradSa)" />')

[void]$sbSvg.AppendLine('  <!-- Graticule (Lat/Lon Coordinates: 80W - 40W / 10N - 50S) -->')
[void]$sbSvg.AppendLine('  <g stroke="#1e293b" stroke-width="0.6" stroke-dasharray="3,3">')

for ($lon = -80; $lon -le -40; $lon += 10) {
    $p1 = Project-Point $lon 14
    $p2 = Project-Point $lon -56
    [void]$sbSvg.AppendLine(('    <line x1="{0}" y1="{1}" x2="{2}" y2="{3}" />' -f $p1.X, $p1.Y, $p2.X, $p2.Y))
}
for ($lat = 10; $lat -ge -50; $lat -= 10) {
    $p1 = Project-Point -85 $lat
    $p2 = Project-Point -34 $lat
    $sw = if ($lat -eq 0) { 'stroke="#334155" stroke-width="1.2"' } else { 'stroke="#1e293b" stroke-width="0.6"' }
    [void]$sbSvg.AppendLine(('    <line x1="{0}" y1="{1}" x2="{2}" y2="{3}" {4} />' -f $p1.X, $p1.Y, $p2.X, $p2.Y, $sw))
}
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Coordinate Text Labels -->')
[void]$sbSvg.AppendLine('  <g fill="#64748b" font-size="9" font-family="monospace">')
for ($lon = -80; $lon -le -40; $lon += 10) {
    $p = Project-Point $lon -55
    [void]$sbSvg.AppendLine(('    <text x="{0}" y="{1}">{2}&#176;W</text>' -f ($p.X - 10), ($height - 15), [Math]::Abs($lon)))
}
for ($lat = 10; $lat -ge -50; $lat -= 10) {
    $p = Project-Point -84 $lat
    $label = if ($lat -eq 0) { '0&#176; (EQUATOR)' } elseif ($lat -gt 0) { ('{0}&#176;N' -f $lat) } else { ('{0}&#176;S' -f [Math]::Abs($lat)) }
    $fill = if ($lat -eq 0) { 'fill="#94a3b8" font-weight="bold"' } else { 'fill="#64748b"' }
    [void]$sbSvg.AppendLine(('    <text x="12" y="{0}" {1}>{2}</text>' -f ($p.Y + 3), $fill, $label))
}
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Natural Earth 50m High-Precision Continental Landmass -->')
[void]$sbSvg.AppendLine('  <g id="south-america-landmass">')
[void]$sbSvg.AppendLine(('    <path d="{0}" fill="#1e293b" stroke="#475569" stroke-width="1.2" stroke-linejoin="round" />' -f $allLandPaths.ToString()))
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Amazon Basin Biome Ambient Area -->')
[void]$sbSvg.AppendLine('  <path d="M 320,200 Q 520,180 660,250 Q 720,340 640,430 Q 500,470 380,410 Q 300,320 320,200 Z" fill="#0f291e" fill-opacity="0.45" stroke="#164e3f" stroke-width="1" stroke-dasharray="3,3" />')
[void]$sbSvg.AppendLine('  <text x="490" y="320" fill="#2dd4bf" font-size="13" font-family="sans-serif" font-weight="bold" opacity="0.35" letter-spacing="4">AMAZON RAINFOREST BASIN</text>')

[void]$sbSvg.AppendLine('  <!-- Andes Mountain Range Continental Spine Line -->')
[void]$sbSvg.AppendLine('  <path d="M 235,110 L 255,165 L 235,215 L 245,255 L 285,320 L 320,400 L 340,490 L 355,570 L 375,670 L 400,750 L 430,810" fill="none" stroke="#64748b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.4" />')
[void]$sbSvg.AppendLine('  <path d="M 235,110 L 255,165 L 235,215 L 245,255 L 285,320 L 320,400 L 340,490 L 355,570 L 375,670 L 400,750 L 430,810" fill="none" stroke="#cbd5e1" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0.75" />')

[void]$sbSvg.AppendLine('  <!-- Primary Habitat: Andes Cloud Forest Singularity Corridor -->')
[void]$sbSvg.AppendLine('  <g id="andes-cloud-forest-corridor">')
[void]$sbSvg.AppendLine(('    <path d="{0}" fill="url(#andesCorridorGrad)" stroke="#f43f5e" stroke-width="2" filter="url(#glowPink)" />' -f $andesPath))
[void]$sbSvg.AppendLine('  </g>')

# Hotspots
[void]$sbSvg.AppendLine('  <!-- Hotspot 1: Quito -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pQuito.X, $pQuito.Y))
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="12" fill="#f43f5e" fill-opacity="0.3" />')
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="5" fill="#ef4444" stroke="#ffffff" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <line x1="0" y1="0" x2="-60" y2="-20" stroke="#f43f5e" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <rect x="-215" y="-34" width="150" height="24" rx="3" fill="#020617" fill-opacity="0.9" stroke="#f43f5e" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <text x="-205" y="-18" fill="#fda4af" font-size="9.5" font-family="sans-serif" font-weight="bold">&#9312; Quito Cloud Forest (Ecuador)</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Hotspot 2: Cusco -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pCusco.X, $pCusco.Y))
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="16" fill="#f43f5e" fill-opacity="0.4" filter="url(#glowPink)" />')
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="7" fill="#e11d48" stroke="#ffffff" stroke-width="2" />')
[void]$sbSvg.AppendLine('    <line x1="0" y1="0" x2="60" y2="-25" stroke="#f43f5e" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <rect x="65" y="-40" width="220" height="30" rx="4" fill="#020617" fill-opacity="0.95" stroke="#f43f5e" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <text x="75" y="-20" fill="#ffe4e6" font-size="11" font-family="sans-serif" font-weight="bold">&#9733; Cusco-Urubamba Singularity Core</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Hotspot 3: Yungas -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pYungas.X, $pYungas.Y))
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="11" fill="#f43f5e" fill-opacity="0.3" />')
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="5" fill="#ef4444" stroke="#ffffff" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <line x1="0" y1="0" x2="50" y2="25" stroke="#f43f5e" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <rect x="55" y="14" width="165" height="24" rx="3" fill="#020617" fill-opacity="0.9" stroke="#f43f5e" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <text x="63" y="30" fill="#fda4af" font-size="9.5" font-family="sans-serif" font-weight="bold">&#9313; Yungas Mist Corridor (Bolivia)</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Hotspot 4: Crystal Caves -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pCaves.X, $pCaves.Y))
[void]$sbSvg.AppendLine('    <polygon points="0,-7 7,0 0,7 -7,0" fill="#38bdf8" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <rect x="-175" y="-12" width="160" height="22" rx="3" fill="#020617" fill-opacity="0.85" stroke="#38bdf8" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <text x="-168" y="3" fill="#bae6fd" font-size="8.5" font-family="sans-serif" font-weight="bold">&#9314; Subterranean Crystal Caves</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Ocean Labels -->')
[void]$sbSvg.AppendLine('  <text x="60" y="440" fill="#334155" font-size="16" font-family="sans-serif" font-weight="bold" letter-spacing="4">PACIFIC OCEAN</text>')
[void]$sbSvg.AppendLine('  <text x="700" y="580" fill="#334155" font-size="16" font-family="sans-serif" font-weight="bold" letter-spacing="4">ATLANTIC OCEAN</text>')

[void]$sbSvg.AppendLine('  <!-- Map Header Box -->')
[void]$sbSvg.AppendLine('  <g transform="translate(25, 25)">')
[void]$sbSvg.AppendLine('    <rect width="440" height="56" rx="4" fill="#020617" fill-opacity="0.92" stroke="#334155" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="16" y="24" fill="#f8fafc" font-size="13" font-family="sans-serif" font-weight="bold">HABITAT RANGE MAP: ANDES CLOUD FOREST (南米アンデス雲霧林)</text>')
[void]$sbSvg.AppendLine('    <text x="16" y="44" fill="#94a3b8" font-size="9.5" font-family="sans-serif">Natural Earth 50m High-Precision Data / Elevation: 2,500m - 3,500m</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Inset Map: Secondary Sanctuaries -->')
[void]$sbSvg.AppendLine('  <g transform="translate(620, 25)">')
[void]$sbSvg.AppendLine('    <rect width="315" height="150" rx="4" fill="#020617" fill-opacity="0.95" stroke="#475569" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <rect x="0" y="0" width="315" height="22" rx="3" fill="#1e293b" />')
[void]$sbSvg.AppendLine('    <text x="12" y="15" fill="#e2e8f0" font-size="9.5" font-family="sans-serif" font-weight="bold">SECONDARY PROTECTED COLONIES (国外・国内保護区)</text>')
[void]$sbSvg.AppendLine('    <circle cx="35" cy="50" r="5" fill="#facc15" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="50" y="48" fill="#fef08a" font-size="10" font-family="sans-serif" font-weight="bold">Tokyo Hachioji Mt. Takao Mana Reserve</text>')
[void]$sbSvg.AppendLine('    <text x="50" y="62" fill="#94a3b8" font-size="8.5" font-family="sans-serif">東京都八王子第3バッファー / 8家族群（45頭）</text>')
[void]$sbSvg.AppendLine('    <circle cx="35" cy="92" r="5" fill="#38bdf8" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="50" y="90" fill="#bae6fd" font-size="10" font-family="sans-serif" font-weight="bold">European Alps Foothill Reserve (Swiss/Austria)</text>')
[void]$sbSvg.AppendLine('    <text x="50" y="104" fill="#94a3b8" font-size="8.5" font-family="sans-serif">アルプス山麓保護回廊 / 標高1,600m</text>')
[void]$sbSvg.AppendLine('    <rect x="15" y="120" width="285" height="20" rx="3" fill="#14532d" fill-opacity="0.6" stroke="#22c55e" stroke-width="0.8" />')
[void]$sbSvg.AppendLine('    <text x="25" y="134" fill="#86efac" font-size="8.5" font-family="sans-serif" font-weight="bold">CITES Appendix I / Class-A Strict Protection</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Legend Box -->')
[void]$sbSvg.AppendLine('  <g transform="translate(25, 690)">')
[void]$sbSvg.AppendLine('    <rect width="400" height="130" rx="4" fill="#020617" fill-opacity="0.92" stroke="#f43f5e" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="14" y="20" fill="#fb7185" font-size="11" font-family="sans-serif" font-weight="bold">凡例 (HABITAT &amp; CONSERVATION LEGEND)</text>')
[void]$sbSvg.AppendLine('    <circle cx="25" cy="42" r="7" fill="#e11d48" stroke="#ffffff" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <text x="42" y="46" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">一次野生生息地（アンデス雲霧林特異点コア 標高2,500-3,500m）</text>')
[void]$sbSvg.AppendLine('    <rect x="18" y="58" width="14" height="14" fill="#f43f5e" fill-opacity="0.3" stroke="#fb7185" stroke-dasharray="3,2" />')
[void]$sbSvg.AppendLine('    <text x="42" y="69" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">高山帯活動・季節回遊回廊（標高2,000-4,000m）</text>')
[void]$sbSvg.AppendLine('    <polygon points="25,90 30,96 25,102 20,96" fill="#38bdf8" stroke="#ffffff" />')
[void]$sbSvg.AppendLine('    <text x="42" y="99" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">地下水晶洞窟群（古代休眠・Al/Crミネラル鉱床）</text>')
[void]$sbSvg.AppendLine('    <line x1="18" y1="116" x2="32" y2="116" stroke="#cbd5e1" stroke-width="3" />')
[void]$sbSvg.AppendLine('    <text x="42" y="120" fill="#94a3b8" font-size="9.5" font-family="sans-serif">アンデス山脈主稜線 (Topographic Continental Mountain Spine)</text>')
[void]$sbSvg.AppendLine('  </g>')
[void]$sbSvg.AppendLine('</svg>')

Set-Content -Path 'assets/creatures/006_carbuncle/carbuncle_map.svg' -Value $sbSvg.ToString() -Encoding utf8
Write-Host 'High-Precision 50m Natural Earth SVG successfully generated: assets/creatures/006_carbuncle/carbuncle_map.svg'

# 2. Render High-Precision PNG via System.Drawing
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

# Ocean
$oceanBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(11, 19, 41))
$graphics.FillRectangle($oceanBrush, 0, 0, $width, $height)

# Grid
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(30, 41, 59)), 1
for ($lon = -80; $lon -le -40; $lon += 10) {
    $p1 = Project-Point $lon 14
    $p2 = Project-Point $lon -56
    $graphics.DrawLine($gridPen, [float]$p1.X, [float]$p1.Y, [float]$p2.X, [float]$p2.Y)
}
for ($lat = 10; $lat -ge -50; $lat -= 10) {
    $p1 = Project-Point -85 $lat
    $p2 = Project-Point -34 $lat
    $graphics.DrawLine($gridPen, [float]$p1.X, [float]$p1.Y, [float]$p2.X, [float]$p2.Y)
}

# Equator
$eqPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(51, 65, 85)), 1.5
$eqPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$pEq1 = Project-Point -85 0
$pEq2 = Project-Point -34 0
$graphics.DrawLine($eqPen, [float]$pEq1.X, [float]$pEq1.Y, [float]$pEq2.X, [float]$pEq2.Y)

# Landmass Polygons
$landBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(30, 41, 59))
$landPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(71, 85, 105)), 1.2

foreach ($ring in $countryPolys) {
    if ($ring.Count -ge 3) {
        $pts = @()
        foreach ($pt in $ring) {
            $p = Project-Point ([double]$pt[0]) ([double]$pt[1])
            $pts += (New-Object System.Drawing.PointF ([float]$p.X), ([float]$p.Y))
        }
        $pArr = [System.Drawing.PointF[]]$pts
        $graphics.FillPolygon($landBrush, $pArr)
        $graphics.DrawPolygon($landPen, $pArr)
    }
}

# Amazon Basin Area
$amazonBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(60, 15, 41, 30))
$amazonPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(100, 22, 78, 63)), 1
$amazonPen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
$pAmazon = [System.Drawing.PointF[]]@(
    (New-Object System.Drawing.PointF 320, 200),
    (New-Object System.Drawing.PointF 520, 180),
    (New-Object System.Drawing.PointF 660, 250),
    (New-Object System.Drawing.PointF 720, 340),
    (New-Object System.Drawing.PointF 640, 430),
    (New-Object System.Drawing.PointF 500, 470),
    (New-Object System.Drawing.PointF 380, 410),
    (New-Object System.Drawing.PointF 300, 320)
)
$graphics.FillPolygon($amazonBrush, $pAmazon)
$graphics.DrawPolygon($amazonPen, $pAmazon)

# Andes Spine Line
$spinePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(180, 203, 213, 225)), 2
$pSpine = [System.Drawing.PointF[]]@(
    (New-Object System.Drawing.PointF 235, 110),
    (New-Object System.Drawing.PointF 255, 165),
    (New-Object System.Drawing.PointF 235, 215),
    (New-Object System.Drawing.PointF 245, 255),
    (New-Object System.Drawing.PointF 285, 320),
    (New-Object System.Drawing.PointF 320, 400),
    (New-Object System.Drawing.PointF 340, 490),
    (New-Object System.Drawing.PointF 355, 570),
    (New-Object System.Drawing.PointF 375, 670),
    (New-Object System.Drawing.PointF 400, 750),
    (New-Object System.Drawing.PointF 430, 810)
)
$graphics.DrawLines($spinePen, $pSpine)

# Primary Habitat Corridor
$habBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(160, 225, 29, 72))
$habPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(244, 63, 94)), 2
$pHabPts = @()
foreach ($c in $andesCoords) {
    $p = Project-Point ([double]$c[0]) ([double]$c[1])
    $pHabPts += (New-Object System.Drawing.PointF ([float]$p.X), ([float]$p.Y))
}
$pHabArr = [System.Drawing.PointF[]]$pHabPts
$graphics.FillPolygon($habBrush, $pHabArr)
$graphics.DrawPolygon($habPen, $pHabArr)

# Hotspot Pins
$pinRed = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(225, 29, 72))
$glowRed = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(70, 244, 63, 94))
$whitePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::White), 1.5

# Cusco
$graphics.FillEllipse($glowRed, ([float]($pCusco.X - 16)), ([float]($pCusco.Y - 16)), 32, 32)
$graphics.FillEllipse($pinRed, ([float]($pCusco.X - 7)), ([float]($pCusco.Y - 7)), 14, 14)
$graphics.DrawEllipse($whitePen, ([float]($pCusco.X - 7)), ([float]($pCusco.Y - 7)), 14, 14)

# Quito
$graphics.FillEllipse($glowRed, ([float]($pQuito.X - 12)), ([float]($pQuito.Y - 12)), 24, 24)
$graphics.FillEllipse($pinRed, ([float]($pQuito.X - 5)), ([float]($pQuito.Y - 5)), 10, 10)
$graphics.DrawEllipse($whitePen, ([float]($pQuito.X - 5)), ([float]($pQuito.Y - 5)), 10, 10)

# Yungas
$graphics.FillEllipse($glowRed, ([float]($pYungas.X - 12)), ([float]($pYungas.Y - 12)), 24, 24)
$graphics.FillEllipse($pinRed, ([float]($pYungas.X - 5)), ([float]($pYungas.Y - 5)), 10, 10)
$graphics.DrawEllipse($whitePen, ([float]($pYungas.X - 5)), ([float]($pYungas.Y - 5)), 10, 10)

# Text & Fonts
$fontTitle = New-Object System.Drawing.Font ('Segoe UI', 12, [System.Drawing.FontStyle]::Bold)
$fontSub = New-Object System.Drawing.Font ('Segoe UI', 9)
$fontBold = New-Object System.Drawing.Font ('Segoe UI', 9.5, [System.Drawing.FontStyle]::Bold)
$textWhite = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))
$textGray = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(148, 163, 184))
$textPink = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(253, 164, 175))

# Header Box
$hdrBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(235, 2, 6, 23))
$hdrBorder = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(51, 65, 85)), 1.2
$graphics.FillRectangle($hdrBrush, 25, 25, 460, 56)
$graphics.DrawRectangle($hdrBorder, 25, 25, 460, 56)
$graphics.DrawString('HABITAT RANGE MAP: ANDES CLOUD FOREST', $fontTitle, $textWhite, 35, 32)
$graphics.DrawString('Natural Earth 50m High-Precision Data | Elevation: 2,500m - 3,500m', $fontSub, $textGray, 35, 54)

# Inset Box
$graphics.FillRectangle($hdrBrush, 620, 25, 315, 140)
$graphics.DrawRectangle($hdrBorder, 620, 25, 315, 140)
$graphics.DrawString('SECONDARY PROTECTED COLONIES', $fontBold, $textWhite, 635, 35)

$goldBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(250, 204, 21))
$graphics.FillEllipse($goldBrush, 638, 62, 8, 8)
$graphics.DrawString('Tokyo Hachioji Mt. Takao Mana Reserve', $fontBold, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(254, 240, 138))), 655, 58)
$graphics.DrawString('Tokyo Hachioji Buffer Zone 3 / 8 Colonies (45)', $fontSub, $textGray, 655, 74)

$blueBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(56, 189, 248))
$graphics.FillEllipse($blueBrush, 638, 100, 8, 8)
$graphics.DrawString('European Alps Foothill Reserve (Swiss/Austria)', $fontBold, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(186, 230, 253))), 655, 96)
$graphics.DrawString('Alpine Mist Corridor / Elevation 1,600m', $fontSub, $textGray, 655, 112)

# Pin Callouts
$lblPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(244, 63, 94)), 1
$graphics.FillRectangle($hdrBrush, ([float]($pCusco.X + 65)), ([float]($pCusco.Y - 40)), 230, 30)
$graphics.DrawRectangle($lblPen, ([float]($pCusco.X + 65)), ([float]($pCusco.Y - 40)), 230, 30)
$graphics.DrawLine($lblPen, [float]$pCusco.X, [float]$pCusco.Y, ([float]($pCusco.X + 65)), ([float]($pCusco.Y - 25)))
$graphics.DrawString('Cusco-Urubamba Singularity Core', $fontBold, $textPink, ([float]($pCusco.X + 75)), ([float]($pCusco.Y - 33)))

# Legend
$graphics.FillRectangle($hdrBrush, 25, 690, 420, 130)
$graphics.DrawRectangle($lblPen, 25, 690, 420, 130)
$graphics.DrawString('HABITAT & CONSERVATION LEGEND', $fontBold, $textPink, 38, 702)

$graphics.FillEllipse($pinRed, 38, 730, 12, 12)
$graphics.DrawEllipse($whitePen, 38, 730, 12, 12)
$graphics.DrawString('Primary Habitat (Andes Singularity: 2,500-3,500m)', $fontSub, $textGray, 58, 728)

$polyIcon = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(120, 244, 63, 94))
$graphics.FillRectangle($polyIcon, 38, 755, 12, 12)
$graphics.DrawRectangle($lblPen, 38, 755, 12, 12)
$graphics.DrawString('Highland Range & Migration (Elevation 2,000-4,000m)', $fontSub, $textGray, 58, 753)

$graphics.DrawLine($spinePen, 38, 785, 52, 785)
$graphics.DrawString('Andes Continental Mountain Spine', $fontSub, $textGray, 58, 778)

# Output PNG
$pngPath = 'assets/creatures/006_carbuncle/carbuncle_range_map.png'
$bitmap.Save($pngPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
Write-Host "High-Precision 50m Natural Earth PNG successfully generated: $pngPath"
