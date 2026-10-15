# Architecture

Last update: 15/10 (W4)

## 1. Overview

```
pac-man.py            entry point: arguments → Config → App
config.json           default configuration
requirements.txt      dependencies, including the assigned maze package (wheel)
Makefile              install, run, debug, clean, lint, lint-strict, package
pacman.spec           PyInstaller spec (packaged build)

app/                  application layer (Lucifer)
  config.py           config file reading, comment filtering, validation
  app.py              App: main loop, state transitions, fonts loading
  state.py            StateName, State base class and every screen
  game_session.py     GameSession: data of the game in progress
  highscores.py       load / validate / add / save highscores

game/                 gameplay layer (Adrien)
  level_logic.py      calls the maze generator, builds a level
  collectibles.py     pacgums placement, eating, level completion
  player_logic.py     player movement and smooth rendering
  ghost_logic.py      ghost targets (4 personalities), frightened mode
  movement.py         wall checks, moves on the grid
  pathfinding.py      BFS shortest path
  collisions.py       player / ghost collisions
  reset_logic.py      respawn after a death or a ghost being eaten
  cheats.py           CheatState
  input.py            direction keys, cheat keys (CHEATINPUT)
  rendering.py        maze, entities and HUD drawing
  assets.py           image loading
  constants.py        colors, wall bits
  entities/           Player, Ghost

assets/               sprites (4 directions per entity) and fonts (Montserrat, OFL)
project_management/   ROADMAP.md, ARCHITECTURE.md
```

Dependency rule: `app/` uses `game/`; `game/` only uses `app.config.Config`
for gameplay values. Only `app/app.py` owns the window and the main loop.

## 2. Startup sequence

1. `pac-man.py` checks there is exactly one argument and that it ends with
   `.json`, then calls `Config.from_file`. Any `ConfigError` prints a clear
   message on stderr and exits with code 1.
2. `App.__init__` opens the window, loads the fonts (fallback to the pygame
   default font if a file is missing or broken), loads the highscores, loads
   the images (exits cleanly if one is missing) and starts on the `Menu`.
3. `App.run()` runs the main loop until `QUIT` or the window is closed.

## 3. Maze representation

- The maze is a `list[list[int]]`, accessed as `maze[y][x]`.
- Coordinates are always written `(x, y)`.
- Each cell is a 4-bit wall mask: `NORTH = 1`, `EAST = 2`, `SOUTH = 4`,
  `WEST = 8`. A value of 15 is a closed cell (part of the "42" pattern).
- Pixel position of a cell: `pixel_x = x * cell_size`,
  `pixel_y = y * cell_size + hud_height` (the HUD is a band at the top).

### Maze generator integration

- The assigned package is `mazegenerator` 2.1.0, installed with pip from the
  wheel listed in `requirements.txt`. It is used as-is, never modified.
- `game/level_logic.py` is the only module that imports it:
  `MazeGenerator((width, height), False, (0, 0), (2, 2), seed).maze`.
  `False` = non-perfect maze (loops, no dead ends).
- Level 1 uses `config.seed`; the next levels use seed `0` (random for this
  generator).
- Player spawn: center cell, shifted one column left for even widths, which
  always lands in an empty column of the "42" pattern (decision D6).
- A failure of the generator is caught in `App` (case `PLAYING`) so that it
  never produces a traceback. Recovery is still partial (see I16 in the roadmap).

## 4. Configuration contract (validated values)

Rules: wrong type → default value + message.
Out of bounds → clamped to the nearest bound + message.
Unknown keys → ignored. `true`/`false` are never accepted as numbers.
Lines starting with `#` (after optional spaces) are comments. They are
replaced by empty lines so that JSON error messages keep the right line number.

### Global values

| Key                     | Type | Default           | Valid range          | Notes                                       |
|-------------------------|------|-------------------|----------------------|---------------------------------------------|
| highscore_filename      | str  | "highscores.json" | non-empty string     | path of the highscore file                  |
| lives                   | int  | 3                 | 1 – 9                | lives at game start                         |
| pacgum                  | int  | 42                | ≥ 1                  | pacgums per level, capped to the free cells |
| points_per_pacgum       | int  | 10                | 0 – 10000            |                                             |
| points_per_super_pacgum | int  | 50                | 0 – 10000            |                                             |
| points_per_ghost        | int  | 200               | 0 – 10000            |                                             |
| seed                    | int  | 500               | ≥ 1                  | level 1 only, next levels are random        |
| level_max_time          | int  | 90                | 10 – 600             | seconds, same limit for every level         |
| level                   | list | 10 default levels | ≥ 10 levels          | padded with default levels if < 10 (D5)     |

### Per-level values (each item of "level")

| Key    | Type | Default | Valid range | Notes                           |
|--------|------|---------|-------------|---------------------------------|
| width  | int  | 21      | 14 – 35     | minimum needed for the "42"     |
| height | int  | 15      | 10 – 20     | minimum needed for the "42"     |

