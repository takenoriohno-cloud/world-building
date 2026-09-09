# ワークフロー: 矛盾検知・すり合わせ (/sdd.clarify)
<!-- .agents/workflows/sdd.clarify.md -->

仕様書策定中または実装前に、既存設定・憲章・確定Q&Aとの矛盾や曖昧さを検知した際に発動する即時停止（HALT）ワークフロー。

## 実行ステップ
1. **即時停止（HALT）**: 自己判断での処理継続を即座に中止。
2. **すり合わせドキュメントの起草**: `.specify/templates/clarify_template.md` に基づき、論点・衝突箇所・選択肢（A, B, C... + 自由回答X）を作成。
3. **ログへの先行記録**: 質問をユーザーに提示する段階で、`doc/audit.log`（および `doc/questions_and_answers.md` の審議中セクション）に記録。
4. **ユーザーへのタグ付き提示**: `[Q: A]` フォーマットで回答を仰ぐ。
5. **回答の正史反映**: ユーザーからの回答を得た後、決定理由を `doc/questions_and_answers.md` に正式記録。
