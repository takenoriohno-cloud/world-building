---
description: すり合わせ決定事項、対話履歴、変更経緯をドキュメントに永続記録し、将来の公式参照元として確定するワークフロー
---

# SDD Phase 6: 監査・永続化ワークフロー (`/sdd.audit`)
<!-- .agents/workflows/sdd.audit.md -->

本ワークフローは、ユーザーとの対話、すり合わせ（Clarify）の採択結果、および実装完了した仕様を正式な正史エビデンスとしてドキュメントに永続記録します。

## 1. 前提条件 (Prerequisites)
- Phase 5（実装）および Phase 4（品質ゲート）の完了、またはすり合わせ（Phase 1）のユーザー回答完了。

## 2. 実行手順 (Execution Steps)
1. **決定事項の記録 (`doc/questions_and_answers.md`)**:
   - 審議が完了したQ&Aアイテムを「解決済み・決定事項」セクションへ移動。
   - 採択された選択肢（A/B/C/X）と理由、関連仕様書へのリンクを明記。
2. **対話・監査ログの追記 (`doc/audit.log`)**:
   - 日時、論点、提案した選択肢、ユーザーの回答、影響範囲、変更ファイルを時系列で追記。
3. **進捗状況の更新 (`doc/current_status.md`)**:
   - 完了したマイルストーン、現在のステータス、次回のアクティブタスクを同期更新。
4. **仕様書・タスクステータスの更新**:
   - 仕様書（`specs/*.spec.md`）のステータスを `[実装完了]` に更新。

## 3. 完了条件 (Done Definition)
- `doc/questions_and_answers.md`, `doc/audit.log`, `doc/current_status.md` がすべて最新状態に更新されていること。

## 4. 次フェーズへの移行 (Next Phase Handoff)
- 本サイクルの完了をユーザーに報告し、次の要望や新機能の **Phase 0: 仕様策定 (`/sdd.specify`)** へ繋げる。
