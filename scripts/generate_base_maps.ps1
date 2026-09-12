# generate_base_maps.ps1
# .NET System.Drawing を使用して高精細なベース白地図 (base_map_world.png / base_map_japan.png) を生成・配備するスクリプト

Add-Type -AssemblyName System.Drawing

function Create-WorldBaseMap {
    param([string]$outputPath)
    
    $width = 1200
    $height = 600
    
    $bitmap = New-Object System.Drawing.Bitmap($width, $height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    
    # 背景（海洋・深海ダークネイビー）
    $oceanBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(20, 26, 38))
    $graphics.FillRectangle($oceanBrush, 0, 0, $width, $height)
    
    # グリッド線
    $gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(35, 45, 65), 1)
    for ($x = 0; $x -lt $width; $x += 40) {
        $graphics.DrawLine($gridPen, $x, 0, $x, $height)
    }
    for ($y = 0; $y -lt $height; $y += 40) {
        $graphics.DrawLine($gridPen, 0, $y, $width, $y)
    }
    
    # 赤道・子午線
    $guidePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(50, 65, 95), 1)
    $guidePen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Dash
    $graphics.DrawLine($guidePen, 0, 300, $width, 300)
    $graphics.DrawLine($guidePen, 600, 0, 600, $height)
    
    # 大陸の描画 (Landmass)
    $landBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(42, 53, 74))
    $landPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(65, 82, 115), 1.5)
    
    # 北米・グリーンランド
    $naPoints = @(
        (New-Object System.Drawing.PointF(70, 90)),
        (New-Object System.Drawing.PointF(120, 65)),
        (New-Object System.Drawing.PointF(200, 75)),
        (New-Object System.Drawing.PointF(270, 90)),
        (New-Object System.Drawing.PointF(260, 140)),
        (New-Object System.Drawing.PointF(210, 155)),
        (New-Object System.Drawing.PointF(220, 185)),
        (New-Object System.Drawing.PointF(250, 200)),
        (New-Object System.Drawing.PointF(260, 250)),
        (New-Object System.Drawing.PointF(220, 290)),
        (New-Object System.Drawing.PointF(190, 295)),
        (New-Object System.Drawing.PointF(175, 250)),
        (New-Object System.Drawing.PointF(135, 210)),
        (New-Object System.Drawing.PointF(100, 175)),
        (New-Object System.Drawing.PointF(60, 140))
    )
    $graphics.FillPolygon($landBrush, $naPoints)
    $graphics.DrawPolygon($landPen, $naPoints)

    # グリーンランド
    $glPoints = @(
        (New-Object System.Drawing.PointF(280, 55)),
        (New-Object System.Drawing.PointF(315, 60)),
        (New-Object System.Drawing.PointF(325, 95)),
        (New-Object System.Drawing.PointF(300, 115)),
        (New-Object System.Drawing.PointF(260, 100))
    )
    $graphics.FillPolygon($landBrush, $glPoints)
    $graphics.DrawPolygon($landPen, $glPoints)

    # 南米
    $saPoints = @(
        (New-Object System.Drawing.PointF(200, 300)),
        (New-Object System.Drawing.PointF(245, 305)),
        (New-Object System.Drawing.PointF(280, 335)),
        (New-Object System.Drawing.PointF(310, 385)),
        (New-Object System.Drawing.PointF(280, 460)),
        (New-Object System.Drawing.PointF(245, 520)),
        (New-Object System.Drawing.PointF(225, 550)),
        (New-Object System.Drawing.PointF(210, 550)),
        (New-Object System.Drawing.PointF(200, 465)),
        (New-Object System.Drawing.PointF(190, 370)),
        (New-Object System.Drawing.PointF(175, 310))
    )
    $graphics.FillPolygon($landBrush, $saPoints)
    $graphics.DrawPolygon($landPen, $saPoints)

    # ユーラシア大陸
    $eaPoints = @(
        (New-Object System.Drawing.PointF(560, 85)),
        (New-Object System.Drawing.PointF(670, 60)),
        (New-Object System.Drawing.PointF(850, 65)),
        (New-Object System.Drawing.PointF(1080, 80)),
        (New-Object System.Drawing.PointF(1120, 115)),
        (New-Object System.Drawing.PointF(1080, 170)),
        (New-Object System.Drawing.PointF(1100, 210)),
        (New-Object System.Drawing.PointF(1040, 245)),
        (New-Object System.Drawing.PointF(1015, 320)),
        (New-Object System.Drawing.PointF(950, 330)),
        (New-Object System.Drawing.PointF(925, 280)),
        (New-Object System.Drawing.PointF(865, 295)),
        (New-Object System.Drawing.PointF(815, 320)),
        (New-Object System.Drawing.PointF(780, 270)),
        (New-Object System.Drawing.PointF(730, 245)),
        (New-Object System.Drawing.PointF(680, 220)),
        (New-Object System.Drawing.PointF(630, 160)),
        (New-Object System.Drawing.PointF(580, 145)),
        (New-Object System.Drawing.PointF(550, 110))
    )
    $graphics.FillPolygon($landBrush, $eaPoints)
    $graphics.DrawPolygon($landPen, $eaPoints)

    # 英国・イベリア・アラビア・インド
    $ukPoints = @(
        (New-Object System.Drawing.PointF(535, 135)),
        (New-Object System.Drawing.PointF(565, 140)),
        (New-Object System.Drawing.PointF(545, 175)),
        (New-Object System.Drawing.PointF(515, 170))
    )
    $graphics.FillPolygon($landBrush, $ukPoints)
    $graphics.DrawPolygon($landPen, $ukPoints)

    $indPoints = @(
        (New-Object System.Drawing.PointF(830, 245)),
        (New-Object System.Drawing.PointF(890, 255)),
        (New-Object System.Drawing.PointF(870, 340)),
        (New-Object System.Drawing.PointF(820, 305))
    )
    $graphics.FillPolygon($landBrush, $indPoints)
    $graphics.DrawPolygon($landPen, $indPoints)

    # アフリカ大陸
    $afPoints = @(
        (New-Object System.Drawing.PointF(565, 215)),
        (New-Object System.Drawing.PointF(660, 210)),
        (New-Object System.Drawing.PointF(705, 245)),
        (New-Object System.Drawing.PointF(735, 295)),
        (New-Object System.Drawing.PointF(725, 380)),
        (New-Object System.Drawing.PointF(685, 470)),
        (New-Object System.Drawing.PointF(635, 520)),
        (New-Object System.Drawing.PointF(585, 495)),
        (New-Object System.Drawing.PointF(560, 370)),
        (New-Object System.Drawing.PointF(525, 310)),
        (New-Object System.Drawing.PointF(540, 245))
    )
    $graphics.FillPolygon($landBrush, $afPoints)
    $graphics.DrawPolygon($landPen, $afPoints)

    # 日本列島
    $jpBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(58, 72, 99))
    $jpPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(99, 179, 237), 2)
    $jpPoints = @(
        (New-Object System.Drawing.PointF(1040, 170)),
        (New-Object System.Drawing.PointF(1075, 160)),
        (New-Object System.Drawing.PointF(1090, 180)),
        (New-Object System.Drawing.PointF(1065, 215)),
        (New-Object System.Drawing.PointF(1045, 220)),
        (New-Object System.Drawing.PointF(1025, 195))
    )
    $graphics.FillPolygon($jpBrush, $jpPoints)
    $graphics.DrawPolygon($jpPen, $jpPoints)

    # オーストラリア
    $auPoints = @(
        (New-Object System.Drawing.PointF(970, 390)),
        (New-Object System.Drawing.PointF(1070, 380)),
        (New-Object System.Drawing.PointF(1105, 425)),
        (New-Object System.Drawing.PointF(1100, 495)),
        (New-Object System.Drawing.PointF(1050, 515)),
        (New-Object System.Drawing.PointF(965, 505)),
        (New-Object System.Drawing.PointF(945, 445))
    )
    $graphics.FillPolygon($landBrush, $auPoints)
    $graphics.DrawPolygon($landPen, $auPoints)

    # 海洋ラベリング
    $fontSea = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
    $seaBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(40, 52, 75))
    $graphics.DrawString("PACIFIC OCEAN", $fontSea, $seaBrush, 400, 290)
    $graphics.DrawString("ATLANTIC OCEAN", $fontSea, $seaBrush, 360, 240)
    $graphics.DrawString("INDIAN OCEAN", $fontSea, $seaBrush, 750, 420)

    # 保存
    $dir = Split-Path -Path $outputPath
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }
    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    
    $graphics.Dispose()
    $bitmap.Dispose()
    Write-Host "Base world map created: $outputPath"
}

Create-WorldBaseMap -outputPath "c:\Users\user\OneDrive\ドキュメント\Antigravity\world-building\assets\templates\base_map_world.png"
