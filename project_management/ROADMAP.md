# Roadmap

> How to use this file: update it at least once a week. Never overwrite a
> planned week once it is set: fill the **Actual** column instead, so the gap
> between plan and reality stays visible. Explain any slip in the progress log.

Week reference (adjust to the real deadline):
W1 = 21/09 → 27/09 · W2 = 28/09 → 04/10 · W3 = 05/10 → 11/10 ·
W4 = 12/10 → 18/10 · W5 = 19/10 → 25/10 · W6 = 26/10 → 01/11

Status values: `TODO` · `IN PROGRESS` · `DONE` · `BLOCKED`

---

## Milestones

| #  | Milestone          | Content                                                        | Planned | Actual | Status      |
|----|--------------------|----------------------------------------------------------------|---------|--------|-------------|
| M1 | Foundations        | Repo setup, config loader, maze rendering, player movement     | W1      | W2     | DONE        |
| M2 | Playable level     | Main loop + states, pacgums, score, maze adapter               | W2      |        | IN PROGRESS |
| M3 | Threats            | Ghosts, super-pacgums, lives, respawn                          | W3      |        | IN PROGRESS |
| M4 | Full game loop     | Levels, timer, all menus, highscores, HUD, cheat mode          | W4      |        | TODO        |
| M5 | Delivery           | Packaging, itch.io deployment, tested on a clean machine       | W5      |        | TODO        |
| M6 | Polish and defense | Lint clean, README, project docs, acceptance tests             | W6      |        | TODO        |

---

## Tasks — Adrien (gameplay)

| ID  | Task                                                    | Planned | Actual | Status      | Notes                                         |
|-----|---------------------------------------------------------|---------|--------|-------------|-----------------------------------------------|
| A1  | Maze rendering (prototype)                              | W1      | W1     | DONE        |                                               |
| A2  | Rendering compliant with MLX constraint                 | W2      | W2     | DONE        | pixel by pixel (set_at), see D1               |
| A3  | Generic entity movement (shared by player and ghosts)   | W1      | W2     | DONE        | movement.py                                   |
| A4  | Player input + buffered turns                           | W1      | W2     | DONE        | requested_direction                           |
| A5  | Wall collisions                                         | W1      | W2     | DONE        |                                               |
| A6  | Pacgums placement + eating + score                      | W2      | W2     | IN PROGRESS | placement concentrated on first rows (I2)     |
| A7  | Super-pacgums + frightened mode                         | W3      | W3     | DONE        | ahead of plan                                 |
| A8  | Player/ghost collision, lives, respawn                  | W3      | W3     | DONE        |                                               |
| A9  | Level win condition (all pacgums eaten)                 | W3      |        | IN PROGRESS | detected, needs the state machine (L4)        |
| A10 | Cheat mode effects                                      | W4      |        | TODO        |                                               |
| A11 | Use the game clock instead of time.monotonic()          | W3      |        | TODO        | with Lucifer, see L4f                         |

## Tasks — Lucifer (infrastructure and UI)

| ID  | Task                                                    | Planned | Actual | Status      | Notes                                         |
|-----|---------------------------------------------------------|---------|--------|-------------|-----------------------------------------------|
| L1  | Config contract documented in ARCHITECTURE.md           | W1      | W2     | DONE        |                                               |
| L2  | Config loader (args, file reading, comment stripping)   | W1      | W2     | DONE        |                                               |
| L3  | Config validation, defaults, clear messages             | W1      | W3     | DONE        | dataclasses + generic validation              |
| L12 | Entry point: arguments, startup errors, asset loading   | W3      | W3     | DONE        | added task                                    |
| L4a | State machine design (ARCHITECTURE.md)                  | W2      | W3     | DONE        |                                               |
| L4b | StateName Enum + State base class                       | W3      |        | TODO        |                                               |
| L4c | App: main loop, dt, transitions                         | W3      |        | TODO        |                                               |
| L4d | Stub states, full cycle tested                          | W3      |        | TODO        |                                               |
| L4e | Move gameplay code into the Playing state               | W3      |        | TODO        | with Adrien                                   |
| L4f | Game clock + level timer                                | W3      |        | TODO        | with Adrien, see A11                          |
| L5  | Maze generator adapter + grid validation                | W2      |        | TODO        | waiting for D8                                |
| L6  | Packaging spike (PyInstaller hello world + generator)   | W2      |        | TODO        | slipped, see W2 log                           |
| L7  | Highscores (load, validate, top 10, save)               | W3      |        | TODO        | location depends on D3                        |
| L8  | Screens: Menu, Instructions, Paused                     | W3      |        | TODO        |                                               |
| L9  | Screens: End (game over / victory + name), Highscores   | W4      |        | TODO        |                                               |
| L10 | HUD, level timer, level progression                     | W4      |        | IN PROGRESS | HUD started by Adrien (score, lives, time)    |
| L11 | Final packaging + itch.io deployment                    | W5      |        | TODO        |                                               |

