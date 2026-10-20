"""Standalone offset dumper — run against a live Crimson Desert build.

Usage:
    python tools/offset_dumper.py --pattern health --scan
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pymem

from crimson_trainer.process.attach import GameProcess


def scan_float(proc: GameProcess, value: float, max_results: int = 32) -> list[int]:
    hits: list[int] = []
    step = 4
    addr = proc.base
    end = proc.base + 0x10000000
    while addr < end and len(hits) < max_results:
        try:
            if abs(proc.read_float(addr) - value) < 0.01:
                hits.append(addr)
        except Exception:  # noqa: BLE001
            pass
        addr += step
    return hits


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--value", type=float, default=100.0)
    p.add_argument("--out", type=Path, default=Path("offsets/scan.json"))
    args = p.parse_args(argv)

    proc = GameProcess("CrimsonDesert.exe")
    if not proc.attach():
        print("attach failed", file=sys.stderr)
        return 1
    hits = scan_float(proc, args.value)
    args.out.write_text(json.dumps({"value": args.value, "hits": hits}, indent=2))
    print(f"wrote {len(hits)} candidates -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())