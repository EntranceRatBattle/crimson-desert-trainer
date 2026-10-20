"""Unit tests for PlayerService using a fake process backend."""
from __future__ import annotations

from crimson_trainer.services.player_service import PlayerService
from crimson_trainer.offsets.loader import OffsetTable


class FakeProcess:
    base = 0x1000
    def __init__(self) -> None:
        self.mem: dict[int, float | int] = {}
    def read_float(self, addr: int) -> float:
        return float(self.mem.get(addr, 0.0))
    def read_int(self, addr: int) -> int:
        return int(self.mem.get(addr, 0))
    def write_float(self, addr: int, v: float) -> None:
        self.mem[addr] = v
    def write_int(self, addr: int, v: int) -> None:
        self.mem[addr] = v


OFFSETS = OffsetTable(
    build="test", player_base=0x100, health=0x10, stamina=0x20,
    gold=0x30, skill_points=0x38, entity_list=0x0, entity_stride=0x40,
    camera_matrix=0x0, checksum="test",
)


def test_godmode_locks_health():
    proc = FakeProcess()
    svc = PlayerService(proc, OFFSETS)
    svc.toggle_godmode(True)
    svc.tick()
    assert proc.read_float(proc.base + 0x100 + 0x10) == 9999.0


def test_set_gold_clamps_negative():
    proc = FakeProcess()
    svc = PlayerService(proc, OFFSETS)
    svc.set_gold(-500)
    assert proc.read_int(proc.base + 0x100 + 0x30) == 0