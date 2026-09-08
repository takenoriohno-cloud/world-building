$bytes = [System.IO.File]::ReadAllBytes('ref_raw/magic_page_101.html')
$utf8 = [System.Text.Encoding]::UTF8.GetString($bytes)
$sjis = [System.Text.Encoding]::GetEncoding(932).GetString($bytes)
$euc = [System.Text.Encoding]::GetEncoding(51932).GetString($bytes)

Write-Host "UTF8 preview (first 200 chars):"
Write-Host $utf8.Substring(0, [Math]::Min(200, $utf8.Length))
Write-Host "`n---`n"
Write-Host "SJIS preview (first 200 chars):"
Write-Host $sjis.Substring(0, [Math]::Min(200, $sjis.Length))
Write-Host "`n---`n"
Write-Host "EUC-JP preview (first 200 chars):"
Write-Host $euc.Substring(0, [Math]::Min(200, $euc.Length))
