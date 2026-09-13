# scripts/fix_carbuncle_svg.ps1
$ErrorActionPreference = 'Stop'

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

foreach ($feat in $json.features) {
    $name = $feat.properties.NAME
    if (-not $name) { $name = $feat.properties.ADMIN }
    if ($saCountries -contains $name) {
        if ($feat.geometry.type -eq 'Polygon') {
            foreach ($ring in $feat.geometry.coordinates) {
                $path = Convert-RingToPath $ring
                [void]$allLandPaths.Append($path + ' ')
            }
        } elseif ($feat.geometry.type -eq 'MultiPolygon') {
            foreach ($poly in $feat.geometry.coordinates) {
                foreach ($ring in $poly) {
                    $path = Convert-RingToPath $ring
                    [void]$allLandPaths.Append($path + ' ')
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
[void]$sbSvg.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
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

[void]$sbSvg.AppendLine('  <!-- Graticule (Lat/Lon Coordinates) -->')
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
[void]$sbSvg.AppendLine('  <g fill="#64748b" font-size="9" font-family="sans-serif">')
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
[void]$sbSvg.AppendLine('    <rect width="460" height="56" rx="4" fill="#020617" fill-opacity="0.92" stroke="#334155" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="16" y="24" fill="#f8fafc" font-size="13" font-family="sans-serif" font-weight="bold">HABITAT RANGE MAP: ANDES CLOUD FOREST SINGULARITY</text>')
[void]$sbSvg.AppendLine('    <text x="16" y="44" fill="#94a3b8" font-size="9.5" font-family="sans-serif">Natural Earth 50m High-Precision Data / Elevation: 2,500m - 3,500m</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Inset Map: Secondary Sanctuaries -->')
[void]$sbSvg.AppendLine('  <g transform="translate(620, 25)">')
[void]$sbSvg.AppendLine('    <rect width="315" height="150" rx="4" fill="#020617" fill-opacity="0.95" stroke="#475569" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <rect x="0" y="0" width="315" height="22" rx="3" fill="#1e293b" />')
[void]$sbSvg.AppendLine('    <text x="12" y="15" fill="#e2e8f0" font-size="9.5" font-family="sans-serif" font-weight="bold">SECONDARY PROTECTED COLONIES</text>')
[void]$sbSvg.AppendLine('    <circle cx="35" cy="50" r="5" fill="#facc15" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="50" y="48" fill="#fef08a" font-size="10" font-family="sans-serif" font-weight="bold">Tokyo Hachioji Mt. Takao Mana Reserve</text>')
[void]$sbSvg.AppendLine('    <text x="50" y="62" fill="#94a3b8" font-size="8.5" font-family="sans-serif">Tokyo Outer Buffer Zone 3 / 8 Families (45 indiv.)</text>')
[void]$sbSvg.AppendLine('    <circle cx="35" cy="92" r="5" fill="#38bdf8" stroke="#ffffff" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="50" y="90" fill="#bae6fd" font-size="10" font-family="sans-serif" font-weight="bold">European Alps Foothill Reserve (Swiss/Austria)</text>')
[void]$sbSvg.AppendLine('    <text x="50" y="104" fill="#94a3b8" font-size="8.5" font-family="sans-serif">Alps Foothill Protected Corridor / Elev. 1,600m</text>')
[void]$sbSvg.AppendLine('    <rect x="15" y="120" width="285" height="20" rx="3" fill="#14532d" fill-opacity="0.6" stroke="#22c55e" stroke-width="0.8" />')
[void]$sbSvg.AppendLine('    <text x="25" y="134" fill="#86efac" font-size="8.5" font-family="sans-serif" font-weight="bold">CITES Appendix I / Class-A Strict Protection</text>')
[void]$sbSvg.AppendLine('  </g>')

[void]$sbSvg.AppendLine('  <!-- Legend Box -->')
[void]$sbSvg.AppendLine('  <g transform="translate(25, 690)">')
[void]$sbSvg.AppendLine('    <rect width="440" height="130" rx="4" fill="#020617" fill-opacity="0.92" stroke="#f43f5e" stroke-width="1.2" />')
[void]$sbSvg.AppendLine('    <text x="14" y="20" fill="#fb7185" font-size="11" font-family="sans-serif" font-weight="bold">HABITAT &amp; CONSERVATION LEGEND</text>')
[void]$sbSvg.AppendLine('    <circle cx="25" cy="42" r="7" fill="#e11d48" stroke="#ffffff" stroke-width="1.5" />')
[void]$sbSvg.AppendLine('    <text x="42" y="46" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">Primary Habitat Core (Andes Cloud Forest Elev. 2,500-3,500m)</text>')
[void]$sbSvg.AppendLine('    <rect x="18" y="58" width="14" height="14" fill="#f43f5e" fill-opacity="0.3" stroke="#fb7185" stroke-dasharray="3,2" />')
[void]$sbSvg.AppendLine('    <text x="42" y="69" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">Highland Foraging &amp; Seasonal Corridor (Elev. 2,000-4,000m)</text>')
[void]$sbSvg.AppendLine('    <polygon points="25,90 30,96 25,102 20,96" fill="#38bdf8" stroke="#ffffff" />')
[void]$sbSvg.AppendLine('    <text x="42" y="99" fill="#cbd5e1" font-size="9.5" font-family="sans-serif">Subterranean Crystal Caves (Ancient Cryptobiosis / Al-Cr Mineral)</text>')
[void]$sbSvg.AppendLine('    <line x1="18" y1="116" x2="32" y2="116" stroke="#cbd5e1" stroke-width="3" />')
[void]$sbSvg.AppendLine('    <text x="42" y="120" fill="#94a3b8" font-size="9.5" font-family="sans-serif">Andes Mountain Spine (Topographic Continental Spine)</text>')
[void]$sbSvg.AppendLine('  </g>')
[void]$sbSvg.AppendLine('</svg>')

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText('assets/creatures/006_carbuncle/carbuncle_map.svg', $sbSvg.ToString(), $utf8NoBom)
Write-Host 'SVG written cleanly with UTF-8 without BOM.'
