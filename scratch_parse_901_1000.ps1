$outputSummary = "scratch_901_1000_summary.txt"
$outputFull = "scratch_901_1000_full_text.txt"
$outputTable = "scratch_901_1000_table.txt"

"" | Out-File -FilePath $outputSummary -Encoding utf8
"" | Out-File -FilePath $outputFull -Encoding utf8
"" | Out-File -FilePath $outputTable -Encoding utf8

for ($i = 901; $i -le 1000; $i++) {
    $num = "{0:D3}" -f $i
    $path = "ref_raw\magic_page_$num.html"
    if (-not (Test-Path $path)) {
        $path = "ref_raw\magic_page_$i.html"
    }
    
    if (Test-Path $path) {
        $content = Get-Content -Path $path -Raw -Encoding utf8
        
        $title = ""
        if ($content -match '<title>(.*?)</title>') {
            $title = $matches[1]
        }
        
        # 見出し抽出
        $headings = @()
        $pattern = '<h[1-4][^>]*>(.*?)</h[1-4]>'
        $regex = [regex]$pattern
        $matchesH = $regex.Matches($content)
        foreach ($m in $matchesH) {
            $cleanH = $m.Groups[1].Value -replace '<[^>]+>', ''
            $headings += $cleanH.Trim()
        }
        $headingStr = $headings -join " / "
        
        # サマリー
        "Page $i | $title | $headingStr" | Out-File -FilePath $outputSummary -Append -Encoding utf8
        
        # 本文クレンジング
        $cleanText = $content -replace '<script[^>]*>.*?</script>', ''
        $cleanText = $cleanText -replace '<style[^>]*>.*?</style>', ''
        $cleanText = $cleanText -replace '<[^>]+>', ' '
        $cleanText = $cleanText -replace '&nbsp;', ' '
        $cleanText = $cleanText -replace '&lt;', '<'
        $cleanText = $cleanText -replace '&gt;', '>'
        $cleanText = $cleanText -replace '&amp;', '&'
        $cleanText = $cleanText -replace '\s+', ' '
        
        "=== PAGE $i : $title ===" | Out-File -FilePath $outputFull -Append -Encoding utf8
        $cleanText.Trim() | Out-File -FilePath $outputFull -Append -Encoding utf8
        "" | Out-File -FilePath $outputFull -Append -Encoding utf8
        
        "Page $i | $title" | Out-File -FilePath $outputTable -Append -Encoding utf8
    } else {
        "Page $i | FILE NOT FOUND" | Out-File -FilePath $outputSummary -Append -Encoding utf8
    }
}
