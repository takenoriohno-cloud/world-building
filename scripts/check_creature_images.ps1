# scripts/check_creature_images.ps1
$creatures = Get-ChildItem 'creatures/*.md' | Sort-Object Name

foreach ($f in $creatures) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $matches = [regex]::Matches($content, '!\[(?<alt>.*?)\]\((?<url>.*?)\)')
    Write-Host ("=== " + $f.Name + " ===")
    if ($matches.Count -eq 0) {
        Write-Host "  [NO IMAGES FOUND]" -ForegroundColor Red
    } else {
        foreach ($m in $matches) {
            $alt = $m.Groups['alt'].Value
            $url = $m.Groups['url'].Value
            # check if file exists
            $relPath = $url.TrimStart('.').TrimStart('/')
            $fullPath = Join-Path (Get-Location) $relPath
            $exists = Test-Path $fullPath
            $status = if ($exists) { "[EXISTS]" } else { "[MISSING FILE]" }
            $color = if ($exists) { "Green" } else { "Red" }
            Write-Host ("  - " + $status + " " + $alt + " -> " + $url) -ForegroundColor $color
        }
    }
}
