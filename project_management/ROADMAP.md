# Roadmap

> How to use this file: update it at least once a week. Never overwrite a
> planned week once it is set: fill the **Actual** column instead, so the gap
> between plan and reality stays visible. Explain any slip in the progress log.

Week reference:
W1 = 21/09 → 27/09 · W2 = 28/09 → 04/10 · W3 = 05/10 → 11/10 ·
W4 = 12/10 → 18/10 · W5 = 19/10 → 25/10 · W6 = 26/10 → 01/11

Status values: `TODO` · `IN PROGRESS` · `DONE` · `BLOCKED` · `DROPPED`

Last update: 15/10 (W4) (took us four weeks to complete this subject)

---

## Milestones

| #  | Milestone          | Content                                                        | Planned | Actual | Status      |
|----|--------------------|----------------------------------------------------------------|---------|--------|-------------|
| M1 | Foundations        | Repo setup, config loader, maze rendering, player movement     | W1      | W2     | DONE        |
| M2 | Playable level     | Main loop + states, pacgums, score, maze integration           | W2      | W3     | DONE        |
| M3 | Threats            | Ghosts, super-pacgums, lives, respawn                          | W3      | W3     | DONE        |
| M4 | Full game loop     | Levels, timer, all menus, highscores, HUD, cheat mode          | W4      | W4     | DONE        |
| M5 | Delivery           | Packaging, itch.io deployment, tested on a clean machine       | W5      |        | IN PROGRESS |
| M6 | Polish and defense | Lint clean, visuals, README, project docs, acceptance tests    | W6      |        | IN PROGRESS |

---

## Tasks — Adrien (gameplay)

| ID  | Task                                                    | Planned | Actual | Status      | Notes                                                      |
|-----|---------------------------------------------------------|---------|--------|-------------|------------------------------------------------------------|
| A1  | Maze rendering (prototype)                              | W1      | W1     | DONE        |                                                            |
| A2  | Rendering compliant with MLX constraint                 | W2      | W2     | DONE        | pixel by pixel (`set_at`), see D1                          |
| A3  | Generic entity movement (shared by player and ghosts)   | W1      | W2     | DONE        | `movement.py`                                              |
| A4  | Player input + buffered turns                           | W1      | W2     | DONE        | `requested_direction`                                      |
| A5  | Wall collisions                                         | W1      | W2     | DONE        |                                                            |
| A6  | Pacgums placement + eating + score                      | W2      | W4     | DONE        | random spread, seeded on level 1 (I2 fixed)                |
| A7  | Super-pacgums + frightened mode                         | W3      | W3     | DONE        | ahead of plan                                              |
| A8  | Player/ghost collision, lives, respawn                  | W3      | W3     | DONE        | distance-based collision on rendered positions             |
| A9  | Level win condition (all pacgums eaten)                 | W3      | W3     | DONE        | wired into the state machine (L4e)                         |
| A10 | Cheat mode effects                                      | W4      | W3     | DONE        | speed, invincibility, timer freeze, level skip             |
| A11 | Use the game clock instead of `time.monotonic()`        | W3      | W3     | DONE        | every `now` comes from `Playing.game_time`                 |
| A12 | Smooth movement (interpolated rendering)                | —       | W3     | DONE        | added task: `render_x/render_y` glide toward targets       |
| A13 | Ghost personalities                                     | —       | W3     | DONE        | added task: direct, ahead, vector, distance                |
| A14 | Directional sprites (no image rotation)                 | —       | W4     | DONE        | added task: 4 images per entity, MLX compliance            |
| A15 | Packaging (PyInstaller spec + `make package`)           | W5      | W4     | IN PROGRESS | spec at repo root; not yet tested on a clean machine       |
| A16 | itch.io deployment (unlisted build)                     | W5      |        | TODO        |                                                            |
| A17 | Validate the grid returned by the generator             | W4      |        | TODO        | also fixes the mypy `no-any-return` in `level_logic.py`    |

