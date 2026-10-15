# Acceptance Test Plan

The purpose of this plan is to verify the mandatory behaviour before submission and before uploading the packaged game.

Status values: `PASS`, `TO RETEST`, `PENDING`.

| Test | Expected result | Status |
|---|---|---|
| `make clean_env && make install` | Virtual environment is recreated and every dependency, including the maze wheel, installs | PASS |
| `make lint` | flake8 and mypy validate project code | TO RETEST before submission |
| `make package` | `dist/pacman/` is rebuilt from `pacman.spec` and receives the config file | PASS |
| Launch with `config.json` | Game starts without traceback | PASS |
| Launch with missing/wrong config | Clear error or safe fallback according to the error type; no raw traceback | PASS / final retest |
| Config with missing values | Defaults are used and messages are printed | PASS |
| Config with out-of-range values | Values are clamped to safe limits | PASS |
| First level generated twice with same seed | Same level layout | PASS |
| Later levels | Random maze generation | PASS |
| Player movement | Cannot cross walls; buffered turns work | PASS |
| Pacgum collision | Pacgum disappears and score increases | PASS |
| Super-pacgum | Score increases and ghosts become edible temporarily | PASS |
| Normal ghost collision | One life is lost and entities respawn | PASS |
| Edible ghost collision | Ghost is eaten and score increases | PASS |
| Level completion | Next level loads while score and remaining lives are kept | PASS |
| Final level completion | Victory screen is reached | TO RETEST |
| Timer reaches zero | Configured timeout behaviour occurs without crash | PASS |
| Pause / resume | Gameplay and timers remain frozen while paused | PASS |
| Cheats F1–F4 | Speed, invincibility, timer freeze and level skip work | PASS |
| Cheats across level skip | Active cheat state is preserved across the new `Playing` state | PASS |
| Cheat run ending | Score is not saved to highscores | PASS |
| Normal run ending | Valid name can be entered and score is saved | TO RETEST |
| Highscore file missing | Game starts with an empty highscore list | PASS |
| Highscore file malformed | Bad data is ignored/handled without crash | PASS |
| Main menu | Start, highscores, instructions and exit are reachable | PASS |
| Menu slideshow | Backgrounds rotate and fade without blocking inputs | PASS |
| Packaged binary | Sprites, fonts, backgrounds and config are found | PASS / retest after final assets |

## Final pre-submission run

1. Remove temporary build output.
2. Run `make install` from a clean environment.
3. Run `make lint`.
4. Run the source version with `make run`.
5. Test one death, one super-pacgum, one edible ghost and pause/resume.
6. Use the cheat skip to reach the final level and confirm the victory flow.
7. Save a normal highscore and reopen the highscore screen.
8. Run `make package` and launch the packaged binary.
9. Verify the repository contains the README, project-management files, wheel, spec and source only (no virtual environment/build output committed).