## Shared tasks

| ID  | Task                                                    | Planned | Actual | Status      | Notes                                         |
|-----|---------------------------------------------------------|---------|--------|-------------|-----------------------------------------------|
| S1  | Makefile (install, run, debug, clean, lint, package)    | W1      |        | IN PROGRESS | check every target exists                     |
| S2  | .gitignore                                              | W1      |        | TODO        | __pycache__ found in the repo                 |
| S3  | Ghost AI (chase / flee / respawn)                       | W3      | W3     | IN PROGRESS | 4 behaviours (direct, ahead, vector, distance)|
| S4  | Risk analysis (RISKS.md)                                | W1      |        | TODO        |                                               |
| S5  | Acceptance test plan + bug log                          | W4      |        | TODO        |                                               |
| S6  | Unit tests on pure logic                                | W2–W5   |        | TODO        | config tested manually so far                 |
| S7  | README (all required sections, in English)              | W6      |        | TODO        |                                               |
| S8  | Lint clean (flake8 + mypy)                              | W6      |        | IN PROGRESS | config.py done, run `make lint` every week    |

---

## Decisions

| ID  | Question                                                          | Owner   | Decision                                                                 | Date |
|-----|-------------------------------------------------------------------|---------|--------------------------------------------------------------------------|------|
| D1  | How to render using only MLX-equivalent functions?                | Adrien  | Pixel by pixel (`set_at` ≈ `mlx_pixel_put`), images resized in the files | W2   |
| D2  | What happens when the level timer runs out?                       | Both    | Counts as a death: lose a life, back to spawn, timer restarts            | W3   |
| D3  | Where is the highscore file stored?                               | Lucifer |                                                                          |      |
| D4  | Do scores obtained in cheat mode enter the highscores?            | Both    |                                                                          |      |
| D5  | What if the config defines fewer than 10 levels?                  | Lucifer | Padded with the default levels from the same position, with a message    | W2   |
| D6  | Player spawn when the "42" pattern occupies the center            | Both    | Center column, shifted left for even widths (always an empty column)     | W3   |
| D7  | Window size vs cell size when level sizes differ                  | Both    |                                                                          |      |
| D8  | How is the assigned A-Maze-ing package installed (pip vs copied)? | Lucifer | Postponed (module name conflict to investigate)                          |      |
| D9  | Game Over and Victory screens                                     | Lucifer | One `End` state with name input, title depends on `session.won`          | W3   |
| D10 | How does pause keep the game intact?                              | Lucifer | Paused keeps a reference to Playing + Playing owns its game clock        | W3   |

---

## Known issues

| ID | Issue                                                                     | Found | Owner   | Status |
|----|---------------------------------------------------------------------------|-------|---------|--------|
| I1 | `score += 200` overwrote `config.points_per_ghost` after a merge          | W3    | Adrien  | TODO   |
| I2 | Pacgums placed in grid order, concentrated on the first rows              | W3    | Adrien  | TODO   |
| I3 | `cell_size = 60` makes a 40-cell-wide maze 2400 px wide (see D7)          | W3    | Both    | TODO   |
| I4 | Module name conflict with the maze generator import (see D8)              | W3    | Lucifer | TODO   |
| I5 | Defaults of `seed` and `pacgum` differ between code and ARCHITECTURE.md   | W3    | Lucifer | TODO   |

---

## Progress log

One entry per week: what was planned, what was actually done, what slipped and why.

### W1 (21/09 → 27/09)
- **Planned:** M1
- **Done:** project setup, maze rendering prototype, task split, config contract started
- **Slipped / why:**
- **Blocking points:**

### W2 (28/09 → 04/10)
- **Planned:** M2
- **Done:** M1 finished (config loader, movement, collisions), pacgums and score,
  rendering made MLX-compliant
- **Slipped / why:** packaging spike (L6) and maze adapter (L5) not started;
  config took longer than planned (switch to dataclasses)
- **Blocking points:** module name conflict on the generator import

### W3 (05/10 → 11/10)
- **Planned:** M3
- **Done so far:** config validation finished, entry point, ghosts AI,
  super-pacgums, lives, state machine design
- **Slipped / why:**
- **Blocking points:**
