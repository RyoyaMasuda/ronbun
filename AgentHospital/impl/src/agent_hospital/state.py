"""グラフ実行中の共有状態（invocation_state）の型定義。

Strands は dict をそのまま渡すため、実行時は通常の dict だが
キーと意味をここで一元管理する。各ノードは同じ dict 参照を読み書きする。
"""

from typing import Any, TypedDict


class LessonEntry(TypedDict, total=False):
    """global_lessons.json の1エントリ。

    Attributes:
        id: 教訓 ID（例: lesson_abc12345）。
        rule: 教訓の本文。
        source_patient: 元になった症例 ID。
        is_active: 有効フラグ。False は論理削除。
        created_at: 作成日時（UTC ISO8601）。
    """

    id: str
    rule: str
    source_patient: str | None
    is_active: bool
    created_at: str


class InvocationStateRequired(TypedDict):
    """診察開始時に必ず存在するフィールド。"""

    patient_id: str
    turn: int


class InvocationState(InvocationStateRequired, total=False):
    """ノード間で共有する invocation_state。

    Strands の graph.invoke_async(task, invocation_state) に渡す dict の型。
    実行を進めるにつれ Pre-Consult / graph 条件 / Reflection がフィールドを追加する。

    Attributes:
        patient_id: 症例 ID（例: patient_001）。main で設定。
        turn: 問診ターン。Patient/Env がログ記録後に increment。
        global_lessons: 有効な教訓一覧。Pre-Consult が設定。
        diagnosis: Interview が出力した病名。graph の条件関数が設定。
        diagnosis_finalized: 診断確定フラグ。graph の条件関数が設定。
        reflection_rule: 誤診時に追記する教訓文。省略時 Reflection が自動生成。
    """

    global_lessons: list[LessonEntry]
    diagnosis: str
    diagnosis_finalized: bool
    reflection_rule: str


def new_invocation_state(patient_id: str, *, turn: int = 0) -> InvocationState:
    """フルグラフ実行用の invocation_state を生成する。

    Args:
        patient_id: 症例 ID。
        turn: 初期ターン。通常 0。

    Returns:
        patient_id と turn のみを持つ InvocationState。
    """
    return {"patient_id": patient_id, "turn": turn}
