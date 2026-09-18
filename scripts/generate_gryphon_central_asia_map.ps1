# scripts/generate_gryphon_central_asia_map.ps1
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Drawing

$json = Get-Content 'assets/templates/ne_50m_countries.json' -Raw | ConvertFrom-Json

$width = 960
$height = 850
# Region: Central Asia / Eurasia (Altai, Tien Shan, Ural, Sayan)
# Longitude: 45°E to 105°E (span 60°)
# Latitude: 60°N to 35°N (span 25°)
$lonMin = 45.0
$lonMax = 105.0
$latMax = 60.0
$latMin = 35.0

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

$targetCountries = @('Russia', 'Kazakhstan', 'Mongolia', 'China', 'Kyrgyzstan', 'Tajikistan', 'Uzbekistan', 'Turkmenistan', 'Iran', 'Afghanistan', 'Pakistan', 'India', 'Georgia', 'Azerbaijan', 'Armenia')

$allLandPaths = New-Object System.Text.StringBuilder
$countryPolys = @()

foreach ($feat in $json.features) {
    $name = $feat.properties.NAME
    if (-not $name) { $name = $feat.properties.ADMIN }
    if ($targetCountries -contains $name) {
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

# Altai Mountain Range Primary Singularity Corridor (Elevation 2,500 - 4,500m)
# Encompasses Russian Altai, Mongolian Altai, Kazakh Altai, Sayan
$altaiCoords = @(
    @(82.0, 52.5),
    @(86.0, 53.5),
    @(90.0, 52.5),
    @(94.0, 51.5),
    @(97.0, 49.5),
    @(95.0, 47.0),
    @(92.0, 46.0),
    @(88.0, 46.5),
    @(84.0, 48.0),
    @(82.5, 50.0)
)
$altaiPath = Convert-RingToPath $altaiCoords

# Tien Shan Corridor
$tienShanCoords = @(
    @(72.0, 42.0),
    @(76.0, 43.0),
    @(80.5, 43.5),
    @(85.0, 43.0),
    @(86.0, 41.5),
    @(80.0, 41.0),
    @(75.0, 40.5),
    @(72.5, 41.0)
)
$tienShanPath = Convert-RingToPath $tienShanCoords

# Hotspots
$pBelukha = Project-Point 86.5 49.8     # Mt. Belukha (Altai Primary Core 4,506m)
$pSayan = Project-Point 93.5 52.0       # Sayan Lightning Ridge
$pKhanTengri = Project-Point 80.2 42.2  # Khan Tengri (Tien Shan 7,010m)
$pUral = Project-Point 59.5 58.0        # Polar/Subpolar Ural Thunder Ridge

# Output Directory
$outDir = 'assets/creatures/002_thunder_gryphon'
if (-not (Test-Path $outDir)) { [void](New-Item -ItemType Directory -Path $outDir) }

# 1. Build High-Precision SVG
$sbSvg = New-Object System.Text.StringBuilder
[void]$sbSvg.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$sbSvg.AppendLine('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 850" width="100%" height="100%">')
[void]$sbSvg.AppendLine('  <defs>')
[void]$sbSvg.AppendLine('    <linearGradient id="bgGradCa" x1="0%" y1="0%" x2="0%" y2="100%">')
[void]$sbSvg.AppendLine('      <stop offset="0%" stop-color="#0b1329" />')
[void]$sbSvg.AppendLine('      <stop offset="100%" stop-color="#020617" />')
[void]$sbSvg.AppendLine('    </linearGradient>')
[void]$sbSvg.AppendLine('    <linearGradient id="altaiGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
[void]$sbSvg.AppendLine('      <stop offset="0%" stop-color="#eab308" stop-opacity="0.85" />')
[void]$sbSvg.AppendLine('      <stop offset="100%" stop-color="#ca8a04" stop-opacity="0.5" />')
[void]$sbSvg.AppendLine('    </linearGradient>')
[void]$sbSvg.AppendLine('    <linearGradient id="tienShanGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
[void]$sbSvg.AppendLine('      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.75" />')
[void]$sbSvg.AppendLine('      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.45" />')
[void]$sbSvg.AppendLine('    </linearGradient>')
[void]$sbSvg.AppendLine('    <filter id="glowGold" x="-20%" y="-20%" width="140%" height="140%">')
[void]$sbSvg.AppendLine('      <feGaussianBlur stdDeviation="4" result="blur" />')
[void]$sbSvg.AppendLine('      <feComposite in="SourceGraphic" in2="blur" operator="over" />')
[void]$sbSvg.AppendLine('    </filter>')
[void]$sbSvg.AppendLine('  </defs>')

[void]$sbSvg.AppendLine('  <!-- Dark Map Background -->')
[void]$sbSvg.AppendLine('  <rect width="960" height="850" fill="url(#bgGradCa)" />')

[void]$sbSvg.AppendLine('  <!-- Graticule (Lat/Lon Coordinates) -->')
[void]$sbSvg.AppendLine('  <g stroke="#1e293b" stroke-width="0.6" stroke-dasharray="3,3">')

for ($lon = 50; $lon -le 100; $lon += 10) {
    $p1 = Project-Point $lon 60
    $p2 = Project-Point $lon 35
    [void]$sbSvg.AppendLine(('    <line x1="{0}" y1="{1}" x2="{2}" y2="{3}" />' -f $p1.X, $p1.Y, $p2.X, $p2.Y))
}
for ($lat = 55; $lat -ge 35; $lat -= 5) {
    $p1 = Project-Point 45 $lat
    $p2 = Project-Point 105 $lat
    $sw = if ($lat -eq 50) { 'stroke="#334155" stroke-width="1.2"' } else { 'stroke="#1e293b" stroke-width="0.6"' }
    [void]$sbSvg.AppendLine(('    <line x1="{0}" y1="{1}" x2="{2}" y2="{3}" {4} />' -f $p1.X, $p1.Y, $p2.X, $p2.Y, $sw))
}
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Coordinate Text Labels -->')
[void]$sbSvg.AppendLine('  <g fill="#64748b" font-size="9" font-family="sans-serif">')
for ($lon = 50; $lon -le 100; $lon += 10) {
    $p = Project-Point $lon 35.5
    [void]$sbSvg.AppendLine(('    <text x="{0}" y="{1}">{2}&#176;E</text>' -f ($p.X - 10), ($height - 15), $lon))
}
for ($lat = 55; $lat -ge 35; $lat -= 5) {
    $p = Project-Point 46 $lat
    [void]$sbSvg.AppendLine(('    <text x="12" y="{0}">{1}&#176;N</text>' -f ($p.Y + 3), $lat))
}
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Natural Earth 50m High-Precision Landmass -->')
[void]$sbSvg.AppendLine('  <g id="central-asia-landmass">')
[void]$sbSvg.AppendLine(('    <path d="{0}" fill="#1e293b" stroke="#475569" stroke-width="1.2" stroke-linejoin="round" />' -f $allLandPaths.ToString()))
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Steppe / Basin Ambient Area -->')
[void]$sbSvg.AppendLine('  <path d="M 220,380 Q 420,360 620,400 Q 720,480 600,560 Q 400,580 260,520 Z" fill="#14261c" fill-opacity="0.4" stroke="#1b4332" stroke-width="1" stroke-dasharray="3,3" />')
[void]$sbSvg.AppendLine('  <text x="360" y="470" fill="#4ade80" font-size="12" font-family="sans-serif" font-weight="bold" opacity="0.3" letter-spacing="4">EURASIAN STEPPE &amp; KAZAKH UPLANDS</text>')

[void]$sbSvg.AppendLine('  <!-- Mountain Spine Lines (Ural, Altai, Tien Shan, Sayan) -->')
[void]$sbSvg.AppendLine('  <path d="M 250,90 L 245,220 L 255,380 L 260,540" fill="none" stroke="#64748b" stroke-width="3.5" stroke-linecap="round" opacity="0.4" />')
[void]$sbSvg.AppendLine('  <path d="M 580,240 L 640,320 L 700,420 L 760,510" fill="none" stroke="#64748b" stroke-width="4" stroke-linecap="round" opacity="0.4" />')

[void]$sbSvg.AppendLine('  <!-- Primary Habitat: Altai Gold-Lightning Singularity Core -->')
[void]$sbSvg.AppendLine('  <g id="altai-singularity-corridor">')
[void]$sbSvg.AppendLine(('    <path d="{0}" fill="url(#altaiGoldGrad)" stroke="#facc15" stroke-width="2" filter="url(#glowGold)" />' -f $altaiPath))
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Secondary Habitat: Tien Shan Thunder Mountain Corridor -->')
[void]$sbSvg.AppendLine('  <g id="tienshan-corridor">')
[void]$sbSvg.AppendLine(('    <path d="{0}" fill="url(#tienShanGrad)" stroke="#38bdf8" stroke-width="1.8" />' -f $tienShanPath))
[void]$sbSvg.AppendLine('  </g>')

# Hotspots
[void]$sbSvg.AppendLine('  <!-- Hotspot 1: Mt. Belukha Core -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pBelukha.X, $pBelukha.Y))
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="16" fill="#eab308" fill-opacity="0.4" filter="url(#glowGold)" />')
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="7" fill="#facc15" stroke="#ffffff" stroke-width="2" />')
[void]$sbSvg.AppendLine('    <line x1="0" y1="0" x2="-65" y2="-25" stroke="#facc15" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <rect x="-275" y="-40" width="205" height="30" rx="4" fill="#020617" fill-opacity="0.95" stroke="#facc15" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <text x="-265" y="-20" fill="#fef08a" font-size="11" font-family="sans-serif" font-weight="bold">&#9733; Mt. Belukha Alpha Nest Core</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Hotspot 2: Sayan Ridge -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pSayan.X, $pSayan.Y))
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="11" fill="#eab308" fill-opacity="0.3" />')
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="5" fill="#ca8a04" stroke="#ffffff" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <line x1="0" y1="0" x2="45" y2="-20" stroke="#facc15" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <rect x="50" y="-32" width="165" height="24" rx="3" fill="#020617" fill-opacity="0.9" stroke="#facc15" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <text x="58" y="-16" fill="#fef08a" font-size="9.5" font-family="sans-serif" font-weight="bold">&#9312; Sayan Lightning Ridge</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Hotspot 3: Khan Tengri -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pKhanTengri.X, $pKhanTengri.Y))
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="12" fill="#38bdf8" fill-opacity="0.3" />')
[void]$sbSvg.AppendLine('    <circle cx="0" cy="0" r="5" fill="#0284c7" stroke="#ffffff" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <line x1="0" y1="0" x2="-50" y2="25" stroke="#38bdf8" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <rect x="-215" y="15" width="160" height="24" rx="3" fill="#020617" fill-opacity="0.9" stroke="#38bdf8" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <text x="-205" y="31" fill="#bae6fd" font-size="9.5" font-family="sans-serif" font-weight="bold">&#9313; Khan Tengri High Corridor</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Hotspot 4: Ural Ridge -->')
[void]$sbSvg.AppendLine(('  <g transform="translate({0},{1})">' -f $pUral.X, $pUral.Y))
[void]$sbSvg.AppendLine('    <polygon points="0,-7 7,0 0,7 -7,0" fill="#facc15" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <rect x="-165" y="-12" width="150" height="22" rx="3" fill="#020617" fill-opacity="0.85" stroke="#facc15" stroke-width="1" />')
[void]$sbSvg.AppendLine('    <text x="-158" y="3" fill="#fef08a" font-size="8.5" font-family="sans-serif" font-weight="bold">&#9314; Ural Gold Mine Lodes</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Map Header Box -->')
[void]$sbSvg.AppendLine('  <g transform="translate(25, 25)">')
[void]$sbSvg.AppendLine('    <rect width="470" height="56" rx="4" fill="#020617" fill-opacity="0.92" stroke="#334155" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="16" y="24" fill="#f8fafc" font-size="13" font-family="sans-serif" font-weight="bold">HABITAT RANGE MAP: ALTAI-EURASIA MOUNTAIN CORRIDOR</text>')
[void]$sbSvg.AppendLine('    <text x="16" y="44" fill="#94a3b8" font-size="9.5" font-family="sans-serif">Natural Earth 50m High-Precision Data / Elevation: 2,500m - 4,500m</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Inset Map: Secondary Colonies -->')
[void]$sbSvg.AppendLine('  <g transform="translate(620, 25)">')
[void]$sbSvg.AppendLine('    <rect width="315" height="150" rx="4" fill="#020617" fill-opacity="0.95" stroke="#475569" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <rect x="0" y="0" width="315" height="22" rx="3" fill="#1e293b" />')
[void]$sbSvg.AppendLine('    <text x="12" y="15" fill="#e2e8f0" font-size="9.5" font-family="sans-serif" font-weight="bold">SECONDARY HABITAT / DEFENSE ZONES</text>')
[void]$sbSvg.AppendLine('    <circle cx="35" cy="50" r="5" fill="#ef4444" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="50" y="48" fill="#fca5a5" font-size="10" font-family="sans-serif" font-weight="bold">North America: Cascade Mt. Air Sector</text>')
[void]$sbSvg.AppendLine('    <text x="50" y="62" fill="#94a3b8" font-size="8.5" font-family="sans-serif">Mt. Rainier - Seattle Corridor (Ares Escort Zone)</text>')
[void]$sbSvg.AppendLine('    <circle cx="35" cy="92" r="5" fill="#38bdf8" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="50" y="90" fill="#bae6fd" font-size="10" font-family="sans-serif" font-weight="bold">Japan: Northern Alps / Mt. Fuji ADIZ</text>')
[void]$sbSvg.AppendLine('    <text x="50" y="104" fill="#94a3b8" font-size="8.5" font-family="sans-serif">JGSDF 1st ADA / 87-AW Air Defense Sector</text>')
[void]$sbSvg.AppendLine('    <rect x="15" y="120" width="285" height="20" rx="3" fill="#854d0e" fill-opacity="0.6" stroke="#eab308" stroke-width="0.8" />')
[void]$sbSvg.AppendLine('    <text x="25" y="134" fill="#fde047" font-size="8.5" font-family="sans-serif" font-weight="bold">Class-B Controlled / Threat Level III (Air Defense)</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Legend Box -->')
[void]$sbSvg.AppendLine('  <g transform="translate(25, 690)">')
[void]$sbSvg.AppendLine('    <rect width="450" height="130" rx="4" fill="#020617" fill-opacity="0.92" stroke="#eab308" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="14" y="20" fill="#fde047" font-size="11" font-family="sans-serif" font-weight="bold">HABITAT &amp; AIR DEFENSE LEGEND</text>')
[void]$sbSvg.AppendLine('    <circle cx="25" cy="42" r="7" fill="#eab308" stroke="#ffffff" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <text x="42" y="46" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">Primary Habitat (Altai Gold-Lightning Core Elev. 2,500-4,500m)</text>')
[void]$sbSvg.AppendLine('    <rect x="18" y="58" width="14" height="14" fill="#38bdf8" fill-opacity="0.4" stroke="#0284c7" stroke-dasharray="3,2" />')
[void]$sbSvg.AppendLine('    <text x="42" y="69" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">Secondary Mountain Corridor (Tien Shan / Ural Ridge)</text>')
[void]$sbSvg.AppendLine('    <polygon points="25,90 30,96 25,102 20,96" fill="#facc15" stroke="#ffffff" />')
[void]$sbSvg.AppendLine('    <text x="42" y="99" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">Ancient Gold Lode Singularity (Cryptobiosis / Bio-Charge Nests)</text>')
[void]$sbSvg.AppendLine('    <line x1="18" y1="116" x2="32" y2="116" stroke="#cbd5e1" stroke-width="3" />')
[void]$sbSvg.AppendLine('    <text x="42" y="120" fill="#94a3b8" font-size="9.5" font-family="sans-serif">Eurasian High Mountain Spines (Altai, Tien Shan, Sayan)</text>')
[void]$sbSvg.AppendLine('  </g>')
[void]$sbSvg.AppendLine('</svg>')

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $outDir 'gryphon_map.svg'), $sbSvg.ToString(), $utf8NoBom)
Write-Host 'High-Precision 50m Natural Earth SVG generated: gryphon_map.svg'

# 2. Render High-Precision PNG via System.Drawing
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

# Background
$bgBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(11, 19, 41))
$graphics.FillRectangle($bgBrush, 0, 0, $width, $height)

# Graticule
$gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(30, 41, 59)), 1
for ($lon = 50; $lon -le 100; $lon += 10) {
    $p1 = Project-Point $lon 60
    $p2 = Project-Point $lon 35
    $graphics.DrawLine($gridPen, [float]$p1.X, [float]$p1.Y, [float]$p2.X, [float]$p2.Y)
}
for ($lat = 55; $lat -ge 35; $lat -= 5) {
    $p1 = Project-Point 45 $lat
    $p2 = Project-Point 105 $lat
    $graphics.DrawLine($gridPen, [float]$p1.X, [float]$p1.Y, [float]$p2.X, [float]$p2.Y)
}

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

# Altai Polygon (Gold)
$altaiPts = @()
foreach ($pt in $altaiCoords) {
    $p = Project-Point ([double]$pt[0]) ([double]$pt[1])
    $altaiPts += (New-Object System.Drawing.PointF ([float]$p.X), ([float]$p.Y))
}
$altaiBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(160, 234, 179, 8))
$altaiPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(250, 204, 21)), 2.5
$graphics.FillPolygon($altaiBrush, [System.Drawing.PointF[]]$altaiPts)
$graphics.DrawPolygon($altaiPen, [System.Drawing.PointF[]]$altaiPts)

