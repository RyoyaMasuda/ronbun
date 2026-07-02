"""AgentResult / Message からテキストを取り出すユーティリティ。"""

from typing import Any


def agent_result_text(result: Any) -> str:
    """Agent または NodeResult のテキスト出力を取得する。

    Args:
        result: AgentResult、NodeResult、または message 属性を持つオブジェクト。

    Returns:
        連結したテキスト。取得できなければ str(result)。
    """
    if hasattr(result, "result"):
        result = result.result
    if not hasattr(result, "message"):
        return str(result)
    message = result.message
    blocks = message.get("content", []) if isinstance(message, dict) else message.content
    return " ".join(
        block.get("text", "") if isinstance(block, dict) else getattr(block, "text", "")
        for block in blocks
    ).strip()
