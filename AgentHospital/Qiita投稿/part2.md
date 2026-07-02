# Part 2 — ミニ版構築（8〜10章）

> 本ファイルは **Part 2** です。Part 1（論文解説）の続きから読んでください。Part 3 以降は別ファイルで執筆します。

---

## 8. ミニ版 Agent Hospital の設計

論文を丸ごと再現するのではなく、**診察 → 正誤判定 → 反省 → 経験蓄積** のコアだけを切り出します。MedQA の数値再現ではなく、ワークフローと記憶更新を体感するのが目的です。

### 8-1. 再現する部分 / 省略する部分

| 論文の要素 | ミニ版 |
|---|---|
| 問診・診断・反省・経験蓄積 | **再現** |
| 患者の症状・検査結果・正誤判定 | **簡略再現**（症例 JSON + ルール） |
| トリアージ・看護師・32 診療科・患者自動生成 | **省略** |
| embedding 検索（Naive RAG） | **省略** → Skills でファイル読み書き |

研究・学習用であり、診断支援・実臨床用途は想定していません。

### 8-2. スコープとワークフロー

| 項目 | 仮置き |
|---|---|
| 疾患 | 1〜3 種 |
| 症例数 | 訓練 10〜30 / テスト 5〜10 |
| LLM | 未確定（API 経由） |

1 回の診察が完結するフローに絞ります。実装では次の **4 ノード**（処理の塊）に分けます。英語名はコード上の識別子です。

| ノード名 | 意味 | 種類 |
|---|---|---|
| **Pre-Consult** | **診察前準備** — 過去の教訓を読み込む | Python |
| **Interview** | **問診・診断** — 医師エージェントが質問・検査指示・診断 | LLM |
| **Patient/Env** | **患者・環境** — 症状や検査結果を返す | Python or LLM |
| **Reflection** | **反省** — 正解と比較し、教訓を追記 | Python + LLM |

```
診察前準備 → 問診・診断 ⇄ 患者・環境 → 反省
(Pre-Consult)  (Interview)  (Patient/Env)  (Reflection)
```

`Interview` と `Patient/Env` は問診が終わるまで往復し、診断が確定したら `Reflection` へ進みます。制御は **AWS Strands** の `GraphBuilder`（有向グラフ）に任せます。

### 8-3. 技術スタック

- **Strands + GraphBuilder** — ワークフローを明示（LangChain 等は使わない）
- **記憶** — `storage/` に JSON、`skills/` に Agent Skills 形式（`SKILL.md` + `scripts/`）
- **正誤判定** — 症例 JSON の `ground_truth` と照合（論文シミュレータの簡略版）

---

## 9. 実装

### 9-1. 各ノードの処理

1. **Pre-Consult（診察前準備）** — `global-lessons` Skill を有効化し、教訓を読み込んでプロンプトに載せる
2. **Interview（問診・診断）** — 教訓を踏まえて質問・検査指示。必要なら `patient-record` Skill でカルテ追記
3. **Patient/Env（患者・環境）** — 手書きの症例 JSON から症状・検査結果を返す（まずはルールベース）
4. **Reflection（反省）** — 誤診なら原因分析 → `global-lessons` Skill で教訓を追記

論文の症例ベース / 経験ベースの二系統は、ミニ版では **`global_lessons.json` に一本化**しています。

### 9-2. 記憶を Skills 形式で置く

**データ**（`storage/`）と**読み書きの手順**（`skills/`）を分けます。Strands の Agent Skills 形式では、各 Skill はディレクトリ + `SKILL.md`（YAML frontmatter + 本文）+ 任意の `scripts/` です。起動時は `name` / `description` だけプロンプトに載り、必要になったら Skill を有効化して本文・スクリプトを使います。

```
skills/
├── global-lessons/          # 共通教訓
│   ├── SKILL.md
│   └── scripts/
│       ├── read_global_lessons.py
│       └── update_global_lessons.py
└── patient-record/          # 個別カルテ
    ├── SKILL.md
    └── scripts/
        └── write_patient_record.py

storage/                     # データ本体（Skills の scripts から読み書き）
├── doctor/global_lessons.json
└── patients/patient_001.json
```

`global-lessons/SKILL.md` の例：

```markdown
---
name: global-lessons
description: 過去の診察教訓を読み書きする。診察前の読み込みと、反省後の追記で使う。
allowed-tools: read_global_lessons update_global_lessons
---

# 共通教訓ノート

- `scripts/read_global_lessons.py` — `is_active: true` のエントリだけ返す
- `scripts/update_global_lessons.py` — 追記。古いルールは `is_active: false` で論理削除
```

| Skill | いつ | 触るファイル |
|---|---|---|
| `global-lessons` | Pre-Consult / Reflection | `doctor/global_lessons.json` |
| `patient-record` | Interview 中/後 | `patients/patient_xxx.json` |

Naive RAG（ベクトル DB に載せて一括検索）ではなく、**Skill を通じてファイルを能動的に読み書きする**形です。

### 9-3. つまずきそうな点

- **ループ終了** —「診断した」発言だけでは曖昧。構造化出力 or ツールで確定させる
- **教訓の肥大化** — Append-only なので矛盾ルールの整理が必要
- **コスト** — 1 症例あたり複数ターンの API 呼び出し

---

## 10. 動かしてみた結果

> 実装・実験の進行に合わせて追記予定。現時点は評価の枠だけ。

**見る指標**：診断正答率、`global_lessons` の件数、問診ターン数。訓練前（教訓なし）と後で同じテストセットを比較する。

**具体例**：（追記予定）失敗 → 反省 → 類似症例で成功、など 1〜2 件。

**論文との主な差分**：患者は手書き JSON、経験は embedding 検索ではなくファイル直読み、規模は数十症例。Part 3 で持ち帰りたいのは「グラフでフローを切る」「失敗をファイルに残す」という設計感です。

---

## 次へ

続きは **Part 3**（ミニ版から RAG チャットへ — 何が活かせるか）です。

---

## 本 Part の参考

- Part 1 — 論文解説
- `実装検討.txt` — Strands / GraphBuilder / 記憶設計