# Tien Shan Polygon (Blue)
$tsPts = @()
foreach ($pt in $tienShanCoords) {
    $p = Project-Point ([double]$pt[0]) ([double]$pt[1])
    $tsPts += (New-Object System.Drawing.PointF ([float]$p.X), ([float]$p.Y))
}
$tsBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(120, 56, 189, 248))
$tsPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(2, 132, 199)), 1.8
$graphics.FillPolygon($tsBrush, [System.Drawing.PointF[]]$tsPts)
$graphics.DrawPolygon($tsPen, [System.Drawing.PointF[]]$tsPts)

# Hotspots
$coreBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(250, 204, 21))
$whitePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::White), 2
$graphics.FillEllipse($coreBrush, [float]($pBelukha.X - 8), [float]($pBelukha.Y - 8), 16, 16)
$graphics.DrawEllipse($whitePen, [float]($pBelukha.X - 8), [float]($pBelukha.Y - 8), 16, 16)

# Overlay Header & Insets
$headerBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(235, 2, 6, 23))
$headerPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(51, 65, 85)), 1.2
$graphics.FillRectangle($headerBrush, 25, 25, 470, 56)
$graphics.DrawRectangle($headerPen, 25, 25, 470, 56)

$fBold = New-Object System.Drawing.Font ('Arial', 11, [System.Drawing.FontStyle]::Bold)
$fSub = New-Object System.Drawing.Font ('Arial', 8.5)
$textWhite = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(248, 250, 252))
$textMuted = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(148, 163, 184))

