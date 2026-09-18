---
description: 承認された仕様書（Spec）およびタスク（Tasks）に基づき、図鑑記事や設定ファイルを厳密に生成・執筆するワークフロー
---

# SDD Phase 5: 実装・生成ワークフロー (`/sdd.implement`)
<!-- .agents/workflows/sdd.implement.md -->

本ワークフローは、事前承認された仕様書（`specs/`）およびタスクリスト（`tasks/`）に基づき、図鑑記事（`creatures/*.md`）や世界設定資料（`world/*.md`）の実装・生成を行います。

## 1. 前提条件 (Prerequisites)
- Gate 2 承認トークン（`.specify/approvals/<feature_name>_gate2.json`）の実在が確認されていること（`run_gate.ps1 -Id <id> -Gate 2 -Assert`）。

## 2. 実行手順 (Execution Steps)

### Phase 5-A: QGIS タクティカルマップ生成 ＆ 機械的停止（Gate 2.5）
1. **オンデマンド・タイル取得（外部通信窓口）**:
   - `fetch_map_tiles.py` を `BypassSandbox: true` で単独実行し、対象BBOXのベースマップタイルをローカルにキャッシュ（同時にEPSG:3857ワールドファイル `.pgw`/`.prj` を自動生成）。
2. **ネットワーク遮断の機械的検証（セキュリティゲート）**:
   - 直ちに標準サンドボックス（`BypassSandbox: false`）にて `assert_network_isolated.py` を実行。
   - 外部通信が100%遮断されていることを機械的に確認（PASSするまでレンダリングおよび後続処理を物理ブロック）。
3. **オフライン QGIS タクティカルマップ自動レンダリング**:
   - サンドボックス内（`BypassSandbox: false`）にて `engine/gis/generate_tactical_map.py` を実行。内部でも再度遮断確認が行われた上で完全オフライン描画される。
4. **機械的画像バリデータ実行**:
   - `.\engine\sdd\run_gate.ps1 -Id <id> -Step qgis` を実行し、ファイル実在、容量 > 100KB、PNGバイナリ整合性、ネットワーク遮断を確認。
5. **★【Gate 2.5: QGIS画像目視承認（QGIS HALT）】**:
   - **生成されたマップ画像をメッセージ内に提示し、機械的に作業を停止（HALT）すること**。
   - ユーザーに一次生息地・国内隔離施設のBBOX、ポリゴン、文字、レイアウトの目視確認を要請。
6. **QGIS 承認トークン発行**:
   - ユーザーからの画像承認（Proceed）を受領後、`.\engine\sdd\run_gate.ps1 -Id <id> -Step qgis -Approve -Notes "..."` を実行。

### Phase 5-B: 3大写真アセット生成 ＆ 本稿執筆
1. **QGIS 承認トークンの確認**:
   - `.\engine\sdd\run_gate.ps1 -Id <id> -Step qgis -Assert` を実行し、承認を確認（未承認時は物理ブロック）。
2. **3大写真アセット生成**:
   - 野生生態観測写真、標本マクロ写真、料理写真（Class-A/B）を生成し配備。
3. **図鑑記事執筆（TEMPLATE.md 全9章全20節）**:
   - 仕様書とテンプレートに定義された全項目を一切の省略なく記述。
   - Mermaid構造図における記号エスケープと高コントラスト暗色規格（`color:#ffffff`）を徹底。
   - 全6専門ペルソナ脚注の配備。
4. **タスク進捗更新**:
   - タスクファイル（`tasks/*.tasks.md`）の完了チェック。

## 3. 完了条件 (Done Definition)
- QGISマップ目視承認（`qgis.json`）が完了し、3大写真および本稿記事が作成され、タスクが完了していること。

## 4. 次フェーズへの移行 (Next Phase Handoff)
- 実装完了後、自動的に **Phase 6: 監査・永続化ワークフロー (`/sdd.audit`)** へ移行する。

