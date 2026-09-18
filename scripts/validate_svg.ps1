# scripts/validate_svg.ps1
try {
    $xml = New-Object System.Xml.XmlDocument
    $xml.Load((Resolve-Path 'assets/creatures/002_thunder_gryphon/gryphon_map.svg'))
    Write-Host ("XML Validation SUCCESS! Root element: <" + $xml.DocumentElement.Name + ">")
} catch {
    Write-Error ("XML Validation FAILED: " + $_.Exception.Message)
}
