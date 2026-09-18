# 【敵対的独立レビュー書】HIST-REV-[年代]-[識別子]-[担当ペルソナ]

> **レビュー担当**: [レビュー専任ペルソナ名・役職]（Review-Only Agent）  
> **準拠規格**: AWS AIDLC Phase Boundary Review (Adversarial Posture & Checkable Evidence)  
> **査定対象**: `stories.md`, `requirements.md`, `personas.md`  
> **作成日時**: [YYYY-MM-DD HH:MM]  

---

## 1. レビュー判定（Review Verdict）

## Review verdict (READY / NOT-READY)

> ※READY の条件: 下記の敵対的検証項目において、致命的矛盾・憲章違反・未充足要件がゼロ件であり、すべての合格判定に具体的なファイル行番号の証拠（Checkable Evidence）が付与されていること。

---

## 2. 敵対的検証チェックリスト（Adversarial Inspection Checklist）

作成者の主張を鵜呑みにせず、「矛盾・破綻・ご都合主義」を積極的に暴くスタンスで検証する。

### ① 担当領域・専門性監査（Domain Specific Review）
- [ ] **[担当ペルソナ固有の監査項目]**:
  - *検証結果*: PASS / FAIL
  - *具体的証拠（Checkable Evidence）*: `[ファイル名:L行番号]`
  - *指摘・反証事項*: [安易な妥協を排した厳しい技術的・専門的指摘]

### ② 現実史・クロニクル突合監査（Chronicle Consistency）
- [ ] **現実の公式記録との整合性**:
  - *検証結果*: PASS / FAIL
  - *具体的証拠*: `world/history/raw_timeline_1980_2026.json` [該当事件テキスト]
  - *指摘事項*: [現実の出来事の歪曲や年月のズレがないか]

### ③ 最上位憲章・無矛盾性監査（Charter Compliance）
- [ ] **憲章絶対法則（AGENTS.md）との完全一致**:
  - *生体媒介原則（1.2節）*: 電子機器への直接干渉などの違反描写がないか
  - *通常兵器DRバランス（1.3節）*: 物理弾頭や通常火器の有効性が担保されているか
  - *三段階分類法（1.7節）*: Class-A/B/Cの安全・毒性区分が正しく運用されているか
  - *具体的証拠*: `AGENTS.md:L[行番号]` ⇄ `stories.md:L[行番号]`

---

## 3. 敵対的所見・改善要求（Adversarial Findings & Action Items）

| 重要度（Severity） | 指摘内容（Finding） | 是正要求（Required Action） | 対象ストーリーID |
| :--- | :--- | :--- | :--- |
| **BLOCKING / MAJOR / MINOR** | [具体的な論理欠陥・憲章抵触] | [どのように書き換えるべきか] | STO-XX |

---

## 4. 査定者サイン（Reviewer Sign-off）

- **査定者氏名**: [担当ペルソナ名]
- **所属部署**: [担当部署名]
- **最終ステータス**: READY（承認・正史昇格可） / NOT-READY（差戻し・修正要請）
