"""永続化レイヤ（記憶機構）の公開 API。

教訓（lessons）と症例（patients）の読み書き関数を re-export する。
グラフの Python ノードおよび Skills の scripts/ から利用される。
"""

from agent_hospital.memory.lessons import append_lesson, deactivate_lesson, read_active_lessons
from agent_hospital.memory.patients import append_patient_log, load_patient

__all__ = [
    "read_active_lessons",
    "append_lesson",
    "deactivate_lesson",
    "load_patient",
    "append_patient_log",
]
