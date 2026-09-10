---
description: ユーザー要件・魔獣生成・ルール追加を受け、外部調査と憲章整合性を踏まえた仕様書（Spec）を起草するワークフロー
---

# SDD Phase 0: 仕様策定ワークフロー (`/sdd.specify`)
<!-- .agents/workflows/sdd.specify.md -->

ユーザーからの新規要件・魔獣生成・ルール追加の要望を受け、`.specify/specs/[機能・魔獣名].spec.md` を起草するワークフロー。

## 1. 前提条件 (Prerequisites)
- 関連資料（`constitution.md`, `project-context.md`, `world/*.md`, `doc/questions_and_answers.md`）の事前全走査。

## 2. 実行手順 (Execution Steps)
1. **外部科学リサーチ（グラウンディング義務）**:
   - `search_web` ツールを用いて、原種生物データ（骨格・咬合力・感染症）、銃火器弾道データ（初速・運動エネルギーJ）、実在地理・法規データを調査。
2. **仕様書の起草**:
   - テンプレート（`.specify/templates/spec_template.md`）に基づき、`.specify/specs/[名称].spec.md` を作成。
3. **5専門部署チェックマトリクスの適用**:
   - 生物・地理・社会・魔導理論・憲章監査の全5観点から整合性を検証。
4. **矛盾・曖昧さのハンドリング**:
   - 既存設定との衝突が検知された場合は即座に `/sdd.clarify`（HALT）を発動。

## 3. 完了条件 (Done Definition)
- 外部科学データと5部署チェックを含む仕様書ドラフトが作成され、ユーザーに提示されていること。

## 4. 次フェーズへの移行 (Next Phase Handoff)
- ユーザーから仕様書への合意・承認が得られた場合、自動的に **Phase 2: 実装計画策定 (`/sdd.plan`)** および **Phase 3: タスク分解 (`/sdd.tasks`)** へ移行する。
