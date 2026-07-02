"""グローバル教訓（global_lessons.json）の読み書き。

Reflection で誤診時に追記されたルールを Pre-Consult が参照する。
エントリは Append-only で、無効化は is_active フラグによる論理削除。
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_hospital.config import GLOBAL_LESSONS_PATH


def _load_all(path: Path = GLOBAL_LESSONS_PATH) -> list[dict[str, Any]]:
    """教訓ファイルをすべて読み込む。

    Args:
        path: 読み込み先 JSON ファイル。

    Returns:
        教訓エントリのリスト。ファイルが存在しない場合は空リスト。
    """
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def _save_all(lessons: list[dict[str, Any]], path: Path = GLOBAL_LESSONS_PATH) -> None:
    """教訓リストを JSON ファイルに書き込む。

    Args:
        lessons: 保存する教訓エントリのリスト。
        path: 書き込み先 JSON ファイル。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)


def read_active_lessons(path: Path = GLOBAL_LESSONS_PATH) -> list[dict[str, Any]]:
    """有効な教訓のみ返す。

    Args:
        path: 読み込み先 JSON ファイル。

    Returns:
        is_active が True の教訓エントリのリスト。
    """
    return [lesson for lesson in _load_all(path) if lesson.get("is_active", True)]


def append_lesson(
    rule: str,
    *,
    source_patient: str | None = None,
    path: Path = GLOBAL_LESSONS_PATH,
) -> dict[str, Any]:
    """新しい教訓エントリを追記する。

    Args:
        rule: 教訓の本文（診断ルールなど）。
        source_patient: 教訓の元になった症例 ID。省略可。
        path: 書き込み先 JSON ファイル。

    Returns:
        追加された教訓エントリ。id, rule, source_patient, is_active,
        created_at を含む。
    """
    lessons = _load_all(path)
    entry = {
        "id": f"lesson_{uuid.uuid4().hex[:8]}",
        "rule": rule,
        "source_patient": source_patient,
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    lessons.append(entry)
    _save_all(lessons, path)
    return entry


def deactivate_lesson(lesson_id: str, path: Path = GLOBAL_LESSONS_PATH) -> bool:
    """指定 ID の教訓を論理削除する。

    Args:
        lesson_id: 無効化する教訓の ID。
        path: 書き込み先 JSON ファイル。

    Returns:
        該当エントリが見つかり無効化できた場合 True。それ以外 False。
    """
    lessons = _load_all(path)
    updated = False
    for lesson in lessons:
        if lesson.get("id") == lesson_id and lesson.get("is_active", True):
            lesson["is_active"] = False
            updated = True
    if updated:
        _save_all(lessons, path)
    return updated
