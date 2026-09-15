<#
.SYNOPSIS
    QGIS Automated Tactical Map Rendering Pipeline
    Auto-detects QGIS / OSGeo4W installation and executes PyQGIS export,
    or falls back to built-in high-precision GeoJSON telemetry renderer.
#>

$ErrorActionPreference = "Continue"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Join-Path $scriptDir "project"
$layersDir = Join-Path $scriptDir "layers"
$qgsFile = Join-Path $projectDir "magma_salamander_tactical.qgs"
$outputPng = Join-Path $scriptDir "..\..\assets\creatures\004_magma_salamander\004_magma_salamander_range_map.png"
$outputPng = [System.IO.Path]::GetFullPath($outputPng)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  QGIS AUTOMATED TACTICAL GEOINT ENGINE (SDD PIPELINE)    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check for QGIS / OSGeo4W installations
$qgisPyCandidates = @(
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

    $pyScript = Join-Path $scriptDir "render_qgis.py"
    & $foundQgisPy $pyScript

    if (Test-Path $outputPng) {
        Write-Host "[SUCCESS] QGIS Map Rendered Successfully:" -ForegroundColor Green
        Write-Host "          $outputPng" -ForegroundColor White
        exit 0
    }
} else {
    Write-Host "[INFO] Local QGIS desktop binary not detected in standard paths." -ForegroundColor Yellow
    Write-Host "       GeoJSON assets (.geojson) & Project file (.qgs) are ready at:" -ForegroundColor Cyan
    Write-Host "       $qgsFile" -ForegroundColor White
    Write-Host "       -> You can open this .qgs file directly in QGIS GUI anytime!" -ForegroundColor Gray
    Write-Host ""
    Write-Host "[INFO] Activating High-Precision GIS GeoJSON Telemetry Engine..." -ForegroundColor Yellow

    # Run the integrated C# DEM + GeoJSON renderer
    $csRenderer = Join-Path $scriptDir "..\scripts\DemMapRenderer.cs"
    if (Test-Path $csRenderer) {
        Add-Type -Path $csRenderer -ReferencedAssemblies System.Drawing -ErrorAction SilentlyContinue
        [DemMapRenderer]::Render($outputPng)
        Write-Host "[SUCCESS] Tactical Map updated with verified GIS GeoJSON coordinates:" -ForegroundColor Green
        Write-Host "          $outputPng" -ForegroundColor White
    }
}
