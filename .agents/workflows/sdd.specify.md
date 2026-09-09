# ワークフロー: 仕様策定 (/sdd.specify)
<!-- .agents/workflows/sdd.specify.md -->

ユーザーからの新規要件・魔獣生成・ルール追加の要望を受け、`.specify/specs/[機能・魔獣名].md` を起草するワークフロー。

## 実行ステップ
1. **関連資料の全事前チェック**: `constitution.md`, `project-context.md`, `world/*.md`, `doc/questions_and_answers.md` を全走査。
2. **外部科学リサーチ**: `search_web` ツールを用いて、原種生物、銃火器弾道学、地理インフラ、ジビエ法規の現実数値を調査・取得。
3. **仕様書の起草**: `.specify/templates/spec_template.md` に基づき、`.specify/specs/[名称].md` を作成。
4. **憲章適合性チェック**: 6大原則との矛盾がないかを明記。
5. **ユーザー提示**: 作成した仕様書を提示し、レビュー・合意を求める。
