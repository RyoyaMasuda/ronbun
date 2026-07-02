"""Agent Hospital 診察ワークフローの Strands グラフ定義。

Pre-Consult → Interview ⇄ Patient/Env → Reflection のフローを GraphBuilder で構築する。
Interview 出力の [DIAGNOSIS: 病名] で Patient/Env と Reflection の分岐を制御する。
"""

import re
from typing import Any

from strands import Agent
from strands.multiagent import GraphBuilder
from strands.multiagent.graph import GraphState

from agent_hospital.nodes.function_node import FunctionNode
from agent_hospital.nodes.interview import create_interview_agent
from agent_hospital.nodes.patient_env import PatientEnvNode
from agent_hospital.nodes.pre_consult import run_pre_consult
from agent_hospital.nodes.reflection import run_reflection
from agent_hospital.nodes.text_utils import agent_result_text
from agent_hospital.state import InvocationState


def _extract_diagnosis(text: str) -> str | None:
    """Interview 出力から [DIAGNOSIS: 病名] を抽出する。

    Args:
        text: Interview Agent の応答テキスト。

    Returns:
        抽出した病名。マーカーがなければ None。
    """
    match = re.search(r"\[DIAGNOSIS:\s*(.+?)\]", text, re.IGNORECASE)
    return match.group(1).strip() if match else None


def _interview_text(state: GraphState) -> str:
    """GraphState から Interview ノードのテキスト出力を取得する。

    Args:
        state: グラフ実行中の状態。results に interview ノード結果を含む。

    Returns:
        Interview の応答テキスト。ノード未実行時は空文字。
    """
    node = state.results.get("interview")
    if not node:
        return ""
    return agent_result_text(node)


def _update_diagnosis_state(state: GraphState, invocation_state: InvocationState) -> bool:
    """Interview の出力を読み、invocation_state の診断フラグを更新する。

    Args:
        state: グラフ実行中の状態。
        invocation_state: ノード間共有状態。

    Returns:
        [DIAGNOSIS: 病名] が見つかり診断確定した場合 True。
    """
    diagnosis = _extract_diagnosis(_interview_text(state))
    if diagnosis:
        invocation_state["diagnosis"] = diagnosis
        invocation_state["diagnosis_finalized"] = True
        return True
    invocation_state["diagnosis_finalized"] = False
    return False


def needs_patient_response(
    state: GraphState, *, invocation_state: InvocationState, **kwargs: Any
) -> bool:
    """Interview 後に patient_env へ進むか。

    医師がまだ質問中（[DIAGNOSIS: ...] なし）→ True → 患者の返答を取りに行く。

    Returns:
        patient_env へ進む場合 True。
    """
    return not _update_diagnosis_state(state, invocation_state)


def ready_for_reflection(
    state: GraphState, *, invocation_state: InvocationState, **kwargs: Any
) -> bool:
    """Interview 後に reflection へ進むか。

    医師が診断確定（[DIAGNOSIS: ...] あり）→ True → 振り返りへ進む。

    Returns:
        reflection へ進む場合 True。
    """
    return _update_diagnosis_state(state, invocation_state)


def build_graph():
    """診察ワークフローの Strands グラフを構築する。

    Returns:
        実行可能な Graph インスタンス。エントリポイントは pre_consult。
    """
    builder = GraphBuilder()

    builder.add_node(FunctionNode(run_pre_consult, name="pre_consult"), "pre_consult")
    builder.add_node(PatientEnvNode(), "patient_env")
    builder.add_node(FunctionNode(run_reflection, name="reflection"), "reflection")

    interview: Agent = create_interview_agent()
    builder.add_node(interview, "interview")

    builder.add_edge("pre_consult", "interview")

    # Interview の直後は2択。condition が True のエッジだけ通る（同時には両方通らない）。
    #
    #   Interview の出力                    → 次に動くノード
    #   ─────────────────────────────────────────────────────
    #   「いつから痛みますか？」など          → patient_env（患者の返答）
    #   「…[DIAGNOSIS: 帯状疱疹]」と確定     → reflection（正誤判定）
    builder.add_edge("interview", "patient_env", condition=needs_patient_response)
    builder.add_edge("interview", "reflection", condition=ready_for_reflection)

    # patient_env の次は必ず interview（患者の返答をもとに、医師が続きの質問をする）
    builder.add_edge("patient_env", "interview")

    builder.set_entry_point("pre_consult")
    builder.set_max_node_executions(20)
    builder.reset_on_revisit(True)
    return builder.build()
