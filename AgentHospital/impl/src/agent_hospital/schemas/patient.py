"""症例マスタの型定義。"""

from typing import Literal, TypedDict

CaseSplit = Literal["train", "test"]
"""症例のデータセット区分。"""


class CaseMaster(TypedDict):
    """storage/patients/patient_xxx.json の症例マスタ。

    consultation_log は含めない（セッション側に保存）。
    """

    patient_id: str
    split: CaseSplit
    chief_complaint: str
    history: str
    exam_results: dict[str, str]
    ground_truth: str
