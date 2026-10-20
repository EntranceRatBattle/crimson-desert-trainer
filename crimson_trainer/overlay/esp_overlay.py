"""DirectX-free overlay — draws entity boxes via a transparent Win32 window."""
from __future__ import annotations

import threading
import tkinter as tk
from dataclasses import dataclass

import numpy as np
from loguru import logger

from crimson_trainer.process.attach import GameProcess
from crimson_trainer.offsets.loader import OffsetTable


@dataclass
class Entity:
    x: float
    y: float
    z: float
    kind: str


class EspOverlay:
    def __init__(self, process: GameProcess, offsets: OffsetTable) -> None:
        self.process = process
        self.offsets = offsets
        self.enabled = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self.enabled = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("ESP overlay started")

    def stop(self) -> None:
        self.enabled = False
        logger.info("ESP overlay stopped")

    def read_entities(self) -> list[Entity]:
        base = self.process.base + self.offsets.entity_list
        out: list[Entity] = []
        for i in range(64):
            addr = base + i * self.offsets.entity_stride
            try:
                x = self.process.read_float(addr)
                y = self.process.read_float(addr + 4)
                z = self.process.read_float(addr + 8)
            except Exception:  # noqa: BLE001
                break
            if x == 0.0 and y == 0.0 and z == 0.0:
                continue
            out.append(Entity(x, y, z, kind="hostile" if i % 3 == 0 else "neutral"))
        return out

    def _run(self) -> None:
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-transparentcolor", "black")
        root.configure(bg="black")
        canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

        def draw() -> None:
            if not self.enabled:
                root.destroy()
                return
            canvas.delete("all")
            ents = self.read_entities()
            for e in ents:
                sx = int(e.x * 10 + root.winfo_screenwidth() / 2)
                sy = int(e.y * 10 + root.winfo_screenheight() / 2)
                color = "#ff2b2b" if e.kind == "hostile" else "#2bff88"
                canvas.create_rectangle(sx - 20, sy - 40, sx + 20, sy, outline=color, width=2)
            root.after(16, draw)

        draw()
        root.mainloop()