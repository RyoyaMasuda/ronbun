#!/usr/bin/env python3
"""global-lessons Skill: 有効な教訓を JSON で stdout に出力する。

Interview Agent が shell ツール経由で呼び出す thin wrapper。
内部で agent_hospital.memory.lessons.read_active_lessons を使用する。

Usage:
    python scripts/read_global_lessons.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from agent_hospital.memory.lessons import read_active_lessons  # noqa: E402

if __name__ == "__main__":
    print(json.dumps(read_active_lessons(), ensure_ascii=False, indent=2))
