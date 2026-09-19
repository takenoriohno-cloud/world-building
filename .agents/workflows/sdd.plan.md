---
description: 合意された仕様書（.specify/specs/*.spec.md）に基づき、実装計画書（.specify/plans/*.plan.md）を作成・承認要請するワークフロー
---

# SDD Phase 2: 実装計画策定ワークフロー (`/sdd.plan`)
<!-- .agents/workflows/sdd.plan.md -->

合意された仕様書（`.specify/specs/*.spec.md`）に基づき、実装計画書（`.specify/plans/*.plan.md`）を作成するワークフロー。

## 1. 前提条件 (Prerequisites)
- Phase 0（仕様書）のユーザー合意が完了していること。

## 2. 実行手順 (Execution Steps)
1. **対象仕様書のロード**:
   - `.specify/specs/[名称].spec.md` の要件とデータ定義を読み込む。
2. **変更・新規ファイルの特定**:
   - 作成・更新する全ファイル（本体ファイル、インデックス、進捗等）を抽出。
3. **計画書の作成（Grepエビデンス付きチェックリスト）**:
   - テンプレート（`.specify/templates/plan_template.md`）に基づき、`.specify/plans/[名称].plan.md` を作成。
   - `.\engine\sdd\run_gate.ps1 -Id <id> -Gate 2` を実行し、全20節見出し網羅、GURPS公式呪文実在性、QGIS定義、6ペルソナ査定が 100% PASS することを確認。
4. **Gate 2（計画承認・ペルソナ査定）の完全展開とユーザー承認要請**:
   - 以下の4大要素をユーザーメッセージ内に**完全展開（Full Disclosure）**して停止（Gate 2 HALT）すること：
     1. **📋 実装計画チェックリスト ＆ 機械的突合エビデンス**: `run_gate.ps1 -Gate 2` の全PASS判定、GURPS公式呪文実在突合行番号、QGIS定義。
     2. **🎭 6専門部署ペルソナ別 INVEST準拠・敵対的査定（Adversarial Review）報告**: 各ペルソナが忖度なく専門領域（解剖学・軍事・法務・魔導力学・メディア・憲章）から計画の欠陥を攻撃し、INVEST原則（Independent, Negotiable, Valuable, Estimable, Small, Testable）に沿って打開案（案A/案B）を提示。
     3. **🧐 曖昧さ・衝突回避の複数選択肢質問（Q1/Q2: A/B/C/X）**: 主級Alpha、メガコーポ動態等の設計分岐点の提示（※選択肢IDは必ずアルファベットに統一）。
     4. **★ ユーザーからの計画着工承認（Proceed）の受領待ち停止（HALT）**: 質問への回答と着工承認を同一視せず、明示的な着工承認を待つ。
5. **Gate 2 承認トークン発行**:
   - ユーザーから計画着工承認（Proceed）を受領後、`.\engine\sdd\run_gate.ps1 -Id <id> -Step gate2 -Approve -Notes "..."` で承認トークン（`gate2.json`）を発行。

## 3. 完了条件 (Done Definition)
- `run_gate.ps1 -Gate 2` が 100% PASS し、Gate 2 完全展開を経てユーザーの明示的承認（Proceed）を得て `.specify/approvals/<id>_gate2.json` が発行されていること。

## 4. 次フェーズへの移行 (Next Phase Handoff)
- Gate 2 承認トークン確認後、**Phase 5-A: QGISタクティカルマップ生成** を実行し、直後に **【Gate 2.5: QGIS画像目視承認（QGIS HALT）】** で停止する（※トークンが無い場合は物理ブロック）。


