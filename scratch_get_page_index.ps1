$lines = [System.IO.File]::ReadAllLines("scratch_301_400_full_text.txt", [System.Text.Encoding]::UTF8)
$page_lines = @()
for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match '^=== PAGE (\d+) ===') {
        $page_lines += ("Line " + ($i+1) + ": Page " + $matches[1])
    }
}
[System.IO.File]::WriteAllLines("scratch_301_400_page_index.txt", $page_lines, [System.Text.Encoding]::UTF8)
Write-Output ("Found " + $page_lines.Count + " pages.")
