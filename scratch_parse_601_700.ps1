$results = @()
$full_text = @()

for ($i = 601; $i -le 700; $i++) {
    $num = "{0:D3}" -f $i
    $file = "ref_raw/magic_page_$num.html"
    if (Test-Path $file) {
        $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $file))
        $html = [System.Text.Encoding]::UTF8.GetString($bytes)
        
        $title = "No Title"
        if ($html -match '<title>([^<]+)</title>') {
            $title = $matches[1].Trim()
        }
        
        $h_list = @()
        $mc = [regex]::Matches($html, '<h[1-4][^>]*>(.*?)</h[1-4]>')
        foreach ($m in $mc) {
            $t = $m.Groups[1].Value -replace '<[^>]+>', ''
            $t = $t.Trim()
            if ($t.Length -gt 0) {
                $h_list += $t
            }
        }
        $h_str = $h_list -join " | "
        $results += ("Page " + $num + " => Title: " + $title + " => Headings: " + $h_str)
        
        # Clean text
        $text = $html -replace '(?s)<style.*?</style>', ''
        $text = $text -replace '(?s)<script.*?</script>', ''
        $text = $text -replace '(?s)<div id="menubar".*?</div>', ''
        $text = $text -replace '(?s)<div id="header".*?</div>', ''
        $text = $text -replace '(?s)<div id="footer".*?</div>', ''
        $text = $text -replace '<[^>]+>', ' '
        $text = $text -replace '&nbsp;', ' '
        $text = $text -replace '&lt;', '<'
        $text = $text -replace '&gt;', '>'
        $text = $text -replace '&amp;', '&'
        $text = $text -replace '[ \t]+', ' '
        $lines = $text -split "\r?\n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
        $clean_text = $lines -join "`n"
        
        $full_text += ("=== PAGE " + $num + " ===")
        $full_text += $clean_text
        $full_text += "`n"
    } else {
        $results += ("Page " + $num + " => NOT_FOUND")
    }
}

[System.IO.File]::WriteAllLines("scratch_601_700_table.txt", $results, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllLines("scratch_601_700_full_text.txt", $full_text, [System.Text.Encoding]::UTF8)
Write-Output ("Extracted " + $results.Count + " pages for 601-700.")
