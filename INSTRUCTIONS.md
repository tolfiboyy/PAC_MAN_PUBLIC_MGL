PAC-MAN - QUICK INSTRUCTIONS
============================

Launch from source:
  make install
  make run

Launch packaged build:
  ./pacman config.json

CONTROLS
--------
Arrow keys : move Pac-Man
ESC/PAUSE  : pause
END        : end the current game
TAB        : show/hide the cheat sheet

CHEATS (peer-review helpers)
----------------------------
F1 : increased player speed
F2 : invincibility
F3 : freeze/unfreeze the level timer
F4 : skip current level

MENU
----
Arrow keys : navigate
ENTER      : select

CONFIGURATION
-------------
The game expects one JSON configuration file.
Lines beginning with # are accepted as comments.
Invalid or missing values are handled with safe defaults/clamping.

HIGHSCORES
----------
At the end of a normal game, enter a valid name and press ENTER to save.
Runs using cheats are intentionally not registered in the highscore table.
