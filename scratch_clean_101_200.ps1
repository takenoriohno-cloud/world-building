$results = @()
for ($i = 101; $i -le 200; $i++) {
    $num = "{0:D3}" -f $i
    $file = "ref_raw/magic_page_$num.html"
    if (Test-Path $file) {
        $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $file))
        $html = [System.Text.Encoding]::UTF8.GetString($bytes)
        
        $title = "No Title"
        if ($html -match '<title>([^<]+)</title>') {
            $title = ($matches[1] -replace '\s*-\s*GURPSよろず.*', '').Trim()
        }
        
        # Look for the main h2 or h3 heading under the main content
        $main_heading = ""
        if ($html -match '(?s)<div id="body">(.*?)</div>') {
            $body = $matches[1]
            if ($body -match '<h[123][^>]*>(.*?)</h[123]>') {
                $main_heading = ($matches[1] -replace '<[^>]+>', '').Trim()
            }
        }
        
        # Check if it has spell data or specific rules
        $is_spell = ($html -match '呪文クラス|基本消費|前提条件')
        $is_magic_item = ($html -match '魔化|品物のパワー|魔法の品物')
        
        $results += "$num | $title | $main_heading | Spell:$is_spell | Item:$is_magic_item"
    }
}
[System.IO.File]::WriteAllLines("scratch_101_200_table.txt", $results, [System.Text.Encoding]::UTF8)
Write-Output "Extracted $($results.Count) lines to scratch_101_200_table.txt"
