# Architecture

Service-oriented layout for the Crimson Desert Trainer.

```
crimson_trainer/
├── bootstrap.py            # wires everything together
├── process/attach.py       # pymem wrapper, read/write primitives
├── offsets/loader.py       # versioned + checksum-verified offset tables
├── services/               # business logic (player, combat, world)
├── overlay/esp_overlay.py  # transparent Win32 ESP overlay
├── ui/trainer_window.py    # thin CustomTkinter controller
├── utils/                  # memory helpers, hotkey registration
└── config/                 # yaml settings
tools/                      # standalone offset dumper + launcher
tests/                      # pytest suite
```

Rule of thumb: **handlers (UI) never touch memory directly** — they call
services, which call `GameProcess`. That way any new cheat can be
unit-tested with a fake process backend (see `tests/test_player_service.py`).