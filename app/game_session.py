from dataclasses import dataclass

@dataclass
class GameSession():
    lives: int
    score: int = 0
    level_index: int = 0
    won: bool = False
    
