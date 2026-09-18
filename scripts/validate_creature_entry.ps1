# Automated Creature Entry Validator (PowerShell)
# Usage: powershell -ExecutionPolicy Bypass -File scripts/validate_creature_entry.ps1 -FilePath creatures/007_pyro_pride_lion.md

param (
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

if (-not (Test-Path $FilePath)) {
    Write-Error "File not found: $FilePath"
    exit 1
}

$lines = Get-Content -Path $FilePath -Encoding UTF8
$totalLines = $lines.Count
$errors = [System.Collections.Generic.List[string]]::new()
$evidence = @{}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CREATURE ENTRY RIGOROUS VALIDATOR (SDD Phase 4/6 Audit)   " -ForegroundColor Cyan
Write-Host "  Target File: $FilePath (Total Lines: $totalLines)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Check Mandatory 9 Chapter Headings (Exact Regex)
$chapterPatterns = @(
    @{ Id=1; Name="第1章 基本分類・早わかり"; Regex="^##\s+1\.\s+基本分類・早わかり" },
    @{ Id=2; Name="第2章 伝承考証とマナ覚醒の架橋"; Regex="^##\s+2\.\s+伝承考証とマナ覚醒の架橋" },
    @{ Id=3; Name="第3章 生物学的特徴・ライフステージ"; Regex="^##\s+3\.\s+生物学的特徴・ライフステージ" },
    @{ Id=4; Name="第4章 生態・食物連鎖・人間社会との摩擦"; Regex="^##\s+4\.\s+(生態・食物連鎖・人間社会との摩擦|生態・人間社会摩擦・繁殖育児)" },
    @{ Id=5; Name="第5章 魔導科学・上位神性・背景ロア"; Regex="^##\s+5\.\s+(魔導科学・上位神性・背景ロア|ガープス第4版（GURPS 4th）戦闘データ|ガープス第4版データブロック)" },
    @{ Id=6; Name="第6章 交戦マニュアル・都市防災コラム"; Regex="^##\s+6\.\s+(交戦マニュアル・都市防災コラム|軍事対処・防護プロトコル|交戦マニュアル・防衛対策)" },
    @{ Id=7; Name="第7章 解体・ジビエ食文化・料理レシピ/素材抽出"; Regex="^##\s+7\.\s+(解体・ジビエ食文化・料理レシピ|解体・食利用・素材採取|解体・非可食バイオハザード指定・素材抽出)" },
    @{ Id=8; Name="第8章 現場記録・通信ログ"; Regex="^##\s+8\.\s+(現場記録・通信ログ|現場記録・調査員ログ)" },
    @{ Id=9; Name="第9章 参考文献・典拠資料/派生種"; Regex="^##\s+9\.\s+(参考文献・典拠資料|関連研究・派生種|参考文献・関連資料)" }
)

Write-Host "`n--- [1] 9大章節タイトル Grep 突合検証 ---" -ForegroundColor Yellow
for ($i = 0; $i -lt $chapterPatterns.Count; $i++) {
    $chap = $chapterPatterns[$i]
    $found = $false
    for ($l = 0; $l -lt $lines.Count; $l++) {
        if ($lines[$l] -match $chap.Regex) {
            $lineNum = $l + 1
            $found = $true
            $evidence["Chap_$($chap.Id)"] = "L$lineNum : $($lines[$l])"
            Write-Host "  [PASS] $($chap.Name) -> Line $lineNum" -ForegroundColor Green
            break
        }
    }
    if (-not $found) {
        $errors.Add("Missing Chapter $($chap.Id): $($chap.Name) matching pattern '$($chap.Regex)'")
        Write-Host "  [FAIL] $($chap.Name) -> NOT FOUND" -ForegroundColor Red
    }
}

# 2. Check NatGeo Fast Facts, Scale & Range Map Elements
Write-Host "`n--- [2] ナショナルジオグラフィック流新要素 Grep 検証 ---" -ForegroundColor Yellow

$natGeoChecks = @(
    @{ Name="和名命名規約の明記"; Regex="\*\*和名命名規約\*\*" },
    @{ Name="直感的サイズ比較"; Regex="\*\*直感的サイズ比較\*\*" },
    @{ Name="生息・分布マップ埋め込み"; Regex="!\[生息・分布マップ\]\(.*(map\.svg|range_map\.png)\)" },
    @{ Name="視覚資料アーカイブ（写真テーブル）"; Regex="###\s+視覚資料アーカイブ" },
    @{ Name="Mermaid生体解剖連関図 (flowchart TD)"; Regex="flowchart\s+TD" },
    @{ Name="Mermaid生態系/狩猟ネットワーク図 (flowchart LR)"; Regex="flowchart\s+LR" },
    @{ Name="GURPS Stat Block (```yaml)"; Regex="```yaml" }
)

foreach ($chk in $natGeoChecks) {
    $found = $false
    for ($l = 0; $l -lt $lines.Count; $l++) {
        if ($lines[$l] -match $chk.Regex) {
            $lineNum = $l + 1
            $found = $true
            $evidence[$chk.Name] = "L$lineNum"
            Write-Host "  [PASS] $($chk.Name) -> Line $lineNum" -ForegroundColor Green
            break
        }
    }
    if (-not $found) {
        $errors.Add("Missing NatGeo Element: $($chk.Name) matching '$($chk.Regex)'")
        Write-Host "  [FAIL] $($chk.Name) -> NOT FOUND" -ForegroundColor Red
    }
}

# 3. Summary & Result
Write-Host "`n============================================================" -ForegroundColor Cyan
if ($errors.Count -eq 0) {
    Write-Host "  AUDIT RESULT: ALL CRITERIA PASSED! (0 Errors)" -ForegroundColor Green
    Write-Host "  Ready for Gate 2 PASS / Formal Publication." -ForegroundColor Green
} else {
    Write-Host "  AUDIT RESULT: FAILED ($($errors.Count) Errors Detected)" -ForegroundColor Red
    foreach ($err in $errors) {
        Write-Host "   - $err" -ForegroundColor Red
    }
}
Write-Host "============================================================" -ForegroundColor Cyan

if ($errors.Count -gt 0) {
    exit 1
} else {
    exit 0
}
