$proc = Get-ChildItem -Path "C:\Program Files" -Filter "qgis_process.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if ($proc) {
    Write-Host "[FOUND] qgis_process: $($proc.FullName)"
} else {
    Write-Host "[SEARCHING] Looking in C:\OSGeo4W..."
    $proc = Get-ChildItem -Path "C:\OSGeo4W" -Filter "qgis_process.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($proc) {
        Write-Host "[FOUND] qgis_process in OSGeo4W: $($proc.FullName)"
    } else {
        Write-Host "[SEARCHING] Searching all QGIS files in C:\Program Files..."
        Get-ChildItem -Path "C:\Program Files" -Filter "*qgis*" -ErrorAction SilentlyContinue | Select-Object FullName
    }
}
