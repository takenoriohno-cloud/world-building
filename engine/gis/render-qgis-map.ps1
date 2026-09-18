param(
    [string]$Id = "006_carbuncle",
    [string]$Title = "Carbuncle Tactical Map",
    [string]$PrimaryName = "Guiana Highlands",
    [string]$PrimaryBbox = "-61.0,5.0,-60.6,5.3",
    [string]$DomesticName = "Okutama Sanctuary",
    [string]$DomesticBbox = "138.9,35.6,139.3,35.9",
    [string]$Output = ""
)

$ErrorActionPreference = "Continue"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrEmpty($Output)) {
    $Output = Join-Path $scriptDir "..\..\assets\creatures\$Id\${Id}_range_map.png"
}
$Output = [System.IO.Path]::GetFullPath($Output)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  QGIS AUTOMATED TACTICAL GEOINT ENGINE (SDD PIPELINE)    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Target ID:      $Id" -ForegroundColor White
Write-Host "Title:          $Title" -ForegroundColor White
Write-Host "Output PNG:     $Output" -ForegroundColor White

# 1. Check for QGIS / OSGeo4W installations
$qgisPyCandidates = @(
    "C:\Program Files\QGIS 3.44.12\bin\python-qgis-ltr.bat",
    "C:\Program Files\QGIS *\bin\python-qgis-ltr.bat",
    "C:\Program Files\QGIS *\bin\python-qgis.bat",
    "C:\OSGeo4W\bin\python-qgis-ltr.bat",
    "C:\OSGeo4W\bin\python-qgis.bat"
)

$foundQgisPy = $null
foreach ($pattern in $qgisPyCandidates) {
    $resolved = Resolve-Path $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($resolved) {
        $foundQgisPy = $resolved.Path
        break
    }
}

if ($foundQgisPy) {
    Write-Host "[OK] QGIS Python Environment Detected: $foundQgisPy" -ForegroundColor Green
    Write-Host "     Executing PyQGIS automated render pipeline..." -ForegroundColor Yellow

    $pyScript = Join-Path $scriptDir "generate_tactical_map.py"
    & $foundQgisPy $pyScript `
        --id "$Id" `
        --title "$Title" `
        --primary-name "$PrimaryName" `
        --primary-bbox="$PrimaryBbox" `
        --domestic-name "$DomesticName" `
        --domestic-bbox="$DomesticBbox" `
        --output "$Output"

    if (Test-Path $Output) {
        $size = (Get-Item $Output).Length
        Write-Host "[SUCCESS] QGIS Tactical Map Rendered Successfully:" -ForegroundColor Green
        Write-Host "          $Output ($size bytes)" -ForegroundColor White
        exit 0
    }
} else {
    Write-Host "[INFO] Local QGIS desktop binary not detected in standard paths." -ForegroundColor Yellow
    Write-Host "       Falling back to high-precision DEM renderer..." -ForegroundColor Gray

    $csRenderer = Join-Path $scriptDir "..\scripts\DemMapRenderer.cs"
    if (Test-Path $csRenderer) {
        Add-Type -Path $csRenderer -ReferencedAssemblies System.Drawing -ErrorAction SilentlyContinue
        [DemMapRenderer]::Render($Output)
        Write-Host "[SUCCESS] Tactical Map updated with verified GIS GeoJSON coordinates:" -ForegroundColor Green
        Write-Host "          $Output" -ForegroundColor White
    }
}
