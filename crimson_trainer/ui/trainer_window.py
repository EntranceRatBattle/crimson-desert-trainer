"""CustomTkinter trainer window — thin controller delegating to services."""
from __future__ import annotations

import customtkinter as ctk
from loguru import logger

from crimson_trainer.services.player_service import PlayerService
from crimson_trainer.services.combat_service import CombatService
from crimson_trainer.services.world_service import WorldService
from crimson_trainer.overlay.esp_overlay import EspOverlay

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class TrainerWindow(ctk.CTk):
    def __init__(
        self,
        player: PlayerService,
        combat: CombatService,
        world: WorldService,
        overlay: EspOverlay,
    ) -> None:
        super().__init__()
        self.player, self.combat, self.world, self.overlay = player, combat, world, overlay
        self.title("Crimson Desert Trainer v1.4.2")
        self.geometry("520x640")

        self._section("Player")
        self.godmode_btn = ctk.CTkSwitch(self, text="Godmode", command=self._toggle_godmode)
        self.godmode_btn.pack(pady=4, padx=20, anchor="w")

        self._section("Combat")
        self.stamina_btn = ctk.CTkSwitch(self, text="Infinite Stamina", command=self._toggle_stamina)
        self.stamina_btn.pack(pady=4, padx=20, anchor="w")
        self.onehit_btn = ctk.CTkSwitch(self, text="One-Hit Mode", command=self.combat.toggle_one_hit)
        self.onehit_btn.pack(pady=4, padx=20, anchor="w")

        self._section("Overlay")
        self.esp_btn = ctk.CTkButton(self, text="Toggle ESP", command=self._toggle_esp)
        self.esp_btn.pack(pady=8, padx=20, anchor="w")

        self.status = ctk.CTkLabel(self, text="Attached — awaiting input")
        self.status.pack(side="bottom", pady=10)

        self.after(50, self._tick)

    def _section(self, name: str) -> None:
        ctk.CTkLabel(self, text=name, font=("Segoe UI", 14, "bold")).pack(pady=(12, 2), padx=20, anchor="w")

    def _toggle_godmode(self) -> None:
        enabled = bool(self.godmode_btn.get())
        self.player.toggle_godmode(enabled)

    def _toggle_stamina(self) -> None:
        self.combat.set_infinite_stamina(bool(self.stamina_btn.get()))

    def _toggle_esp(self) -> None:
        if self.overlay.enabled:
            self.overlay.stop()
        else:
            self.overlay.start()

    def _tick(self) -> None:
        try:
            self.player.tick()
            self.combat.tick()
            stats = self.player.read_stats()
            self.status.configure(text=f"HP {stats.health:.0f}  Gold {stats.gold}  SP {stats.skill_points}")
        except Exception as exc:  # noqa: BLE001
            logger.debug("tick error: {}", exc)
        self.after(100, self._tick)