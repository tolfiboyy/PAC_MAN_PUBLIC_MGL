Maze representation
-------------------
maze is a list[list[int]]

Access:
maze[y][x]

Coordinates:
(x, y)

Wall encoding:
NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8

Rendering:
pygame

Cell coordinates:
pixel_x = x * cell_size
pixel_y = y * cell_size

Configuration contract (validated values)
-----------------------------------------
Rules: wrong type -> default value + message.
       Out of bounds -> clamped to the nearest bound + message.
       Unknown keys -> ignored.

### Global values

| Key                     | Type | Default           | Valid range            | Notes                                   |
|-------------------------|------|-------------------|------------------------|-----------------------------------------|
| highscore_filename      | str  | "highscores.json" | non-empty string       | path of the highscore file              |
| lives                   | int  | 3                 | 1 – 9                  | lives at game start                     |
| pacgum                  | int  | 500               | 1 – accessible cells   | pacgums placed per level (see note)     |
| points_per_pacgum       | int  | 10                | 0 – 10000              |                                         |
| points_per_super_pacgum | int  | 50                | 0 – 10000              |                                         |
| points_per_ghost        | int  | 200               | 0 – 10000              |                                         |
| seed                    | int  | 42                | >= 1                   | used for level 1 only, others random    |
| level_max_time          | int  | 90                | 10 – 600               | seconds, same limit for every level     |
| level                   | list | 10 default levels | >= 10 levels           | padded with default levels if < 10 (D5) |

### Per-level values (each item of "level")

| Key    | Type | Default | Valid range | Notes                              |
|--------|------|---------|-------------|------------------------------------|
| width  | int  | 21      | 14 – 40     | min needed for the "42" pattern    |
| height | int  | 15      | 10 – 40     | min needed for the "42" pattern    |

An invalid level entry (not an object) is skipped with a message.

State machine
-------------

### Principle

A single main loop (`App`) runs the whole program. Each frame it:
1. computes `dt` = real time since the previous frame (`time.monotonic()`),
   capped at 0.1 s,
2. forwards every pygame event to the current state (except the window close
   event, handled by `App` itself: it quits from any state),
3. calls `update(dt)`, then `draw(screen)` on the current state, then flips
   the display,
4. performs the transition if the current state requested one.

Only `App` reads the real time. Only `App` changes the current state.

### State interface

Every state implements:
- `handle_event(event)`: react to user input
- `update(dt)`: advance the state by `dt` seconds
- `draw(screen)`: draw the state
- `next_state: StateName | None`: set by the state to request a transition
  (`None` = stay in the current state)

`StateName` is an Enum:
MENU, PLAYING, PAUSED, RESUME, END, HIGHSCORES, INSTRUCTIONS, QUIT

### States

| State        | Shows                                         | Keys                                    | Can request                                      |
|--------------|-----------------------------------------------|-----------------------------------------|--------------------------------------------------|
| Menu         | title, menu entries, top highscores           | arrows + Enter                          | PLAYING, HIGHSCORES, INSTRUCTIONS, QUIT          |
| Playing      | maze, entities, HUD                           | arrows / WASD, Escape = pause, cheats   | PAUSED, PLAYING (next level), END                |
| Paused       | frozen game behind a pause menu               | arrows + Enter, Escape = resume         | RESUME, MENU                                     |
| End          | "Game Over" or "Victory", final score, name   | letters, digits, space, Backspace, Enter| MENU (after saving the highscore)                |
| Highscores   | top 10 scores                                 | Enter / Escape                          | MENU                                             |
| Instructions | controls and rules                            | Enter / Escape                          | MENU                                             |

Game Over and Victory screens are the same `End` state: only the title
changes, based on `session.won`.

### Transitions

    Menu ──Start──────────> Playing ──Escape──> Paused ──Resume──> Playing
     │                        │                   └──Main menu──> Menu
     ├──Highscores──> Highscores ──> Menu
     ├──Instructions──> Instructions ──> Menu
     └──Exit──> QUIT

    Playing ──level complete, not last──> Playing (next level)
    Playing ──last level complete──> End (victory) ──name saved──> Menu
    Playing ──no lives left──> End (game over) ──name saved──> Menu

### What App does for each transition

- PLAYING: always creates a **new** Playing state for `session.level_index`
  (new maze, new entities, new game clock).
- PAUSED: creates a Paused state that keeps a reference to the current
  Playing state. Paused draws that Playing state (frozen) behind its menu.
- RESUME: the current state becomes the Playing instance kept by Paused
  (same game, same clock, nothing recreated).
- END: creates an End state reading the session.
- MENU: creates a Menu state and discards the session.
- QUIT: leaves the main loop.

### Shared data

- `Config`: loaded once at startup, read-only, given to the states.
- `GameSession`: `score`, `lives`, `level_index`, `won`. Created by App when
  Menu requests PLAYING (Start), discarded when going back to Menu.
  Read and written by Playing, read by Paused (HUD) and End.
- Highscores: loaded once at startup and owned by App. End adds the new
  entry and saves the file. Menu and Highscores only display them.

### Game clock

Playing owns its own clock, `game_time` (seconds, starts at 0 for each
level), increased by `dt` in `update`. It replaces `time.monotonic()`
everywhere in the gameplay code (`now = game_time`). Paused never calls
`Playing.update`, so every duration (edible mode, ghost respawn, movement
delays, level timer) freezes automatically during a pause.

The level timer uses `timer_start` (value of `game_time` when the timer
last started):
remaining time = `config.level_max_time - (game_time - timer_start)`.

### Gameplay decisions

- Level complete: `session.level_index += 1`. If it was the last level,
  `session.won = True` and END. Otherwise PLAYING (next level).
- No lives left: `session.won = False` and END.
- Time out (D2): counts as a death. The player loses a life, the player
  and ghosts go back to their spawn, and the level timer restarts
  (`timer_start = game_time`). Pacgums already eaten stay eaten.
- Level 1 uses `config.seed`. Next levels use a random seed (0 for the
  generator).