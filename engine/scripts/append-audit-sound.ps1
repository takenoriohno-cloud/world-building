# -*- coding: utf-8 -*-
# append-audit-sound.ps1

$auditPath = ".\doc\audit.log"

$entry = @"

### 75. 【2026-09-16】音声系呪文（38種）の過不足なき収集・詳細取得と公式アーカイブ（sound.md）完全補完
- **ユーザー指示**: 音声系呪文も不足があるため、Seesaa Wiki（EUC-JP）の音声系呪文ページ（https://seesaawiki.jp/mokugyo/d/%b2%bb%c0%bc%b7%cf%bc%f6%ca%b8）を参照し、リンク先の各呪文詳細まで取得して過不足なく再編成すること。
- **対応と反映**:
  1. **EUC-JP対応クローラー開発・実行（engine/scripts/crawl_sound_spells.py）**:
     - Seesaa Wiki固有のEUC-JPエンコーディングを自動デコードし、ハングを回避しながら全38種の呪文詳細テキスト、詠唱時間、消費エネルギー、持続時間、前提条件、魔化データを網羅的に抽出・保存（scratch/sound_spells_data.json）。
  2. **音声系呪文アーカイブの完全再編成（world/magic/spells/sound.md）**:
     - 旧来の12呪文から、以下の全38種へと3倍以上に大幅拡張：
       - ① ガープス第4版『魔法大全』基本音声系呪文：28種（《作音》《感覚鋭敏化》《沈黙》《超音波視覚》《雷鳴》《発声》《不明瞭》《擬声》《沈黙障壁》《静寂》《忍び足》《拡声》《騒音》《遅発伝言》《防音》《音噴射》《爆裂衝球》《密談》《遠耳》《筆記》《採譜》《伝言》《魔法の口》《声変え》《銀の舌》《残響再現》《魔法の耳》《透明な耳》）
       - ② 魔導兵器・音響戦術拡張呪文（MAS/MDS）：5種（《強化爆裂衝球*》《致傷振動圏*》《破肉の叫び*》《破壊振動*》《死の声がけ*》）
       - ③ 日常・民間簡単呪文（The Least of Spells）：5種（《ペット呼び》（並）《音害微減》（並）《きしみ音》（並）《投げ声》（並）《水中会話術》（並））
     - 高コントラスト仕様Mermaid前提条件ツリー（ダークスレート背景×鮮明シアン枠×純白文字）を配備。
     - 2026年現代戦術・対魔獣音響兵器（LRAD・スクリーム作戦）、メガコーポ情報保全（CR2防音二重ガラス・科捜研残響再現捜査）、国際規制（CR4非人道音響兵器）の考証を完備。
  3. **管理ドキュメント同期**:
     - doc/current_status.md の呪文アーカイブ行を更新（全28系統・ファイル、移動系61種・音声系38種完全補完）。
- **ステータス**: **音声系呪文アーカイブ拡充完了 (Done)**
"@

[System.IO.File]::AppendAllText($auditPath, $entry, [System.Text.Encoding]::UTF8)
Write-Host "audit.log successfully updated with sound spells entry."
