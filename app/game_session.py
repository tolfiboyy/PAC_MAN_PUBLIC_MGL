from dataclasses import dataclass, field
from game.cheats import CheatState


@dataclass
class GameSession():

    """Dataclass that holds the informations of the current game session"""

    lives: int
    score: int = 0
    level_index: int = 0
    won: bool = False
    cheats: CheatState = field(default_factory=CheatState)
    cheated: bool = False
