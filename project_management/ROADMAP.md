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
| M1 | Foundations        | Repo setup, config loader, maze rendering, player movement     | W1      |        | IN PROGRESS |
| M2 | Playable level     | Main loop + states, pacgums, score, maze adapter               | W2      |        | TODO        |
| M3 | Threats            | Ghosts, super-pacgums, lives, respawn                          | W3      |        | TODO        |
| M4 | Full game loop     | Levels, timer, all menus, highscores, HUD, cheat mode          | W4      |        | TODO        |
| M5 | Delivery           | Packaging, itch.io deployment, tested on a clean machine       | W5      |        | TODO        |
| M6 | Polish and defense | Lint clean, README, project docs, acceptance tests             | W6      |        | TODO        |

---

## Tasks — Didou (gameplay)

| ID  | Task                                                    | Planned | Actual | Status      | Notes                              |
|-----|---------------------------------------------------------|---------|--------|-------------|------------------------------------|
| A1  | Maze rendering (prototype)                              | W1      | W1     | DONE        | uses draw.line, see decision D1    |
| A2  | Rendering compliant with MLX constraint                 | W2      |        | TODO        | depends on D1                      |
| A3  | Generic entity movement (shared by player and ghosts)   | W1      |        | IN PROGRESS |                                    |
| A4  | Player input + buffered turns                           | W1      |        | IN PROGRESS |                                    |
| A5  | Wall collisions                                         | W1      |        | IN PROGRESS |                                    |
| A6  | Pacgums placement + eating + score                      | W2      |        | TODO        |                                    |
| A7  | Super-pacgums + frightened mode                         | W3      |        | TODO        |                                    |
| A8  | Player/ghost collision, lives, respawn                  | W3      |        | TODO        |                                    |
| A9  | Level win condition (all pacgums eaten)                 | W3      |        | TODO        |                                    |
| A10 | Cheat mode effects                                      | W4      |        | TODO        |                                    |

## Tasks — Lucifer (infrastructure and UI)

| ID  | Task                                                    | Planned | Actual | Status      | Notes                              |
|-----|---------------------------------------------------------|---------|--------|-------------|------------------------------------|
| L1  | Config contract documented in ARCHITECTURE.md           | W1      |        | TODO        | blocks Adrien's hardcoded values   |
| L2  | Config loader (args, file reading, comment stripping)   | W1      |        | IN PROGRESS |                                    |
| L3  | Config validation, defaults, clear messages             | W1      |        | IN PROGRESS |                                    |
| L4  | Main loop + state machine skeleton                      | W2      |        | TODO        | Adrien's gameplay plugs into it    |
| L5  | Maze generator adapter + grid validation                | W2      |        | TODO        |                                    |
| L6  | Packaging spike (PyInstaller hello world + generator)   | W2      |        | TODO        | early risk check                   |
| L7  | Highscores (load, validate, top 10, save)               | W3      |        | TODO        | location depends on D3             |
| L8  | Screens: main menu, instructions, pause                 | W3      |        | TODO        |                                    |
| L9  | Screens: game over, victory, name entry, highscores     | W4      |        | TODO        |                                    |
| L10 | HUD, level timer, level progression                     | W4      |        | TODO        |                                    |
| L11 | Final packaging + itch.io deployment                    | W5      |        | TODO        |                                    |

## Shared tasks

| ID  | Task                                                    | Planned | Actual | Status | Notes                               |
|-----|---------------------------------------------------------|---------|--------|--------|-------------------------------------|
| S1  | Makefile (install, run, debug, clean, lint, package)    | W1      |        | TODO   |                                     |
| S2  | .gitignore                                              | W1      |        | TODO   |                                     |
| S3  | Ghost AI (chase / flee / respawn)                       | W3      |        | TODO   | starts once A3 is stable            |
| S4  | Risk analysis (RISKS.md)                                | W1      |        | TODO   | update weekly                       |
| S5  | Acceptance test plan + bug log                          | W4      |        | TODO   |                                     |
| S6  | Unit tests on pure logic                                | W2–W5   |        | TODO   | config, highscores, adapter, AI     |
| S7  | README (all required sections, in English)              | W6      |        | TODO   |                                     |
| S8  | Lint clean (flake8 + mypy)                              | W6      |        | TODO   | run `make lint` every week          |

---

## Open decisions

| ID | Question                                                              | Owner   | Decision | Date |
|----|-----------------------------------------------------------------------|---------|----------|------|
| D1 | How to render walls using only MLX-equivalent functions?              | Adrien  |          |      |
| D2 | What happens when the level timer runs out?                           | Both    |          |      |
| D3 | Where is the highscore file stored (repo vs user data directory)?     | Lucifer |          |      |
| D4 | Do scores obtained in cheat mode enter the highscores?                | Both    |          |      |
| D5 | What if the config defines fewer than 10 levels?                      | Lucifer |          |      |
| D6 | Player spawn when the "42" pattern occupies the center                | Both    |          |      |
| D7 | Window size vs cell size when level sizes differ                      | Both    |          |      |
| D8 | How is the assigned A-Maze-ing package installed (pip vs copied)?     | Lucifer |          |      |

---

## Progress log

One entry per week: what was planned, what was actually done, what slipped and why.

### W1 (21/09 → 27/09)
- **Planned:** M1
- **Done:**
- **Slipped / why:**
- **Blocking points:**

### W2 (28/09 → 04/10)
- **Planned:** M2
- **Done:**
- **Slipped / why:**
- **Blocking points:**