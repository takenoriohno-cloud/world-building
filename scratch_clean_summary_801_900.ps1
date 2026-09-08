$summaryPath = "scratch_801_900_summary.txt"
$cleanPath = "scratch_801_900_clean_summary.txt"

$lines = Get-Content -Path $summaryPath -Encoding utf8

$cleanLines = @()
foreach ($line in $lines) {
    if ($line.Trim() -ne "") {
        $cleaned = $line -replace ' / メニュー.*$', ''
        $cleaned = $cleaned -replace ' / 最近の.*$', ''
        $cleaned = $cleaned -replace ' / 検索.*$', ''
        $cleaned = $cleaned -replace ' / 関連.*$', ''
        $cleanLines += $cleaned
    }
}

$cleanLines | Out-File -FilePath $cleanPath -Encoding utf8
