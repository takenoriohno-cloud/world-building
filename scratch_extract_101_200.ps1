$results = @()
for ($i = 101; $i -le 200; $i++) {
    $num = "{0:D3}" -f $i
    $file = "ref_raw/magic_page_$num.html"
    if (Test-Path $file) {
        $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $file))
        $html = [System.Text.Encoding]::GetEncoding('Shift_JIS').GetString($bytes)
        $title = "No Title"
        if ($html -match '<title>(.*?)</title>') {
            $title = $matches[1].Trim()
        }
        $h = ""
        if ($html -match '<h[123][^>]*>(.*?)</h[123]>') {
            $h = ($matches[1] -replace '<.*?>','').Trim()
        }
        $results += ("Page " + $num + ": Title='" + $title + "' | H='" + $h + "'")
    }
}
$results | Out-File -FilePath "scratch_pages_101_200.txt" -Encoding utf8
Write-Host "Extracted" $results.Count "pages."
