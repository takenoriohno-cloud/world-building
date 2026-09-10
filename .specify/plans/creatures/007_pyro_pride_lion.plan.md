# 実装計画書 (Implementation Plan)
<!-- .specify/plans/creatures/007_pyro_pride_lion.plan.md -->

# 【実装計画】第007号：陽炎巨鬣獅 パイロ・プライド・ライオン (Pyro-Pride Lion)

- **対象仕様書**: `[.specify/specs/creatures/007_pyro_pride_lion.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/007_pyro_pride_lion.spec.md)`
- **作成日**: 2026-09-10
- **ステータス**: 計画承認

---

## 1. 実装アプローチ概要
1. **視覚アセットの生成（Phase 5.1）**:
   - `generate_image` を使用し、サバンナで熱波を纏いプライドを率いる雄獅子の生態写真（`pyro_lion_wild.jpg`）および赤熱する鬣のケラチン繊維マクロ写真（`pyro_lion_mane_macro.jpg`）を生成・`assets/creatures/007_pyro_pride_lion/` に配備。
2. **Mermaid構造図の設計（Phase 5.2）**:
   - 生体熱励起・解剖連関図（`flowchart TD` / `subgraph`）
   - プライド戦術包囲狩猟・サバンナ食物連鎖図（`flowchart LR` / `TD`）
3. **図鑑記事の完全執筆（Phase 5.3）**:
   - `TEMPLATE.md` 準拠（全8章構成）。
   - GURPS 4thデータブロック（SM +1 / ST 24, DX 13, HT 12, HP 28, DR 8/4, FP 16 / 《蜃気楼》《火球》《熱気》）。
   - 音響分析（4.3節: 18Hz〜120Hz インフラサウンド・低周波咆哮、120dB）。
   - Class-Bジビエ解体手順（太陽熱嚢・火炎腺摘出プロトコル）と素材利用（耐熱鬣毛皮）。
4. **品質ゲート検査と監査記録（Phase 5.4 / 6）**:
   - 6大部署・憲章整合性チェック。
   - `doc/questions_and_answers.md`（Q15）および `doc/audit.log` の更新。
