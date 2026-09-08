$out = @()
for ($i = 101; $i -le 200; $i++) {
    $num = "{0:D3}" -f $i
    $file = "ref_raw/magic_page_$num.html"
    if (Test-Path $file) {
        $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $file))
        $html = [System.Text.Encoding]::UTF8.GetString($bytes)
        
        # Strip HTML tags simply
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
        
        $out += "=== PAGE $num ==="
        $out += $clean_text
        $out += "`n"
    }
}
[System.IO.File]::WriteAllLines("scratch_101_200_full_text.txt", $out, [System.Text.Encoding]::UTF8)
Write-Output "Extracted full text of 101-200 to scratch_101_200_full_text.txt"
