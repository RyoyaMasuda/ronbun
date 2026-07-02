"""Pre-Consult（診察前準備）ノード。

診察開始前に有効なグローバル教訓を読み込み、invocation_state に載せる。
"""

from typing import Any

from agent_hospital.memory.lessons import read_active_lessons
from agent_hospital.state import InvocationState


def run_pre_consult(task: Any, invocation_state: InvocationState) -> str:
    """有効な教訓を invocation_state に載せ、要約を返す。

    Args:
        task: グラフから渡されるタスク（本ノードでは未使用）。
        invocation_state: 共有状態。patient_id を読み、global_lessons を書き込む。

    Returns:
        Pre-Consult の実行結果テキスト。患者 ID と教訓一覧を含む。
    """
    lessons = read_active_lessons()
    invocation_state["global_lessons"] = lessons
    patient_id = invocation_state.get("patient_id", "patient_001")
    summary = "\n".join(f"- {item['rule']}" for item in lessons) or "（教訓なし）"
    return f"[Pre-Consult] patient={patient_id}\n教訓:\n{summary}"
