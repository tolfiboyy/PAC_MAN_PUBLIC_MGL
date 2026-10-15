# Risk Analysis

This file lists the main risks identified during the Pac-Man project and the mitigation used by the team.

| Risk | Impact | Mitigation / decision | Status |
|---|---|---|---|
| External maze package changes or fails | Game cannot start a level | Keep the original wheel, install it through `requirements.txt`, isolate its use in `level_logic.py` | Monitored |
| Invalid configuration during peer review | Crash or unusable game | Validate types, clamp numeric values, provide defaults and clear messages | Mitigated |
| Use of a Pygame feature without an MLX equivalent | Subject non-compliance | Use basic surfaces, pixels, image loading, blitting and events; avoid runtime sprite transforms | Mitigated |
| State change loses score/lives/cheats | Incorrect level progression | Store persistent game data in `GameSession` rather than in a single `Playing` object | Mitigated |
| Highscore file is missing/corrupted/unwritable | Game crash or lost menu | Validate JSON entries and catch file errors; continue with an empty/in-memory list | Mitigated |
| Packaging misses assets or dependencies | Distributed build does not launch | Keep `pacman.spec` at repository root and test `make package` from a clean build | Mitigated |
| Relative asset paths depend on launch directory | Packaged build may fail from an unexpected working directory | Validate the packaged build before platform upload | To retest |
| Two developers edit the same architecture area | Merge conflicts / duplicated work | Split gameplay and application/UI work, record shared decisions in the roadmap | Mitigated |
| Last-minute feature changes create regressions | Broken final build | Freeze non-essential features, run acceptance tests before submission/upload | Active |
