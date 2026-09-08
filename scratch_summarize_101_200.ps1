$text = [System.IO.File]::ReadAllText("scratch_101_200_full_text.txt", [System.Text.Encoding]::UTF8)
$pages = $text -split "=== PAGE "

# Let's inspect groups:
# Group 1: 101-108 (Rules: Ceremonial, Area, Staff, Distance, Inventing Spells)
# Group 2: 109-136 (Magic Items, Enchantment, Powerstone economics)
# Group 3: 137-185 (Special College categories: Gates, Animals, Illusions, Golem, Armor Enchantments)
# Group 4: 186-200 (Alternate Magic Systems: Clerical, Ritual Magic, Modifying Prerequisites)

$summary = @()
for ($i = 1; $i -lt $pages.Count; $i++) {
    $p = $pages[$i]
    $lines = $p -split "`n"
    $page_num = $lines[0].Trim()
    $content_sample = ($lines[1..([Math]::Min(10, $lines.Count-1))] -join " ").Trim()
    $summary += "=== $page_num ==="
    $summary += $content_sample.Substring(0, [Math]::Min(150, $content_sample.Length))
}

[System.IO.File]::WriteAllLines("scratch_101_200_summary.txt", $summary, [System.Text.Encoding]::UTF8)
Write-Host "Summary generated!"
