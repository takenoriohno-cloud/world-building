# 【タスク一覧】第12号エントリー 樹皮小人ボウトラックル 新規格（全9章）再構築

- **対象仕様書**: `[.specify/specs/creatures/012_wood_bowtruckle_refactor.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/012_wood_bowtruckle_refactor.spec.md)`
- **対象計画書**: `[.specify/plans/012_wood_bowtruckle_refactor.plan.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/plans/012_wood_bowtruckle_refactor.plan.md)`
- **作成フェーズ**: Phase 3: Tasks
- **作成日**: 2026-09-12
- **ステータス**: 完了 (Done)

---

## 1. 依存関係順タスクリスト

- [x] **Task 1: 【視覚アセット生成】野生写真・木質爪標本・クラフトジン料理写真の生成・配備**
  - `generate_image` を活用し、以下の3画像を生成して `assets/creatures/012_wood_bowtruckle/` に配備完了。
    1. `wood_bowtruckle_wild.jpg`: 古代イングリッシュオーク樹皮と同化した野生成体（全高18cm、若葉頭部、木質棘爪）の生態ドキュメンタリー写真。
    2. `wood_bowtruckle_claw.jpg`: 採取された前肢木質棘爪（Spur Claws / モース硬度4.5、リグニン結晶構造）の顕微鏡マクロ標本写真。
    3. `wood_bowtruckle_cuisine.jpg`: **【料理写真】英国最高級クラフトジン「ドライアドズ・バウ（Dryad's Bough）」のアンティーク角瓶ボトル＆ボタニカルハーブティーのスタジオ写真**。
  - **検証基準**: 3画像が正しく生成・配置され、クォータエラーがないことを確認。

- [x] **Task 2: 【図鑑記事完全リライト】新規格全9章構成による `012_wood_bowtruckle.md` の刷新**
  - `TEMPLATE.md` の全9章構成を完全網羅して執筆完了。
    - 第1章: 生物学的分類階級（節足動物門 / 昆虫綱 / ナナフシ目 / 樹守科 / ボウトラックル属 / 樹皮小人種）、学名語源。
    - 第2章: ケルト神話のドルイド聖樹信仰・オガム文字・グリーンマン伝承の原典調査と、2000年マナ覚醒後の植物節足キメラ化の科学的架橋。
    - 第3章: 幼体・成熟成体・Elder Alpha（樹齢200年巨木共生・体高30cm・DR 5）の3段階ライフステージ、Mermaid生体解剖図（`flowchart TD / subgraph`）。
    - 第4章: 宿主樹木活性化・キクイムシ捕食・害鳥集団防衛クロスリレーション、Mermaid生態系図（`flowchart LR`）。
    - 第5章: 《樹木同化》《植物交信》の魔導力学、音響ログ（32〜52kHz超音波クリック音、5〜15Hz樹液流動超低周波）、上位神格グリーンマン霊的交信。
    - 第6章: GURPS 4th Stat Block（成熟成体＆Elder Alpha）、英国王立森林局（DEFRA）推奨ゴーグルプロトコル、林業マタギ燻煙コラム。
    - 第7章: Class-B、クラフトジン「ドライアドズ・バウ」減圧蒸留レシピ、ハーブティー、料理写真埋め込み、精密工学素材価値。
    - 第8章: コーンウォール州森林警備隊無線交信ログおよび森林局注意報。
    - 第9章: 参考文献・典拠資料。
  - **検証基準**: 全9章が漏れなく完成し、Mermaid構文エラーがなく、画像リンクが正常であることを確認。

- [x] **Task 3: 【管理ドキュメント同期・監査更新】**
  - `doc/current_status.md`、`doc/audit.log` を最新状態に同期。
  - **検証基準**: 状態が完了（Done）として正確に記録されていること。
