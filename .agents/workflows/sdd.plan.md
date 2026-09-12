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
   - 章節タイトル、ファイルパス、および `grep_search` による呪文・生体異能・ルールの客観的エビデンスを明記してチェック（`[x]`）する。
4. **監査承認（Gate 2）およびユーザー承認要請**:
   - 憲章監査室が全チェック項目の適合性を検証（PASS）した上で、ユーザーからの承認を得る。


## 3. 完了条件 (Done Definition)
- 実装計画書が作成され、ユーザーの承認（Proceed）を得ていること。

## 4. 次フェーズへの移行 (Next Phase Handoff)
- 実装計画の承認後、直ちに **Phase 3: タスク分解ワークフロー (`/sdd.tasks`)** を実行する。
