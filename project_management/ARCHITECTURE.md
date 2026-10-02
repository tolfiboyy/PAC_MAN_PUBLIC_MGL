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