# Contributing to crimson-desert-trainer

Thanks for wanting to help. This is a community-driven open-source trainer
for **Crimson Desert** built in Python. Please read the guidelines below
before opening a PR.

## Ground rules

- Trainer is for **single-player / offline** use only. Do not submit
  features intended for multiplayer or online modes.
- Do not commit private offsets, dumped SDKs, or copyrighted game assets.
- Every memory write must be guarded by a version + checksum check
  (`crimson_trainer/offsets/loader.py`).
- New cheats go in `crimson_trainer/services/` with a matching test in
  `tests/`.

## Pull request flow

1. Fork + branch off `main` (`feat/godmode-rework`, `fix/esp-flicker`).
2. Run `pytest -q` — all tests must pass.
3. Update `CHANGELOG.md` (see template in `docs/`).
4. Bump `__version__` in `crimson_trainer/__init__.py` for user-facing cheats.

## Style

- `ruff` + `black` defaults, line length 100.
- No `print()` in services — use `loguru.logger`.
- Prefer dataclasses for state models.

## Reporting bugs

Use the issue template and attach the trainer log from `logs/trainer.log`.