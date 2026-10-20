"""World manipulation — teleport, time-of-day, free camera."""
from __future__ import annotations

from loguru import logger

from crimson_trainer.process.attach import GameProcess
from crimson_trainer.offsets.loader import OffsetTable


class WorldService:
    def __init__(self, process: GameProcess, offsets: OffsetTable) -> None:
        self.process = process
        self.offsets = offsets
        self.free_camera = False

    def teleport(self, x: float, y: float, z: float) -> None:
        base = self.process.base + self.offsets.player_base
        # position triple lives right before the health block in Crimson Desert
        pos = base + self.offsets.health - 12
        self.process.write_float(pos, x)
        self.process.write_float(pos + 4, y)
        self.process.write_float(pos + 8, z)
        logger.info("teleport -> ({:.1f}, {:.1f}, {:.1f})", x, y, z)

    def set_time_of_day(self, hour: float) -> None:
        clamped = max(0.0, min(hour, 24.0))
        addr = self.process.base + self.offsets.camera_matrix + 0x40
        self.process.write_float(addr, clamped)
        logger.debug("time_of_day -> {}", clamped)

    def toggle_free_camera(self) -> bool:
        self.free_camera = not self.free_camera
        logger.info("free_camera = {}", self.free_camera)
        return self.free_camera