# Offset tables

Offsets change every game patch. When Crimson Desert updates:

1. Run `tools/offset_dumper.py --value 100` to scan for the health float.
2. Narrow down candidates by re-scanning after taking damage.
3. Copy the confirmed offsets into `crimson_trainer/offsets/manifest.json`
   under the new build key.
4. Recompute the checksum (see `loader.py`) and set the `checksum` field.
5. Bump `__version__` and test with `pytest -q`.