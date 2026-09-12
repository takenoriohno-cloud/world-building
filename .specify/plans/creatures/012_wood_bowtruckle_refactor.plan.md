# 【実装計画】第12号エントリー 樹皮小人ボウトラックル 新規格（全9章）再構築

- **対象仕様書**: `[.specify/specs/creatures/012_wood_bowtruckle_refactor.spec.md](file:///c:/Users/user/OneDrive/ドキュメント/Antigravity/world-building/.specify/specs/creatures/012_wood_bowtruckle_refactor.spec.md)`
- **作成フェーズ**: Phase 2: Plan
- **作成日**: 2026-09-12
- **ステータス**: 承認待ち（Gate 2）

---

## 1. 提案アプローチと変更の概要

新・高規格図鑑テンプレート（`TEMPLATE.md`）に基づき、第12号ボウトラックル（*Dendrophasma britannicum*）を全9章構成で完全リライトします。

### ■ 主な実装ポイント
1. **第1章（基本分類・メタデータ）**:
   - 生物学的分類階級（節足動物門 / 昆虫綱 / ナナフシ目 / 樹守科 / ボウトラックル属 / 樹皮小人種）および学名語源を完全明記。
2. **第2章（伝承考証とマナ覚醒の架橋）**:
   - ケルト神話のドルイド聖樹信仰・オガム文字・グリーンマン伝承の原典調査と、2000年マナ覚醒後の植物節足キメラ化の科学的架橋。
3. **第3章（生物学的特徴・ライフステージ）**:
   - 幼体（2〜5cm）→ 成熟成体（15〜22cm）→ **古樹共生個体（Elder Alpha / 樹齢200年巨木共生・体高30cm・DR 5）**の3段階。
   - Mermaid生体解剖器官連関図（`flowchart TD / subgraph`）。
4. **第4章（生態・食物連鎖・相互作用）**:
   - 宿主樹木活性化・キクイムシ捕食・害鳥集団防衛のクロスリレーションとMermaid生態系図（`flowchart LR`）。
5. **第5章（魔導科学・上位神性・背景ロア）**:
   - 《樹木同化》《植物交信》のパッシブ魔導力学。
   - 音響ログ（32〜52kHz超音波クリック音、5〜15Hz樹液流動超低周波共振）。
   - 上位神格「グリーンマン（Green Man）」霊的交信および英国メガコーポ蒸留所経済。
6. **第6章（交戦マニュアル・都市防災コラム）**:
   - GURPS 4th Stat Block（成熟成体 SM -4 / ST 1, DX 15, IQ 6, HT 11, HP 4, DR 3、Elder Alpha SM -3 / ST 3, DX 16, IQ 8, HT 13, HP 8, DR 5）。
   - 英国王立森林局（DEFRA）推奨「密閉ゴーグル着用プロトコル」および林業マタギ「ユーカリスモーカー忌避コラム」。
7. **第7章（解体・ジビエ食文化・料理レシピ）**:
   - Class-B（要処理種 / 粗繊維のため肉食用不可・生薬および蒸留原料）。
   - **最高級クラフトジン「ドライアドズ・バウ（Dryad's Bough）」減圧蒸留レシピ**および「ケルティック・ウッド・インフュージョン」ハーブティー。
   - **【料理写真】（Cuisine Photo）の生成・配備**。
8. **第8章（現場記録・通信ログ）**:
   - コーンウォール州森林警備隊・密猟者摘発現場ログおよび森林局注意報。
9. **第9章（参考文献・典拠資料）**:
   - ケルト樹木民俗誌、昆虫解剖学、英国蒸留酒基準等の学術出典。

---

## 2. 変更・新規作成ファイル一覧

### 【視覚アセット生成】
- `assets/creatures/012_wood_bowtruckle/wood_bowtruckle_wild.jpg`: 野生成態写真
- `assets/creatures/012_wood_bowtruckle/wood_bowtruckle_claw.jpg`: 木質爪マクロ標本写真
- `assets/creatures/012_wood_bowtruckle/wood_bowtruckle_cuisine.jpg`: **【料理写真】クラフトジン「ドライアドズ・バウ」ボトル＆ハーブティー**

### 【図鑑記事リライト】
- `creatures/012_wood_bowtruckle.md`: 新規格全9章構成への完全刷新

### 【管理ドキュメント同期】
- `doc/current_status.md`: 第12号の最新ステータス更新
- `doc/audit.log`: SDD作業ログの記録

---

## 3. 品質ゲート・憲章整合性検証（Analyze Checklist）
- [x] 最上位憲章 `AGENTS.md`（第4.1節・新規格全9章＆料理写真義務）と100%整合しているか。
- [x] 生体媒介原則・非電磁干渉（Q2）、三段階法制分類（Q3: Class-B）、ガープス基準（Q6）と完全合致しているか。
- [x] 画像相対パスが `../assets/creatures/012_wood_bowtruckle/...` で正しく設計されているか。
