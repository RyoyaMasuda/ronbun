#!/usr/bin/env python3
"""global-lessons Skill: 教訓の追記・論理削除を行う。

Interview Agent が shell ツール経由で呼び出す thin wrapper。
内部で agent_hospital.memory.lessons を使用する。

Usage:
    python scripts/update_global_lessons.py --rule "ルール文" [--source-patient ID] [--deactivate lesson_xxx]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from agent_hospital.memory.lessons import append_lesson, deactivate_lesson  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="グローバル教訓を追記する。--deactivate で既存エントリを無効化可能。",
    )
    parser.add_argument("--rule", required=True, help="追加する教訓の本文")
    parser.add_argument("--source-patient", default=None, help="教訓の元症例 ID")
    parser.add_argument("--deactivate", default=None, help="無効化する lesson id")
    args = parser.parse_args()

    if args.deactivate:
        deactivate_lesson(args.deactivate)
    entry = append_lesson(args.rule, source_patient=args.source_patient)
    print(json.dumps(entry, ensure_ascii=False, indent=2))
