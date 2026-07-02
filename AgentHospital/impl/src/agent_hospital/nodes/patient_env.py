"""Patient/Env（患者・環境）ノード。

LLM ベースの患者エージェント。症例 JSON の症状情報をもとにロールプレイし、
医師（Interview）の質問に答える。Strands グラフが直前の interview 出力を入力する。
"""

from typing import Any, cast

from strands import Agent
from strands.multiagent.base import MultiAgentBase, MultiAgentResult, NodeResult, Status

from agent_hospital.memory.patients import append_patient_log, load_patient
from agent_hospital.nodes.text_utils import agent_result_text
from agent_hospital.state import InvocationState


def build_patient_system_prompt(patient: dict[str, Any]) -> str:
    """症例 JSON から患者ロールプレイ用 system_prompt を組み立てる。

    ground_truth（正解病名）は含めない。患者は自覚症状として答える。

    Args:
        patient: load_patient() の戻り値。

    Returns:
        患者 Agent 向け system_prompt。
    """
    exam = patient.get("exam_results", {})
    exam_lines = "\n".join(f"- {key}: {value}" for key, value in exam.items()) or "（なし）"
    return (
        "あなたは医師の診察を受けている患者です。"
        "医師の質問に、自然な日本語で短く答えてください。"
        "病名を自分から断定しないでください（「〜かもしれません」程度は可）。"
        "分からないことは「分かりません」と答えてください。\n\n"
        "あなたが自覚していること:\n"
        f"- いちばん困っていること: {patient.get('chief_complaint', '体調不良')}\n"
        f"- その他の症状・経過: {patient.get('history', '特になし')}\n\n"
        "検査や視診で分かっていること（医師が聞いたときだけ答える）:\n"
        f"{exam_lines}"
    )


class PatientEnvNode(MultiAgentBase):
    """症例に基づく患者 LLM Agent をグラフノードとして実行する。

    Attributes:
        name: グラフ上のノード ID。
    """

    name = "patient_env"

    async def invoke_async(
        self,
        task: Any,
        invocation_state: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> MultiAgentResult:
        """患者 Agent を起動し、医師の問いかけに答える。

        task には Strands が直前の interview 出力などを含めて渡す。

        Args:
            task: グラフから構築された入力（医師の質問を含む）。
            invocation_state: 共有状態。patient_id, turn を参照・更新する。
            **kwargs: Strands から渡される追加引数（未使用）。

        Returns:
            患者の返答を載せた MultiAgentResult。
        """
        state: InvocationState = cast(InvocationState, invocation_state or {})
        patient_id = state.get("patient_id", "patient_001")
        turn = state.get("turn", 0)
        patient = load_patient(patient_id)

        agent = Agent(
            name="patient_env",
            system_prompt=build_patient_system_prompt(patient),
        )
        agent_result = await agent.invoke_async(task, invocation_state)
        reply = agent_result_text(agent_result)

        append_patient_log(patient_id, {"role": "patient", "turn": turn, "text": reply})
        state["turn"] = turn + 1

        node_result = NodeResult(result=agent_result, status=Status.COMPLETED)
        return MultiAgentResult(
            status=Status.COMPLETED,
            results={self.name: node_result},
            execution_count=1,
        )
