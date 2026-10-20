"""Versioned offset table loader with checksum verification."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

OFFSET_DIR = Path(__file__).parent


@dataclass(frozen=True)
class OffsetTable:
    build: str
    player_base: int
    health: int
    stamina: int
    gold: int
    skill_points: int
    entity_list: int
    entity_stride: int
    camera_matrix: int
    checksum: str

    @classmethod
    def load(cls, trainer_version: str) -> "OffsetTable":
        manifest = OFFSET_DIR / "manifest.json"
        data = json.loads(manifest.read_text())
        if trainer_version not in data["compatible"]:
            logger.warning("Trainer {} not listed in manifest compatible set", trainer_version)

        build = data["latest_build"]
        entry = data["builds"][build]
        payload = {k: v for k, v in entry.items() if k != "checksum"}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        if digest != entry["checksum"]:
            raise RuntimeError(f"Offset table checksum mismatch for build {build}")

        return cls(build=build, checksum=digest, **payload)