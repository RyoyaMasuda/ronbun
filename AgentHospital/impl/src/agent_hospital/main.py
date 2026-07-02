"""Agent Hospital CLI エントリポイント。"""

import argparse
import asyncio

from dotenv import load_dotenv

from agent_hospital.config import IMPL_ROOT
from agent_hospital.graph import build_graph
from agent_hospital.memory.patients import list_patient_ids
from agent_hospital.memory.sessions import start_session
from agent_hospital.state import new_invocation_state


async def run_graph(patient_id: str) -> None:
    """Strands グラフ全体を非同期実行する。

    Args:
        patient_id: 症例 ID。invocation_state に渡される。
    """
    graph = build_graph()
    invocation_state = new_invocation_state(patient_id)
    invocation_state["session_id"] = start_session(patient_id)
    task = f"患者 {patient_id} の診察を開始してください。"
    result = await graph.invoke_async(task, invocation_state)
    print(f"status: {result.status}")
    print(f"session: {invocation_state['session_id']}")
    for node_id, node_result in result.results.items():
        print(f"--- {node_id} ---")


async def run_all(patient_ids: list[str]) -> None:
    """複数症例を順に実行する。

    Args:
        patient_ids: 実行する症例 ID のリスト。
    """
    for i, patient_id in enumerate(patient_ids, start=1):
        print(f"\n======== [{i}/{len(patient_ids)}] {patient_id} ========")
        await run_graph(patient_id)


def main() -> None:
    """CLI のエントリポイント。"""
    load_dotenv(IMPL_ROOT / ".env")
    parser = argparse.ArgumentParser(description="Agent Hospital impl")
    parser.add_argument("--patient", default="patient_001", help="症例 ID（単体実行時）")
    parser.add_argument(
        "--list",
        action="store_true",
        help="症例一覧（manifest）を表示",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="manifest の症例をすべて順に実行",
    )
    parser.add_argument(
        "--split",
        choices=["train", "test"],
        help="--list / --all で train または test のみ対象",
    )
    args = parser.parse_args()

    if args.list:
        for pid in list_patient_ids(split=args.split):
            print(pid)
        return

    if args.all:
        patient_ids = list_patient_ids(split=args.split)
        if not patient_ids:
            print("対象症例がありません。")
            return
        asyncio.run(run_all(patient_ids))
        return

    asyncio.run(run_graph(args.patient))


if __name__ == "__main__":
    main()
