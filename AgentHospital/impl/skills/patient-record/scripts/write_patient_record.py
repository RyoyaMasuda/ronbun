#!/usr/bin/env python3
"""patient-record Skill: セッション JSON の dialogue に問診ログを追記する。

Interview Agent が shell ツール経由で呼び出す thin wrapper。

Usage:
    python scripts/write_patient_record.py --patient patient_001 --session SESSION_ID --role doctor --text "問診内容"
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from agent_hospital.memory.sessions import append_session_log  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="セッション JSON の dialogue に追記する。")
    parser.add_argument("--patient", required=True, help="症例 ID")
    parser.add_argument("--session", required=True, help="セッション ID")
    parser.add_argument("--role", required=True, help="ログの role（doctor / patient など）")
    parser.add_argument("--text", required=True, help="追記するテキスト")
    args = parser.parse_args()
    append_session_log(args.patient, args.session, {"role": args.role, "text": args.text})
    print("ok")
