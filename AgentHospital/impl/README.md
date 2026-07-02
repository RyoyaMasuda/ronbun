# Agent Hospital — impl

論文 Agent Hospital の小規模再現。Strands `GraphBuilder` + Agent Skills + JSON 記憶。

## 構成

```
impl/
├── docs/                 # 設計ドキュメント（data-design.md など）
├── src/agent_hospital/   # Python（グラフ・ノード・記憶ロジック）
├── skills/               # Agent Skills（SKILL.md + scripts/）
└── storage/              # 実行時データ（教訓・症例 JSON）
```

設計のたたき台: [docs/data-design.md](docs/data-design.md)

## セットアップ（初回だけ）

```bash
cd impl
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env   # AOAI の値を編集
```

| 変数 | 説明 |
|------|------|
| `AZURE_OPENAI_ENDPOINT` | `https://YOUR_RESOURCE.openai.azure.com` |
| `AZURE_OPENAI_API_KEY` | API キー |
| `AZURE_OPENAI_DEPLOYMENT` | デプロイ名 |

## 実行

```bash
# activate 済みなら
agent-hospital --patient patient_001

# activate なし
impl/.venv/bin/agent-hospital --patient patient_001

agent-hospital --list              # 症例一覧
agent-hospital --all               # 20件すべて
agent-hospital --all --split train # 訓練15件のみ
agent-hospital --all --split test  # テスト5件のみ
```

`pip install -e .` 済みなら CWD 不問。`.env` は `impl/.env` を自動読込。

症例データ: `storage/patients/`（20件: train 15 + test 5）。詳細は [docs/data-design.md](docs/data-design.md)。

## ワークフロー

```
Pre-Consult → Interview ⇄ Patient/Env → Reflection
```

- **Pre-Consult / Reflection** — Python ノード（`FunctionNode`）
- **Interview / Patient/Env** — Strands `Agent`（Patient/Env は症例 JSON でロールプレイ）
