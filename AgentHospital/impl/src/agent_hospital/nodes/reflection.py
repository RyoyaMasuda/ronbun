"""Reflection（反省）ノード。

Interview で確定した診断と症例の正解（ground_truth）を比較し、
結果を consultation_log に記録する。誤診時は global_lessons に教訓を追記する。
"""

from typing import Any

from agent_hospital.memory.lessons import append_lesson
from agent_hospital.memory.patients import append_patient_log, load_patient
from agent_hospital.state import InvocationState


def run_reflection(task: Any, invocation_state: InvocationState) -> str:
    """診断結果を正解と比較し、必要なら教訓を追加する。

    Args:
        task: グラフから渡されるタスク（本ノードでは未使用）。
        invocation_state: 共有状態。patient_id, diagnosis, reflection_rule を参照。

    Returns:
        Reflection の実行結果テキスト。正解/誤診と追加した教訓 ID を含む。
    """
    patient_id = invocation_state.get("patient_id", "patient_001")
    patient = load_patient(patient_id)
    ground_truth = patient["ground_truth"]
    diagnosis = invocation_state.get("diagnosis", "未診断")
    correct = diagnosis.strip() == ground_truth.strip()

    append_patient_log(
        patient_id,
        {
            "role": "reflection",
            "diagnosis": diagnosis,
            "ground_truth": ground_truth,
            "correct": correct,
        },
    )

    if correct:
        return f"[Reflection] 正解 ({ground_truth})"

    rule = invocation_state.get(
        "reflection_rule",
        f"{patient.get('chief_complaint', '')} のパターンでは {ground_truth} を疑う",
    )
    entry = append_lesson(rule, source_patient=patient_id)
    return f"[Reflection] 誤診 ({diagnosis} != {ground_truth})。教訓追加: {entry['id']}"
