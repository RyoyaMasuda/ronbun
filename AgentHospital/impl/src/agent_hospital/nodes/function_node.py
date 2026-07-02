"""Strands GraphBuilder 用の Python 関数ノードラッパー。

同期 Python 関数を MultiAgentBase として包み、AgentResult 形式で返す。
Pre-Consult / Patient/Env / Reflection ノードで使用する。
"""

from typing import Any, Callable, cast

from strands.agent.agent_result import AgentResult
from strands.multiagent.base import MultiAgentBase, MultiAgentResult, NodeResult, Status
from strands.telemetry.metrics import EventLoopMetrics
from strands.types.content import ContentBlock, Message

from agent_hospital.state import InvocationState

NodeFunc = Callable[[Any, InvocationState], str]


class FunctionNode(MultiAgentBase):
    """Python 関数を Strands グラフノードとして実行する。

    Attributes:
        func: 実行する同期関数。
        name: グラフ上のノード ID。
    """

    def __init__(self, func: NodeFunc, name: str | None = None) -> None:
        """FunctionNode を初期化する。

        Args:
            func: (task, invocation_state) -> str 形式の同期関数。
            name: ノード名。省略時は func.__name__ を使用。
        """
        super().__init__()
        self.func = func
        self.name = name or func.__name__

    async def invoke_async(
        self,
        task: Any,
        invocation_state: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> MultiAgentResult:
        """関数を実行し、Strands の MultiAgentResult を返す。

        Args:
            task: グラフから渡されるタスク文字列。
            invocation_state: ノード間で共有する状態辞書（InvocationState として扱う）。
            **kwargs: Strands から渡される追加引数（未使用）。

        Returns:
            func の戻り値を AgentResult.message に載せた MultiAgentResult。
        """
        state: InvocationState = cast(InvocationState, invocation_state or {})
        text = self.func(task, state)
        agent_result = AgentResult(
            stop_reason="end_turn",
            message=Message(role="assistant", content=[ContentBlock(text=text)]),
            metrics=EventLoopMetrics(),
            state={},
        )
        node_result = NodeResult(
            result=agent_result,
            status=Status.COMPLETED,
        )
        return MultiAgentResult(
            status=Status.COMPLETED,
            results={self.name: node_result},
            execution_count=1,
        )
