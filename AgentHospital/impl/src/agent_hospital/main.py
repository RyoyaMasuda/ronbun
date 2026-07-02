"""Agent Hospital CLI エントリポイント。"""

import argparse
import asyncio

from agent_hospital.graph import build_graph
from agent_hospital.state import new_invocation_state


async def run_graph(patient_id: str) -> None:
    """Strands グラフ全体を非同期実行する。

    Args:
        patient_id: 症例 ID。invocation_state に渡される。
    """
    graph = build_graph()
    invocation_state = new_invocation_state(patient_id)
    task = f"患者 {patient_id} の診察を開始してください。"
    result = await graph.invoke_async(task, invocation_state)
    print(f"status: {result.status}")
    for node_id, node_result in result.results.items():
        print(f"--- {node_id} ---")


def main() -> None:
    """CLI のエントリポイント。"""
    parser = argparse.ArgumentParser(description="Agent Hospital impl")
    parser.add_argument("--patient", default="patient_001", help="症例 ID")
    args = parser.parse_args()
    asyncio.run(run_graph(args.patient))


if __name__ == "__main__":
    main()
