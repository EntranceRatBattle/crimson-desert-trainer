"""Windows process attach / read-write primitives for Crimson Desert."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass

import pymem
import pymem.process
from loguru import logger


@dataclass
class GameProcess:
    exe_name: str
    pid: int | None = None
    handle: pymem.Pymem | None = None
    base: int = 0

    def attach(self) -> bool:
        try:
            self.handle = pymem.Pymem(self.exe_name)
            module = pymem.process.module_from_name(
                self.handle.process_handle, self.exe_name
            )
            self.base = module.lpBaseOfDll
            self.pid = self.handle.process_id
            return True
        except pymem.exception.ProcessNotFound:
            logger.error("{} not found", self.exe_name)
            return False
        except Exception as exc:  # noqa: BLE001
            logger.exception("attach failed: {}", exc)
            return False

    def read_float(self, addr: int) -> float:
        return self.handle.read_float(addr)

    def write_float(self, addr: int, value: float) -> None:
        self.handle.write_float(addr, value)

    def read_int(self, addr: int) -> int:
        return self.handle.read_int(addr)

    def write_int(self, addr: int, value: int) -> None:
        self.handle.write_int(addr, value)

    def is_alive(self) -> bool:
        if not self.handle:
            return False
        STILL_ACTIVE = 259
        code = wintypes.DWORD()
        ctypes.windll.kernel32.GetExitCodeProcess(
            self.handle.process_handle, ctypes.byref(code)
        )
        return code.value == STILL_ACTIVE