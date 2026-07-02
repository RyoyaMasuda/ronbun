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
from agent_hospital.nodes.patient_env import run_patient_env
from agent_hospital.nodes.pre_consult import run_pre_consult
from agent_hospital.nodes.reflection import run_reflection
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
    result = node.result
    if hasattr(result, "message"):
        blocks = result.message.get("content", []) if isinstance(result.message, dict) else result.message.content
        return " ".join(
            block.get("text", "") if isinstance(block, dict) else getattr(block, "text", "")
            for block in blocks
        )
    return str(result)


def after_interview_to_patient(state: GraphState, *, invocation_state: InvocationState, **kwargs: Any) -> bool:
    """Interview から Patient/Env へ進む条件。

    診断未確定（[DIAGNOSIS: ...] なし）のとき True。確定時は diagnosis を
    invocation_state に書き込み False を返す。

    Args:
        state: グラフ実行中の状態。
        invocation_state: ノード間共有状態。
        **kwargs: Strands から渡される追加引数（未使用）。

    Returns:
        Patient/Env へ遷移する場合 True。
    """
    text = _interview_text(state)
    diagnosis = _extract_diagnosis(text)
    if diagnosis:
        invocation_state["diagnosis"] = diagnosis
        invocation_state["diagnosis_finalized"] = True
        return False
    invocation_state["diagnosis_finalized"] = False
    return True


def after_interview_to_reflection(state: GraphState, *, invocation_state: InvocationState, **kwargs: Any) -> bool:
    """Interview から Reflection へ進む条件。

    Args:
        state: グラフ実行中の状態（本関数では未使用）。
        invocation_state: diagnosis_finalized が True のとき Reflection へ遷移。
        **kwargs: Strands から渡される追加引数（未使用）。

    Returns:
        Reflection へ遷移する場合 True。
    """
    return bool(invocation_state.get("diagnosis_finalized"))


def build_graph():
    """診察ワークフローの Strands グラフを構築する。

    Returns:
        実行可能な Graph インスタンス。エントリポイントは pre_consult。
    """
    builder = GraphBuilder()
    builder.add_node(FunctionNode(run_pre_consult, name="pre_consult"), "pre_consult")
    builder.add_node(FunctionNode(run_patient_env, name="patient_env"), "patient_env")
    builder.add_node(FunctionNode(run_reflection, name="reflection"), "reflection")

    interview: Agent = create_interview_agent()
    builder.add_node(interview, "interview")
    
    builder.add_edge("pre_consult", "interview")
    builder.add_edge("interview", "patient_env", condition=after_interview_to_patient)
    builder.add_edge("patient_env", "interview")
    builder.add_edge("interview", "reflection", condition=after_interview_to_reflection)

    builder.set_entry_point("pre_consult")
    builder.set_max_node_executions(20)
    builder.reset_on_revisit(True)
    return builder.build()
