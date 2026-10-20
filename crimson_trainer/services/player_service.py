"""Player stats: health, stamina, gold, skill points."""
from __future__ import annotations

from dataclasses import dataclass
from loguru import logger

from crimson_trainer.process.attach import GameProcess
from crimson_trainer.offsets.loader import OffsetTable


@dataclass
class PlayerStats:
    health: float
    stamina: float
    gold: int
    skill_points: int


class PlayerService:
    def __init__(self, process: GameProcess, offsets: OffsetTable) -> None:
        self.process = process
        self.offsets = offsets
        self._godmode = False

    @property
    def _base(self) -> int:
        return self.process.base + self.offsets.player_base

    def read_stats(self) -> PlayerStats:
        b = self._base
        return PlayerStats(
            health=self.process.read_float(b + self.offsets.health),
            stamina=self.process.read_float(b + self.offsets.stamina),
            gold=self.process.read_int(b + self.offsets.gold),
            skill_points=self.process.read_int(b + self.offsets.skill_points),
        )

    def set_health(self, value: float) -> None:
        self.process.write_float(self._base + self.offsets.health, value)
        logger.debug("health -> {}", value)

    def set_gold(self, value: int) -> None:
        self.process.write_int(self._base + self.offsets.gold, max(0, value))

    def toggle_godmode(self, enabled: bool | None = None) -> bool:
        self._godmode = (not self._godmode) if enabled is None else enabled
        if self._godmode:
            self.set_health(9999.0)
        logger.info("godmode = {}", self._godmode)
        return self._godmode

    def tick(self) -> None:
        if self._godmode:
            self.set_health(9999.0)