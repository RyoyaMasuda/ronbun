"""診察セッション JSON の読み書き。

1回の agent-hospital 実行ごとに storage/sessions/{patient_id}/{session_id}.json を作成する。
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from agent_hospital.config import SESSIONS_DIR


def _session_path(patient_id: str, session_id: str) -> Path:
    return SESSIONS_DIR / patient_id / f"{session_id}.json"


def start_session(patient_id: str, *, doctor_id: str = "doctor_001") -> str:
    """新しい診察セッションファイルを作成する。

    Args:
        patient_id: 症例 ID。
        doctor_id: 医師 ID。

    Returns:
        生成した session_id（タイムスタンプ + 短い UUID）。
    """
    now = datetime.now(timezone.utc)
    session_id = f"{now.strftime('%Y%m%dT%H%M%S')}_{uuid4().hex[:6]}"
    path = _session_path(patient_id, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = {
        "session_id": session_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "started_at": now.isoformat(),
        "dialogue": [],
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return session_id


def append_session_log(patient_id: str, session_id: str, entry: dict[str, Any]) -> None:
    """セッション JSON の dialogue にエントリを追記する。

    Args:
        patient_id: 症例 ID。
        session_id: セッション ID。
        entry: 追記するログ。at（UTC ISO8601）が自動付与される。
    """
    path = _session_path(patient_id, session_id)
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("dialogue", []).append({**entry, "at": datetime.now(timezone.utc).isoformat()})
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def finalize_session(
    patient_id: str,
    session_id: str,
    *,
    diagnosis: str,
    ground_truth: str,
    correct: bool,
) -> None:
    """Reflection 完了時にセッションに診断結果を書き込む。

    Args:
        patient_id: 症例 ID。
        session_id: セッション ID。
        diagnosis: 医師の診断。
        ground_truth: 正解病名。
        correct: 正誤。
    """
    path = _session_path(patient_id, session_id)
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    data.update(
        {
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "diagnosis": diagnosis,
            "ground_truth": ground_truth,
            "correct": correct,
        }
    )
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