An invalid level entry (not an object) is skipped with a message. Missing
levels are taken from the default list, starting at the same position.

## 5. State machine

### Principle

A single main loop (`App.run`) drives the whole program. Each frame it:

1. computes `dt` with `pygame.time.Clock().tick(60)` (seconds), capped at
   0.1 s so that a freeze never makes the game jump,
2. forwards every pygame event to the current state, except the window
   close event, handled by `App` itself (quits from any state),
3. calls `update(dt)`, then `draw(screen)` on the current state, then
   `pygame.display.flip()` (the only flip of the program),
4. if the current state set `next_state`, calls `change_state`.

Only `App` reads the real time. Only `App` changes the current state.

### State interface

Every state inherits from `State` (abstract base class):

- `handle_event(event)` — abstract: react to user input
- `draw(screen)` — abstract: repaint the whole screen
- `update(dt)` — optional (default: do nothing)
- `next_state: StateName | None` — set by the state to request a transition

`StateName`: `MENU`, `PLAYING`, `PAUSED`, `RESUME`, `END`, `HIGHSCORES`,
`INSTRUCTIONS`, `QUIT`.

### States

| State        | Shows                                                   | Keys                                              | Can request                             |
|--------------|---------------------------------------------------------|---------------------------------------------------|-----------------------------------------|
| Menu         | title, 4 options, top 3 highscores                      | Up/Down, Enter                                    | PLAYING, HIGHSCORES, INSTRUCTIONS, QUIT |
| Playing      | maze, entities, HUD, optional cheat sheet               | arrows, Esc/Pause = pause, End, Tab, F1–F4        | PAUSED, PLAYING (next level), END       |
| Paused       | frozen game behind the pause text                       | Space/Enter/Esc = resume, End = end the game      | RESUME, END                             |
| End          | GAME OVER or VICTORY, final score, name input           | letters/digits/space, Backspace, Enter, Esc       | MENU                                    |
| Highscores   | top 10 scores                                           | Space/Esc                                         | MENU                                    |
| Instructions | controls, rules, cheat sheet key                        | Space/Esc                                         | MENU                                    |

Game Over and Victory are the same `End` state: the title depends on
`session.won`.

### Transitions

    Menu ──Start──────────> Playing ──Esc──> Paused ──Resume──> Playing
     │                        │                 └──End──> End
     ├──Highscores──> Highscores ──> Menu
     ├──Instructions──> Instructions ──> Menu
     └──Exit──> QUIT

    Playing ──level complete, not last──> Playing (next level)
    Playing ──last level complete──> End (victory) ──Enter / Esc──> Menu
    Playing ──no lives left / End key──> End (game over) ──Enter / Esc──> Menu

### What `App.change_state` does

The first thing it does is reset `next_state` on the state that asked, so a
`Playing` resumed after a pause never asks for a pause again.

| Requested    | Action                                                                                          |
|--------------|-------------------------------------------------------------------------------------------------|
| PLAYING      | creates the `GameSession` if there is none (new game), creates a **new** `Playing` for `session.level_index`, resizes the window to `Playing.windows_size`. Errors (generator) are caught |
| PAUSED       | creates a `Paused` holding the current `Playing` (checked with `isinstance`)                    |
| RESUME       | the current state becomes the `Playing` held by `Paused` (same game, same clock)                |
| END          | resizes the window to the menu size, creates an `End` with the session, the highscores and the file path |
| MENU         | discards the session, creates a `Menu`, resizes the window to the menu size                     |
| HIGHSCORES   | creates a `Highscores` screen                                                                   |
| INSTRUCTIONS | creates an `Instructions` screen                                                                |
| QUIT         | stops the main loop                                                                             |
| other        | `RuntimeError` (programming error)                                                              |

## 6. Shared data

| Data          | Created by           | Lifetime                         | Used by                                         |
|---------------|----------------------|----------------------------------|-------------------------------------------------|
| `Config`      | `pac-man.py`         | whole program, read-only         | `App`, `Playing`, `game/*`                      |
| fonts (dict)  | `load_fonts` in App  | whole program                    | every state (`Title`, `Bold`, `SemiBold`, `Medium`, `SemiMedium`) |
| images        | `load_images` in App | whole program                    | `Playing`                                       |
| `GameSession` | App, on a new game   | one game (until back to Menu)    | `Playing` (read/write), `Paused`, `End`         |
| highscores    | `load_highscores`    | whole program                    | `Menu`, `Highscores` (read), `End` (adds + saves) |

`GameSession` fields: `lives`, `score`, `level_index`, `won`,
`cheats` (`CheatState`), `cheated`.

The highscore list is **one shared list object**: `add_score` modifies it in
place (`append`, `sort`, `del [10:]`), so the menu sees a new score without
being recreated.

## 7. Game clock

