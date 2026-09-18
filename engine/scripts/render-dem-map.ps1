$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$csPath = Join-Path $scriptDir "DemMapRenderer.cs"
$outputPath = Join-Path $scriptDir "..\..\assets\creatures\004_magma_salamander\004_magma_salamander_range_map.png"
$outputPath = [System.IO.Path]::GetFullPath($outputPath)

# Compile C# class
Add-Type -Path $csPath -ReferencedAssemblies System.Drawing

# Render
[DemMapRenderer]::Render($outputPath)

Write-Host "[OK] High-Resolution DEM Tactical Map successfully rendered:"
Write-Host "     $outputPath"
