"""Agent Hospital 実装のパス定数。

impl/ ルートから storage/ と skills/ への絶対パスを定義する。
"""

from pathlib import Path

IMPL_ROOT = Path(__file__).resolve().parents[2]
"""impl/ ディレクトリの絶対パス。"""

STORAGE_ROOT = IMPL_ROOT / "storage"
"""実行時データ（教訓・症例 JSON）のルート。"""

SKILLS_ROOT = IMPL_ROOT / "skills"
"""Agent Skills（SKILL.md + scripts/）のルート。"""

GLOBAL_LESSONS_PATH = STORAGE_ROOT / "doctor" / "global_lessons.json"
"""医師のグローバル教訓ファイル。"""

PATIENTS_DIR = STORAGE_ROOT / "patients"
"""症例 JSON（patient_xxx.json）のディレクトリ。"""

SESSIONS_DIR = STORAGE_ROOT / "sessions"
"""診察セッション JSON のディレクトリ。"""
