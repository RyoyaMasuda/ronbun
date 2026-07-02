"""症例 JSON（patients/patient_xxx.json）の読み込み。

症例マスタは chief_complaint / ground_truth など静的フィールドのみ。
問診ログは memory/sessions.py に保存する。
"""

import json
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
    """症例マスタ JSON を読み込む。

    Args:
        patient_id: 症例 ID。

    Returns:
        症例マスタ。chief_complaint, ground_truth, split などを含む。

    Raises:
        FileNotFoundError: 症例ファイルが存在しない場合。
        json.JSONDecodeError: JSON の形式が不正な場合。
    """
    path = patient_path(patient_id)
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def list_patient_ids(*, split: str | None = None) -> list[str]:
    """manifest.json から症例 ID 一覧を返す。

    Args:
        split: "train" / "test" で絞り込み。None なら全件。

    Returns:
        patient_id のリスト。
    """
    manifest_path = PATIENTS_DIR / "manifest.json"
    with manifest_path.open(encoding="utf-8") as f:
        manifest = json.load(f)
    cases = manifest["cases"]
    if split:
        cases = [c for c in cases if c.get("split") == split]
    return [c["patient_id"] for c in cases]
