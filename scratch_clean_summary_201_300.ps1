$text = [System.IO.File]::ReadAllText("scratch_201_300_full_text.txt", [System.Text.Encoding]::UTF8)
$pages = $text -split "=== PAGE "

$table = @()
for ($i = 1; $i -lt $pages.Count; $i++) {
    $p = $pages[$i]
    $lines = $p -split "`n"
    $page_num = $lines[0].Trim()
    
    $title = ""
    for ($j = 1; $j -lt [Math]::Min(10, $lines.Count); $j++) {
        $l = $lines[$j].Trim()
        if ($l.Length -gt 0) {
            $title = $l
            break
        }
    }
    
    $table += ($page_num + " | " + $title)
}

[System.IO.File]::WriteAllLines("scratch_201_300_clean_summary.txt", $table, [System.Text.Encoding]::UTF8)
Write-Output "Done!"
