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

## セットアップ

```bash
cd impl
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 実行

```bash
agent-hospital --patient patient_001
```

要 LLM（AWS Bedrock または OpenAI 等の設定）。

## ワークフロー

```
Pre-Consult → Interview ⇄ Patient/Env → Reflection
```

- **Pre-Consult / Reflection** — Python ノード（`FunctionNode`）
- **Interview / Patient/Env** — Strands `Agent`（Patient/Env は症例 JSON でロールプレイ）
