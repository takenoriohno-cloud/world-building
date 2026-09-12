---
description: 仕様書策定中または実装前・実装中に、既存設定・憲章・確定Q&Aとの矛盾や曖昧さを検知した際に発動する即時停止（HALT）ワークフロー
---

# SDD Phase 1: 矛盾検知・すり合わせワークフロー (`/sdd.clarify`)
<!-- .agents/workflows/sdd.clarify.md -->

仕様書策定中または実装前・実装中に、既存設定・憲章・確定Q&Aとの矛盾や曖昧さを検知した際に発動する即時停止（HALT）ワークフロー。

## 1. 前提条件 (Prerequisites)
- 矛盾・設定衝突、または意図しない設定削除・短縮リスクの検知。

## 2. 実行手順 (Execution Steps)
1. **即時停止（HALT）**:
   - 自己判断での推測や作業継続を即座に中止する。
2. **すり合わせドキュメントの起草**:
   - テンプレート（`.specify/templates/clarify_template.md`）に基づき、論点・衝突箇所・選択肢（A, B, C... + 自由回答X）を作成。
3. **ログへの先行記録（義務）**:
   - ユーザーに質問を提示する段階で、`doc/audit.log` および `doc/questions_and_answers.md` の「審議中セクション」に先行記録する。
4. **ユーザーへのタグ付き提示**:
   - `[Q: A]` フォーマットで選択肢を提示し、回答・指示を仰ぐ。
5. **回答の正史エビデンス化**:
   - ユーザー回答を得た後、決定理由と採択結果を `doc/questions_and_answers.md` の「解決済みセクション」および `doc/audit.log` に正式登録。

## 3. 完了条件 (Done Definition)
- ユーザーからの回答が得られ、`questions_and_answers.md` および `audit.log` に正史エビデンスとして記録されていること。

## 4. 次フェーズへの移行 (Next Phase Handoff)
- 矛盾解消後、中断していた元のフェーズ（Phase 0: Spec / Phase 2: Plan / Phase 5: Implement 等）へ復帰し作業を再開する。
