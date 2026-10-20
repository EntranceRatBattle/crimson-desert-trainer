"""Entry point — wires services together and starts the GUI."""
from __future__ import annotations

import sys
from loguru import logger

from crimson_trainer.process.attach import GameProcess
from crimson_trainer.offsets.loader import OffsetTable
from crimson_trainer.services.player_service import PlayerService
from crimson_trainer.services.combat_service import CombatService
from crimson_trainer.services.world_service import WorldService
from crimson_trainer.overlay.esp_overlay import EspOverlay
from crimson_trainer.ui.trainer_window import TrainerWindow


class TrainerApp:
    def __init__(self) -> None:
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        logger.add("logs/trainer.log", rotation="2 MB", level="DEBUG")

        self.process = GameProcess("CrimsonDesert.exe")
        self.offsets = OffsetTable.load(__import__("crimson_trainer").__version__)

    def run(self) -> None:
        if not self.process.attach():
            logger.error("Could not attach to CrimsonDesert.exe — is the game running as Admin?")
            return

        logger.info("Attached to PID {}", self.process.pid)
        player = PlayerService(self.process, self.offsets)
        combat = CombatService(self.process, self.offsets)
        world = WorldService(self.process, self.offsets)
        overlay = EspOverlay(self.process, self.offsets)

        TrainerWindow(player=player, combat=combat, world=world, overlay=overlay).mainloop()


def main() -> None:
    TrainerApp().run()


if __name__ == "__main__":
    main()