## Tasks — Tom (infrastructure and UI)

| ID  | Task                                                    | Planned | Actual | Status      | Notes                                                      |
|-----|---------------------------------------------------------|---------|--------|-------------|------------------------------------------------------------|
| L1  | Config contract documented in ARCHITECTURE.md           | W1      | W2     | DONE        |                                                            |
| L2  | Config loader (args, file reading, comment stripping)   | W1      | W2     | DONE        |                                                            |
| L3  | Config validation, defaults, clear messages             | W1      | W3     | DONE        | dataclasses + generic validation                           |
| L12 | Entry point: arguments, startup errors, asset loading   | W3      | W3     | DONE        | added task                                                 |
| L4a | State machine design (ARCHITECTURE.md)                  | W2      | W3     | DONE        |                                                            |
| L4b | `StateName` Enum + `State` base class                   | W3      | W3     | DONE        |                                                            |
| L4c | `App`: main loop, dt, transitions                       | W3      | W3     | DONE        |                                                            |
| L4d | Stub states, full cycle tested                          | W3      | W3     | DONE        |                                                            |
| L4e | Move gameplay code into the `Playing` state             | W3      | W3     | DONE        | with Adrien                                                |
| L4f | Game clock + level timer                                | W3      | W3     | DONE        | with Adrien, see A11                                       |
| L4g | Resume countdown (3, 2, 1)                              | —       | W4     | DROPPED     | see D11                                                    |
| L5  | Maze generator integration + error handling             | W2      | W4     | IN PROGRESS | installed from the wheel (D8); failure handling partial (I16) |
| L6  | Packaging spike                                         | W2      | W4     | DONE        | merged into A15                                            |
| L7  | Highscores (load, validate, top 10, save)               | W3      | W4     | DONE        | see D3, D4, D14                                            |
| L8  | Screens: Menu, Instructions, Paused                     | W3      | W3     | DONE        |                                                            |
| L9  | Screens: End (game over / victory + name), Highscores   | W4      | W4     | DONE        |                                                            |
| L10 | HUD, level timer, level progression                     | W4      | W4     | DONE        | HUD drawn by Adrien's `draw_hud`                           |
| L13 | In-game cheat sheet (Tab)                               | —       | W4     | DONE        | added task: 2×2 grid, active cheats in green               |
| L11 | Visual polish (menus, colors, layout)                   | W6      |        | TODO        | after lint is clean                                        |

## Shared tasks

| ID  | Task                                                    | Planned | Actual | Status      | Notes                                                      |
|-----|---------------------------------------------------------|---------|--------|-------------|------------------------------------------------------------|
| S1  | Makefile (install, run, debug, clean, lint, package)    | W1      | W4     | DONE        | `lint-strict` and `clean_build` included                   |
| S2  | `.gitignore`                                            | W1      | W4     | DONE        | venv, caches, `build/`, `dist/`, `highscores.json`         |
| S3  | Ghost AI (chase / flee / respawn)                       | W3      | W3     | DONE        | see A13                                                    |
| S4  | Risk analysis                                           | W1      |        | TODO        |                                                            |
| S5  | Acceptance test plan + bug log                          | W4      | W4     | IN PROGRESS | first headless run on 14/10, see "Test runs"; bug log = Known issues |
| S6  | Unit tests on pure logic                                | W2–W5   |        | TODO        | config and highscores tested manually so far               |
| S7  | README (all required sections, in English)              | W6      |        | TODO        | on hold until the code is final                            |
| S8  | Lint clean (flake8 + mypy)                              | W6      |        | IN PROGRESS | 66 flake8 + 6 mypy errors on 14/10 (I18)                   |

---

## Decisions

