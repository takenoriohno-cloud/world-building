---
description: 仕様書（Spec）および実装計画（Plan）を、独立して検証可能な細粒度のタスク一覧に分解するワークフロー
---

# SDD Phase 3: タスク分解ワークフロー (`/sdd:tasks`)

本ワークフローは、確定した仕様書（`specs/`）および実装計画（`plans/`）を基に、順序性・依存関係・検証手順を明記したタスクリストを策定します。

## 実行手順

1. **前提資料の確認**:
   - 対象機能の仕様書（`.specify/specs/<feature_name>.spec.md`）
   - 対象機能の実装計画（`.specify/plans/<feature_name>.plan.md`）
   - 最上位憲章（`.specify/memory/constitution.md`）

2. **タスク分解の原則**:
   - **TDD / 検証ファースト**: 各タスクに「成功判定・検証基準（何を以て完了とするか）」を定義。
   - **依存性の最小化**: 可能な限り独立して進行可能なタスク単位に分割。
   - **並行/直列の明示**: 前提となる設定・ドキュメントの依存関係を可視化。

3. **タスクファイルの出力**:
   - テンプレート（`.specify/templates/tasks_template.md`）に従い、`.specify/tasks/<feature_name>.tasks.md` を作成。

4. **進捗ログの更新**:
   - `doc/current_status.md` のアクティブタスク欄に反映。
