"""症例 JSON（patients/patient_xxx.json）の読み書き。

症例の静的データ（主訴・正解など）の読み込みと、
consultation_log への問診・Reflection 履歴の追記を行う。
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_hospital.config import PATIENTS_DIR


def patient_path(patient_id: str) -> Path:
    """症例 ID から JSON ファイルパスを返す。

    Args:
        patient_id: 症例 ID（例: patient_001）。

    Returns:
        storage/patients/{patient_id}.json の Path。
    """
    return PATIENTS_DIR / f"{patient_id}.json"


def load_patient(patient_id: str) -> dict[str, Any]:
    """症例 JSON を読み込む。

    Args:
        patient_id: 症例 ID。

    Returns:
        症例データ。chief_complaint, ground_truth, consultation_log などを含む。

    Raises:
        FileNotFoundError: 症例ファイルが存在しない場合。
        json.JSONDecodeError: JSON の形式が不正な場合。
    """
    path = patient_path(patient_id)
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def append_patient_log(patient_id: str, entry: dict[str, Any]) -> None:
    """consultation_log にエントリを追記する。

    Args:
        patient_id: 症例 ID。
        entry: 追記するログ。role, text など任意のフィールドを含む。
            保存時に at（UTC ISO8601）が自動付与される。

    Raises:
        FileNotFoundError: 症例ファイルが存在しない場合。
    """
    path = patient_path(patient_id)
    data = load_patient(patient_id)
    logs = data.setdefault("consultation_log", [])
    logs.append({**entry, "at": datetime.now(timezone.utc).isoformat()})
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