`Playing` owns its clock: `game_time` (seconds, starts at 0 for each level),
increased by `dt` in `update`. Every gameplay function receives it as `now`
(movement delays, frightened mode, ghost respawn, level timer). `Paused`
never calls `Playing.update`, so everything freezes during a pause without
any pause-specific code.

Level timer:
`remaining_time = level_max_time - (cheats.get_timer_time(game_time) - level_start_time)`.
`level_start_time` is reset to `game_time` after a death or a time out.
The timer-freeze cheat returns a fixed time while active, and the frozen
duration is added to `level_start_time` when it is turned off.

## 8. Gameplay

### Entities and movement

- `Player` and `Ghost` have a grid position (`x`, `y`), a target cell
  (`target_x`, `target_y`) and a rendered position (`render_x`, `render_y`,
  floats). A new direction is only chosen when the entity has reached its
  target cell; the rendered position glides toward the target at
  `speed × dt` cells per second (player 4.0, ghosts 2.8).
- Buffered turns: the arrow pressed is stored in `requested_direction` and
  applied as soon as the move is possible.

### Ghosts

- One ghost per corner, each with a personality:
  `direct` (targets the player), `ahead` (3 cells in front of the player),
  `vector` (uses Blinky's position, like the original game),
  `distance` (chases when far, goes back to its corner when close).
- Paths are computed with a BFS on the maze (`pathfinding.py`).
- Frightened mode: eating a super-pacgum makes every ghost edible for 5 s
  and sends each one to a different random corner.
- An eaten ghost goes back to its corner and waits 2 s before moving again.

### Collisions and rules

- Collision = distance between rendered positions ≤ 0.40 cell.
- Edible ghost touched: `+points_per_ghost`. Otherwise: one life lost,
  player and ghosts back to their spawn.
- Time out (D2): counts as a death.
- Level complete when every pacgum and super-pacgum is eaten. Score and
  lives are kept between levels. Last level complete → victory.
- Pacgums are spread randomly over the free cells (seeded with `config.seed`
  on level 1); super-pacgums are in the 4 corners.

### Cheats

| Key | Effect                                  | Shown green when active |
|-----|-----------------------------------------|-------------------------|
| F1  | player speed +4                         | yes                     |
| F2  | invincibility                           | yes                     |
| F3  | freeze the level timer                  | yes                     |
| F4  | skip the current level                  | no (one-shot)           |
| Tab | show / hide the cheat sheet             | —                       |
| End | end the game now (not a cheat)          | —                       |

Keys are defined once in `CHEATINPUT` (`game/input.py`); the cheat sheet
reads the same dictionary. Cheats live in the `GameSession`, so they stay
active from one level to the next. Using F1–F4 marks the session as
`cheated`: the score is then not saved (D4).

## 9. Highscores

- File: path from `highscore_filename`, relative to the directory the game
  is launched from.
- Format: JSON list of objects, e.g. `[{"name": "Tom", "score": 840}]`.
  In memory: `list[tuple[str, int]]`, sorted by score, 10 entries max.
- Loading never stops the game: missing file → empty list (first launch,
  no message); unreadable file or invalid JSON → message + empty list;
  invalid entries are skipped one by one.
- Valid name: 1–10 characters, letters (accents allowed), digits and spaces,
  not only spaces; trimmed when saved. Valid score: integer ≥ 0.
- The End screen builds the name key by key with `event.unicode`: a
  character is only added if the resulting name is still valid.
- Enter adds the score, sorts, keeps the top 10 and saves the file. A write
  error prints a message and the game continues.

## 10. Rendering and MLX equivalence

The subject only allows pygame features that have an MLX equivalent.

| pygame                                   | MLX equivalent                         | Used for                          |
|------------------------------------------|----------------------------------------|-----------------------------------|
| `display.set_mode`                       | `mlx_new_window`                       | window                            |
| `Surface.set_at`                         | `mlx_pixel_put`                        | walls, pacgums (pixel by pixel)   |
| `image.load`                             | `mlx_png_file_to_image` / `xpm`        | sprites                           |
| `Surface.blit`                           | `mlx_put_image_to_window`              | sprites, text                     |
| `Surface.fill`                           | clearing the window / image            | backgrounds                       |
| `font.render` + `blit`                   | `mlx_string_put`                       | text (custom font: see below)     |
| `event.get` (KEYDOWN, QUIT)              | `mlx_hook` / `mlx_key_hook`            | keyboard, window close            |
| main loop                                | `mlx_loop_hook`                        | frame update                      |
| `Surface(..., SRCALPHA)` + `fill`        | `mlx_new_image` + writing its pixels   | cheat sheet background            |

Not used on purpose: `pygame.draw.*`, `pygame.transform.*` (sprites exist in
4 directions instead of being rotated), sprite groups, rects collisions, sound.

Points to defend during the review:
- Custom TTF fonts: MLX writes text with its own font only.
- Semi-transparent background of the cheat sheet: alpha blending depends on
  the MLX version. Setting the alpha to 255 gives a plain background.
- `pygame.time.Clock` is used for timing only, not for drawing.
