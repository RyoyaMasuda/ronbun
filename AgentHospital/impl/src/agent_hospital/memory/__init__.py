"""永続化レイヤ（記憶機構）の公開 API。

教訓（lessons）と症例（patients）の読み書き関数を re-export する。
グラフの Python ノードおよび Skills の scripts/ から利用される。
"""

from agent_hospital.memory.lessons import append_lesson, deactivate_lesson, read_active_lessons
from agent_hospital.memory.patients import load_patient, list_patient_ids
from agent_hospital.memory.sessions import append_session_log, finalize_session, start_session

__all__ = [
    "read_active_lessons",
    "append_lesson",
    "deactivate_lesson",
    "load_patient",
    "list_patient_ids",
    "start_session",
    "append_session_log",
    "finalize_session",
]
