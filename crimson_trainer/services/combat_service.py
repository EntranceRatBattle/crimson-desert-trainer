"""Combat cheats — infinite stamina, damage multiplier, one-hit mode."""
from __future__ import annotations

from loguru import logger

from crimson_trainer.process.attach import GameProcess
from crimson_trainer.offsets.loader import OffsetTable


class CombatService:
    def __init__(self, process: GameProcess, offsets: OffsetTable) -> None:
        self.process = process
        self.offsets = offsets
        self.infinite_stamina = False
        self.damage_multiplier = 1.0
        self.one_hit = False

    def _base(self) -> int:
        return self.process.base + self.offsets.player_base

    def tick(self) -> None:
        if self.infinite_stamina:
            self.process.write_float(self._base() + self.offsets.stamina, 100.0)
        if self.one_hit:
            self.damage_multiplier = 9999.0

    def set_infinite_stamina(self, enabled: bool) -> None:
        self.infinite_stamina = enabled
        logger.info("infinite_stamina = {}", enabled)

    def set_damage_multiplier(self, mult: float) -> None:
        self.damage_multiplier = max(1.0, min(mult, 9999.0))
        logger.info("damage_multiplier = {}", self.damage_multiplier)

    def toggle_one_hit(self) -> bool:
        self.one_hit = not self.one_hit
        logger.info("one_hit = {}", self.one_hit)
        return self.one_hit