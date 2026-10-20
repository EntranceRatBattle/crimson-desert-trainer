# Security Policy

## Supported versions

| Trainer version | Crimson Desert build | Supported |
|-----------------|----------------------|-----------|
| 1.4.x           | 1.0.7+               | ✅        |
| 1.3.x           | 1.0.5                | ⚠️ limited |
| < 1.3           | any                  | ❌        |

## Reporting a vulnerability

The trainer attaches to the game process and reads/writes memory. Please
report any of the following privately to `security@crimson-desert-trainer.dev`:

- Arbitrary code execution risk in the injector path.
- Signature bypasses that could be weaponized against the game's
  anti-tamper (we will not publish details).
- Bundled binary mismatches (checksum mismatch in `native/`).

## Known limitations

- The trainer **must** run as Administrator for `OpenProcess` with
  `PROCESS_VM_READ | PROCESS_VM_WRITE`.
- Windows Defender may flag `injector/` binaries — this is expected for
  memory-editing tools. Add a folder exclusion if you trust the source.

## Do not

- Do not use this in any online/multiplayer session. Doing so may result
  in a ban and is outside the scope of support.