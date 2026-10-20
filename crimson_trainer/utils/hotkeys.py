"""Global hotkey bindings for toggling cheats without focusing the trainer."""
from __future__ import annotations

import keyboard
from loguru import logger

from crimson_trainer.services.player_service import PlayerService
from crimson_trainer.services.combat_service import CombatService


DEFAULT_BINDINGS = {
    "f1": "godmode",
    "f2": "infinite_stamina",
    "f3": "one_hit",
    "f4": "esp",
}


def register_hotkeys(player: PlayerService, combat: CombatService) -> None:
    keyboard.add_hotkey("f1", lambda: player.toggle_godmode())
    keyboard.add_hotkey("f2", lambda: combat.set_infinite_stamina(not combat.infinite_stamina))
    keyboard.add_hotkey("f3", lambda: combat.toggle_one_hit())
    logger.info("hotkeys registered: {}", list(DEFAULT_BINDINGS.keys()))