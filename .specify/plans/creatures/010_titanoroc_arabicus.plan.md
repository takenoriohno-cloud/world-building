# 実装計画書 (Implementation Plan)
<!-- .specify/plans/creatures/010_titanoroc_arabicus.plan.md -->

# 【実装計画】第010号：砂嵐巨怪鳥 ロック (Titanoroc / Al-Rukh)

- **対象仕様書**: `[.specify/specs/creatures/010_titanoroc_arabicus.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/010_titanoroc_arabicus.spec.md)`
- **作成日**: 2026-09-10
- **ステータス**: 計画承認

---

## 1. 実装アプローチ概要
1. **視覚アセットの生成（Phase 5.1）**:
   - `generate_image` を使用し、中東の砂漠霊峰上空を巨大な砂嵐を伴って飛翔する巨怪鳥の生態写真（`roc_wild_photo.jpg`）およびチタンケラチン羽軸・鉤爪マクロ写真（`roc_quill_macro.jpg`）を生成・`assets/creatures/010_titanoroc_arabicus/` に配備。
2. **Mermaid構造図の設計（Phase 5.2）**:
   - 超巨大猛禽航空生体力学・器官構造図（`flowchart TD` / `subgraph`）
   - 砂嵐突風包囲・落下粉砕狩猟＆国際航空防空回廊図（`flowchart TD` / `LR`）
3. **図鑑記事の完全執筆（Phase 5.3）**:
   - `TEMPLATE.md` 準拠（全8章構成）。
   - GURPS 4thデータブロック（SM +4 / ST 52, DX 13, HT 14, HP 60, DR 12 / 飛翔 Move 25 / 150km/h, FP 22 / 《突風》《砂嵐》《風壁》《超音速降下》）。
   - 音響分析（4.3節: 翼ばたき低周波インフラサウンド 12〜35Hz、130dB裂帛の怪鳥咆哮）。
   - Class-C軍事マテリアル（次世代魔導戦闘機用超高強度羽軸・防護シールド卵殻）の記述。
4. **品質ゲート検査と監査記録（Phase 5.4 / 6）**:
   - 6大部署・憲章整合性チェック。
   - `doc/questions_and_answers.md`（Q18）および `doc/audit.log` の更新。
