# 歴史Inceptionワークフロー (history.inception.md)

本ワークフローは、AWS Labsの **AI-DLC (AI-Driven Development Life Cycle)** アーキテクチャに準拠し、7,039件の現実史クロニクル（`chronology_1980_2026.md`）から魔力覚醒地球の正史エピソードを起草・独立査定・正史統合するための標準運用プロトコルである。

---

## ワークフロー概要図

```
[Stage 1: 要件分析 (Requirements)] ── (現実史クロニクルからTRG抽出・HFR/HNFR策定)
       ▼ output: requirements.md
[Stage 2: ペルソナ策定 (Personas)] ── (当時の当事者アクター・目標・行動・摩擦を定義)
       ▼ output: personas.md
[Stage 3: ストーリー起草 (Stories)] ── (INVEST準拠・Given-When-Then・Mermaid因果図)
       ▼ output: stories.md
[Stage 4: 独立敵対的レビュー (Review)] ── (5専門ペルソナによるReview-Only独立判定)
       ▼ output: review_<persona>.md (READY / NOT-READY)
[Traceability Verification (突合)] ── (verify_history_pipeline.py による三者突合)
       ▼ 100% PASS
【Approval Gate (人間の承認・サインオフ)】 ── (approval.json 発行 ＆ world/history.md 統合)
```

---

## 実行フェーズ詳細

### Stage 1: 要件分析（Requirements Analysis）
- **担当**: 🏛️ 歴史・社会制度考証部（V・シュルツ 特命調査員）
- **テンプレート**: `.specify/templates/history_requirements_template.md`
- **アクション**:
  1. `world/history/raw_timeline_1980_2026.json` より、対象年代の重要事件を「現実史トリガー（TRG-01〜）」として抽出。
  2. 解明すべき歴史的制度・防衛線・メガコーポ利権を「歴史機能要件（HFR-01〜）」として定義。
  3. 最上位憲章（`AGENTS.md`）の制約条件を「非機能要件（HNFR-01〜）」として定義。
  4. 対象ディレクトリ（例: `world/history/stories/<era>/requirements.md`）に出力。

### Stage 2: ペルソナ策定（Personas Formulation）
- **担当**: 🏛️ 歴史・社会制度考証部（V・シュルツ 特命調査員）
- **テンプレート**: `.specify/templates/history_personas_template.md`
- **アクション**:
  1. HFRを体現する当時の当事者（政府高官、自衛隊員、メガコーポ研究員、一般被災者等）を3〜4名選定。
  2. 各ペルソナの目標（Goals）、行動パターン（Actions）、摩擦（Pain Points）を定義。
  3. `world/history/stories/<era>/personas.md` に出力。

### Stage 3: ストーリー起草（User Stories & Acceptance Criteria）
- **担当**: 🏛️ 歴史・社会制度考証部（V・シュルツ 特命調査員）
- **テンプレート**: `.specify/templates/history_story_template.md`
- **アクション**:
  1. 各要件（HFR）をカバーする歴史ストーリー（STO-01〜）を起草。
  2. 構文: `As a [Persona] / When [Trigger] / I had to [Action] / So that [Outcome]`
  3. 各ストーリーに `Given-When-Then` の受け入れ基準および Mermaid因果図を必須配置。
  4. INVEST適合性セルフチェックを行い、`stories.md` に出力。

### Stage 4: 独立敵対的レビュー（Adversarial Review）
- **担当**: 5専門部署（Review-Only Agents、作成権限なし）
  - 🌍 陣内 隆文（軍事・地理） ── `review_jinnai.md`
  - ⚡ クリスティナ・黒田（魔導科学・生体媒介） ── `review_kuroda.md`
  - 🐾 鷹司 冴子（生化学・変異・Class-A/B/C） ── `review_takatsukasa.md`
  - 📸 蓮見 蓮（メディア・市民心理） ── `review_hasumi.md`
  - ⚖️ 首席監査官ゼクスト（最上位憲章無矛盾性） ── `review_zext.md`
- **規約**: `.agents/rules/history_review_rules.md`
- **アクション**:
  1. コンテキストを遮断し、生成された成果物のみを入力として独立査定。
  2. 敵対的スタンスで矛盾・破綻を洗い出し、Checkable Evidence（該当行番号）を明記。
  3. 判定ヘッダー `## Review verdict (READY)` または `NOT-READY` を出力。

### Stage 5: 機械的トレーサビリティ突合チェック（Phase Boundary Verification）
- **コマンド**:
  ```powershell
  & "C:\Program Files\QGIS 3.44.12\apps\Python312\python.exe" engine/history/verify_history_pipeline.py --story-dir "world/history/stories/<era>"
  ```
- **ゲート条件**: 100% PASS（エラー0件）でなければ Gate への進行をブロック。

### Stage 6: Approval Gate ＆ 正史統合（Human Sign-off）
- **アクション**:
  1. ユーザーへ査定結果・検証レポートを提示し、承認（Proceed / Approve）を受領。
  2. `world/history/stories/<era>/approval.json` を発行してスコープを物理凍結。
  3. 承認されたストーリーを `world/history.md` の公式正史年表および個別図鑑記事の遭遇録へ統合。