| ID  | Question                                                          | Owner   | Decision                                                                                       | Date |
|-----|-------------------------------------------------------------------|---------|------------------------------------------------------------------------------------------------|------|
| D1  | How to render using only MLX-equivalent functions?                | Adrien  | Pixel by pixel (`set_at` ≈ `mlx_pixel_put`), images prepared in the asset files, no `draw.*` / `transform.*` | W2   |
| D2  | What happens when the level timer runs out?                       | Both    | Counts as a death: lose a life, back to spawn, timer restarts                                  | W3   |
| D3  | Where is the highscore file stored?                               | Tom | Path from `highscore_filename` in the config (relative to the launch directory), JSON list of `{"name", "score"}` | W4   |
| D4  | Do scores obtained in cheat mode enter the highscores?            | Both    | No. Using any F1–F4 cheat marks the session; the End key is not a cheat                        | W4   |
| D5  | What if the config defines fewer than 10 levels?                  | Tom | Padded with the default levels from the same position, with a message                          | W2   |
| D6  | Player spawn when the "42" pattern occupies the center            | Both    | Center column, shifted left for even widths (always an empty column)                           | W3   |
| D7  | Window size vs cell size when level sizes differ                  | Both    | **Open.** Menus use a fixed window; each level resizes the window to its own size (D15). Max sizes still too large (I3) |      |
| D8  | How is the assigned A-Maze-ing package installed?                 | Both    | pip install of `mazegenerator-2.1.0` wheel through `requirements.txt` (`make install`)         | W4   |
| D9  | Game Over and Victory screens                                     | Tom | One `End` state with name input, title depends on `session.won`                                | W3   |
| D10 | How does pause keep the game intact?                              | Tom | `Paused` keeps a reference to `Playing` + `Playing` owns its game clock                         | W3   |
| D11 | Countdown before resuming                                         | Tom | Dropped: tried inside `App`, conflicted with the state machine design; not worth the risk      | W4   |
| D12 | Where do cheats live?                                             | Both    | In `GameSession`: active cheats persist across levels, reset on a new game                     | W4   |
| D13 | End key during a game or a pause                                  | Both    | Ends the game and opens the End screen (score can be saved). To double-check against 6.8 (I19) | W4   |
| D14 | Player name rules                                                 | Tom | 1–10 chars, letters (accents allowed), digits and spaces, not only spaces, trimmed on save     | W4   |
| D15 | Who resizes the window?                                           | Tom | `App`, using the size computed by each new `Playing` (`windows_size`)                          | W4   |
| D16 | Frame timing                                                      | Both    | `pygame.time.Clock().tick(60)` in `App` only, `dt` capped at 0.1 s                             | W3   |

---

## Known issues and bug log

| ID  | Issue                                                                       | Found | Owner   | Status |
|-----|-----------------------------------------------------------------------------|-------|---------|--------|
| I1  | `score += 200` overwrote `config.points_per_ghost` after a merge            | W3    | Adrien  | FIXED  |
| I2  | Pacgums placed in grid order, concentrated on the first rows                | W3    | Adrien  | FIXED (W4) |
| I3  | Largest allowed level (35×20 cells of 60 px) gives a 2100×1250 window; menus are 1320×1010 | W3 | Both | OPEN |
| I4  | Module name conflict with the maze generator import                         | W3    | Both    | FIXED (W4, D8) |
| I5  | Config defaults differ between code and ARCHITECTURE.md                     | W3    | Tom | FIXED (W4, doc aligned on the code) |
| I6  | Lives reset to `config.lives` at each new level (subject: lives are kept)   | W3    | Adrien  | FIXED (W3, L4e) |
| I7  | `clock.tick(min(60, 0.1))` limited the game to one frame every 10 s         | W3    | Tom | FIXED (W3) |
| I8  | `change_state` stored a `StateName` instead of a state object               | W3    | Tom | FIXED (W3) |
| I9  | END transition did nothing (wrong `isinstance` check)                       | W4    | Tom | FIXED (W4) |
| I10 | Broken imports after moving files into `app/` (`Pacman.app.state`, `game_session`) | W4 | Tom | FIXED (W4) |
| I11 | `save_highscores` opened the file in read mode and dumped the file object   | W4    | Tom | FIXED (W4) |
| I12 | `add_score` truncated a local copy: the shared list grew beyond 10          | W4    | Tom | FIXED (W4) |
| I13 | `cheated` stored per state: lost between `Playing` and `End`                | W4    | Tom | FIXED (W4, D12) |
| I14 | `pygame.key.set_repeat(1, 1)` in End: one key press typed many characters   | W4    | Tom | FIXED (W4) |
| I15 | mypy aborted: `app/` had no `__init__.py`                                   | W4    | Tom | FIXED (W4) |
| I16 | Generator failure: no crash any more, but session not reset and a failure between levels keeps the old maze | W4 | Both | OPEN |
| I17 | End screen: Enter with an empty name leaves without saving                  | W4    | Tom | OPEN (decide) |
| I18 | Lint: 66 flake8 errors (all in `app/`) + 6 mypy errors                      | W4    | Both    | OPEN |
| I19 | End screen still shows "ENTER to save" for cheated runs                     | W4    | Tom | OPEN |

