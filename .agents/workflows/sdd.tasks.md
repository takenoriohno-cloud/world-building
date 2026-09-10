---
description: 仕様書（Spec）および実装計画（Plan）を、独立して検証可能な細粒度のタスク一覧に分解するワークフロー
---

# SDD Phase 3: タスク分解ワークフロー (`/sdd.tasks`)
<!-- .agents/workflows/sdd.tasks.md -->

本ワークフローは、確定した仕様書（`specs/`）および実装計画（`plans/`）を基に、順序性・依存関係・検証手順を明記したタスクリストを策定します。

## 1. 前提条件 (Prerequisites)
- 対象機能の仕様書（`.specify/specs/<feature_name>.spec.md`）
- 対象機能の実装計画（`.specify/plans/<feature_name>.plan.md`）
- 最上位憲章（`.specify/memory/constitution.md` / `AGENTS.md`）

## 2. 実行手順 (Execution Steps)
1. **タスク分解の原則適用**:
   - **TDD / 検証ファースト**: 各タスクに「検証基準（何を以て完了とするか）」を定義。
   - **依存性の最小化**: 可能な限り独立して進行可能なタスク単位に分割。
   - **並行/直列の明示**: 前提となる設定・ドキュメントの依存関係を可視化。
2. **タスクファイルの出力**:
   - テンプレート（`.specify/templates/tasks_template.md`）に従い、`.specify/tasks/<feature_name>.tasks.md` を作成。
3. **進捗ログの初期登録**:
   - `doc/current_status.md` のアクティブタスク欄に反映。

## 3. 完了条件 (Done Definition)
- タスクファイルが生成され、`current_status.md` に反映されていること。

## 4. 次フェーズへの移行 (Next Phase Handoff)
- タスク一覧の策定後、直ちに **Phase 5: 実装・生成ワークフロー (`/sdd.implement`)** へ移行し、定義順にタスクを実行する。
