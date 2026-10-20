"""Config loader with sensible defaults."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parent / "settings.yaml"


@dataclass
class TrainerConfig:
    version: str
    game_exe: str
    require_admin: bool
    overlay_enabled: bool
    log_level: str


def load_config() -> TrainerConfig:
    raw = yaml.safe_load(CONFIG_PATH.read_text())
    t = raw["trainer"]
    return TrainerConfig(
        version=t["version"],
        game_exe=t["game_exe"],
        require_admin=bool(t["require_admin"]),
        overlay_enabled=bool(raw["overlay"]["enabled"]),
        log_level=raw["logging"]["level"],
    )