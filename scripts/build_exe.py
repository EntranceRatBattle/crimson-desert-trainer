"""Build a standalone trainer EXE via PyInstaller."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "CrimsonDesertTrainer",
        "--add-data", f"{root / 'crimson_trainer/offsets/manifest.json'};crimson_trainer/offsets",
        "--add-data", f"{root / 'crimson_trainer/config/settings.yaml'};crimson_trainer/config",
        str(root / "crimson_trainer/bootstrap.py"),
    ]
    return subprocess.call(cmd, cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())