$graphics.DrawString('HABITAT RANGE MAP: ALTAI-EURASIA MOUNTAIN CORRIDOR', $fBold, $textWhite, [float]40, [float]38)
$graphics.DrawString('Natural Earth 50m High-Precision Data / Elevation: 2,500m - 4,500m', $fSub, $textMuted, [float]40, [float]58)

# Inset box
$graphics.FillRectangle($headerBrush, 620, 25, 315, 150)
$graphics.DrawRectangle((New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(71, 85, 105)), 1.2), 620, 25, 315, 150)
$graphics.DrawString('SECONDARY HABITAT / DEFENSE ZONES', $fBold, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(226, 232, 240))), [float]635, [float]35)
$graphics.DrawString('North America: Cascade Mt. Air Sector (Ares Escort)', $fSub, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(254, 202, 202))), [float]640, [float]65)
$graphics.DrawString('Japan: Northern Alps / Mt. Fuji ADIZ (JGSDF 87-AW)', $fSub, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(186, 230, 253))), [float]640, [float]100)

# Legend box
$legendPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(234, 179, 8)), 1.2
$graphics.FillRectangle($headerBrush, 25, 690, 450, 130)
$graphics.DrawRectangle($legendPen, 25, 690, 450, 130)
$graphics.DrawString('HABITAT & AIR DEFENSE LEGEND', $fBold, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(253, 224, 71))), [float]40, [float]705)
$graphics.DrawString('Primary: Altai Gold-Lightning Singularity Core (Elev. 2,500-4,500m)', $fSub, $textWhite, [float]55, [float]730)
$graphics.DrawString('Secondary: Tien Shan / Ural Mountain Spines', $fSub, $textWhite, [float]55, [float]755)
$graphics.DrawString('Ancient Gold Lode Singularity (Bio-Charge Nests)', $fSub, $textWhite, [float]55, [float]780)

$pngPath = Join-Path $outDir 'gryphon_range_map.png'
$bitmap.Save($pngPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
Write-Host "High-Precision PNG generated: $pngPath"
