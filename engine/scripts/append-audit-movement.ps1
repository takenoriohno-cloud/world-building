# -*- coding: utf-8 -*-
# append-audit-movement.ps1

$auditPath = ".\doc\audit.log"

$entry = @"

### 74. 【2026-09-16】移動系呪文（61種）の過不足なき収集・詳細取得と公式アーカイブ（movement.md）完全補完
- **ユーザー指示**: 移動系呪文が足りていないため、Seesaa Wiki（EUC-JP）の移動系呪文ページ（https://seesaawiki.jp/mokugyo/d/%b0%dc%c6%b0%b7%cf%bc%f6%ca%b8）を参照し、リンク先の各呪文詳細まで取得して過不足なく反映すること。
- **対応と反映**:
  1. **EUC-JP対応クローラー開発・実行（engine/scripts/crawl_movement_spells.py）**:
     - Seesaa Wiki固有のEUC-JPエンコーディングを自動判別・デコードし、ハングを回避するurllib/HTMLParserパイプラインを構築。
     - 一覧表からリンク先URLを再帰的に巡回し、全61種の呪文詳細テキスト、詠唱時間、消費エネルギー、持続時間、前提条件、魔化データを網羅的に抽出・保存（scratch/movement_spells_data.json）。
  2. **移動系呪文アーカイブの完全再編成（world/magic/spells/movement.md）**:
     - 旧来の12呪文から、以下の全61種へと約5倍の大幅拡張を実施：
       - ① ガープス第4版『魔法大全』基本移動系呪文：48種（《韋駄天》《念動》《べたべた》《つるつる》《浮揚》《飛行術*》《瞬間移動*》《瞬間回避》等）
       - ② 複合・環境適応移動系呪文：1種（《樹上駆け》［植物移動系］）
       - ③ 魔導兵器・砲兵戦術拡張呪文（MAS/MDS）：7種（《衝突場*》《魔法の巨拳*》《飛ぶ剣舞*》《連鎖球*》《即落*》《内部攪拌*》《四つ裂き*》）
       - ④ 日常・民間簡単呪文（The Least of Spells）：6種（《見当識》（並）《工芸補助》（並）《クッション》（並）《疾走》（並）《開扉》（並）《沈ませ》（並））
     - 前提条件ツリー（Mermaidフローチャート）および2026年現代戦術・法規制（CR4・SAT三次元立体機動・メガコーポ軍事特許）の考証を完備。
  3. **管理ドキュメント同期**:
     - doc/current_status.md の呪文アーカイブ行を更新（全28系統・ファイル、移動系61種完全補完）。
- **ステータス**: **移動系呪文アーカイブ拡充完了 (Done)**
"@

[System.IO.File]::AppendAllText($auditPath, $entry, [System.Text.Encoding]::UTF8)
Write-Host "audit.log successfully updated."
