$lines = [System.IO.File]::ReadAllLines("scratch_401_500_table.txt", [System.Text.Encoding]::UTF8)
$clean = @()
foreach ($line in $lines) {
    if ($line -match 'Page (\d+) => Title: ([^=]+) => Headings: (.*)') {
        $p = $matches[1]
        $t = $matches[2].Trim()
        $h = $matches[3].Trim()
        $parts = $h -split ' \| '
        $filtered = @()
        foreach ($item in $parts) {
            if ($item -notmatch '第\d+章|最近更新|コメント|練習用|フェイク|ルナル|Menu|汎用|はじめに|付録|保留|Martial|Powers|Fantasy|Horror|Supers|Social|Pyramid|GURPS|AD|アクセス|2026-') {
                $filtered += $item
            }
        }
        $h_sub = ($filtered | Select-Object -First 6) -join ' / '
        $clean += ("Page " + $p + " | " + $t + " | " + $h_sub)
    }
}
[System.IO.File]::WriteAllLines("scratch_401_500_clean_summary.txt", $clean, [System.Text.Encoding]::UTF8)
Write-Output ("Clean summary written. Lines: " + $clean.Count)
