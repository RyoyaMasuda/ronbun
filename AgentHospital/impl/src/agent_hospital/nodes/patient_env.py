"""Patient/Env（患者・環境）ノード。

症例 JSON からルールベースで患者の返答を生成し、consultation_log に追記する。
Interview との問診ループで turn ごとに主訴 → 既往 → 検査結果を返す。
"""

from typing import Any

from agent_hospital.memory.patients import append_patient_log, load_patient
from agent_hospital.state import InvocationState


def run_patient_env(task: Any, invocation_state: InvocationState) -> str:
    """症例 JSON から患者の返答を生成する。

    turn 0: chief_complaint
    turn 1: history
    turn 2+: exam_results

    Args:
        task: グラフから渡されるタスク（本ノードでは未使用）。
        invocation_state: 共有状態。patient_id, turn を読み書きする。

    Returns:
        Patient/Env の実行結果テキスト。患者の返答を含む。
    """
    patient_id = invocation_state.get("patient_id", "patient_001")
    patient = load_patient(patient_id)
    turn = invocation_state.get("turn", 0)

    if turn == 0:
        reply = patient.get("chief_complaint", "症状を訴えます。")
    elif turn == 1:
        reply = patient.get("history", "特記事項はありません。")
    else:
        exam = patient.get("exam_results", {})
        reply = "検査結果: " + ", ".join(f"{k}={v}" for k, v in exam.items())

    append_patient_log(patient_id, {"role": "patient", "turn": turn, "text": reply})
    invocation_state["turn"] = turn + 1
    return f"[Patient/Env] {reply}"
