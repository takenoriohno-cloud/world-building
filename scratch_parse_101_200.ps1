$results = @()
for ($i = 101; $i -le 200; $i++) {
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
    }
}
[System.IO.File]::WriteAllLines("scratch_pages_101_200_utf8.txt", $results, [System.Text.Encoding]::UTF8)
Write-Output "Done! Count: $($results.Count)"