---

## Test runs

### 14/10 — headless scenario (simulated key presses, real config)

| Scenario                                                              | Result |
|-----------------------------------------------------------------------|--------|
| Menu navigation to Highscores, Instructions, Start                    | DONE   |
| Window resized to the level size (840×710 for level 1)                | DONE   |
| Escape → pause; clock and level timer frozen during pause             | DONE   |
| Escape → the same game resumes                                        | DONE   |
| Tab → cheat sheet displayed                                           | DONE   |
| Time out → one life lost                                              | DONE   |
| F4 → next level, lives kept, session marked as cheated                | DONE   |
| Cheated run → name input disabled, nothing saved                      | DONE   |
| New game → fresh session                                              | DONE   |
| Pause + End → End screen, name capped at 10 chars, Backspace works    | DONE   |
| Enter → file created, score in the file and in the menu               | DONE   |
| 10 × F4 → Victory screen                                              | DONE   |
| Exit → program stops                                                  | DONE   |
| Bad arguments / missing file / invalid JSON / JSON list as config     | DONE (clear message, no traceback) |
| Generator raising an exception                                        | PARTIAL (I16) |

---

## Progress log

One entry per week: what was planned, what was actually done, what slipped and why.

### W1 (21/09 → 27/09)
- **Planned:** M1
- **Done:** project setup, maze rendering prototype, task split, config contract started
- **Slipped / why:** config loader not finished
- **Blocking points:** none

### W2 (28/09 → 04/10)
- **Planned:** M2
- **Done:** M1 finished (config loader, movement, collisions), pacgums and score,
  rendering made MLX-compliant
- **Slipped / why:** packaging spike (L6) and maze integration (L5) not started;
  config took longer than planned (switch to dataclasses)
- **Blocking points:** module name conflict on the generator import

### W3 (05/10 → 11/10)
- **Planned:** M3
- **Done:** config validation finished, entry point, state machine (`App` + all
  states), gameplay moved into `Playing`, game clock, ghost personalities,
  smooth movement, cheat effects. M2 and M3 closed.
- **Slipped / why:** risk analysis (S4) and packaging still not started; the
  integration of the gameplay into the state machine took most of the week
- **Blocking points:** a series of integration bugs (I6–I8), all fixed

### W4 (12/10 → 18/10) — in progress
- **Planned:** M4
- **Done so far:** integration bugs fixed (I9, I10), cheat sheet (Tab),
  highscore system with name input on the End screen, cheated runs excluded
  from highscores, generator installed from the wheel, directional sprites,
  random pacgum spread, PyInstaller spec, `.gitignore`, first headless test run.
  M4 closed.
- **Slipped / why:** resume countdown dropped (D11); lint not clean yet (I18)
- **Blocking points:** none. Open decisions: D7 (window size), I17, I19
