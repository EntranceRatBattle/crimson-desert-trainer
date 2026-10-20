"""Low-level helpers around pymem for pointer-chain reads."""
from __future__ import annotations

from typing import Iterable

from crimson_trainer.process.attach import GameProcess


def resolve_pointer_chain(process: GameProcess, base: int, offsets: Iterable[int]) -> int:
    addr = base
    for off in offsets:
        addr = process.handle.read_longlong(addr) + off
    return addr


def read_vec3(process: GameProcess, addr: int) -> tuple[float, float, float]:
    return (
        process.read_float(addr),
        process.read_float(addr + 4),
        process.read_float(addr + 8),
    )


def write_vec3(process: GameProcess, addr: int, vec: tuple[float, float, float]) -> None:
    process.write_float(addr, vec[0])
    process.write_float(addr + 4, vec[1])
    process.write_float(addr + 8, vec[2])