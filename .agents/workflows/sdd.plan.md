# ワークフロー: 実装計画策定 (/sdd.plan)
<!-- .agents/workflows/sdd.plan.md -->

合意された仕様書（`.specify/specs/*.md`）に基づき、実装計画書（`.specify/plans/*.md`）を作成するワークフロー。

## 実行ステップ
1. **対象仕様書のロード**: `.specify/specs/[名称].md` の要件とデータ定義を読み込む。
2. **変更ファイル抽出**: 新規作成ファイル、更新ファイル（インデックス、ステータス等）を特定。
3. **計画書の作成**: `.specify/templates/plan_template.md` に基づき、`.specify/plans/[名称].md` を出力。
4. **ユーザー承認要請**: 実装計画をユーザーに提示し、承認（Proceed）を得る。
