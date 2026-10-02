class Ghost:
    def __init__(
            self,
            x: int,
            y: int,
            behavior: str
            ) -> None:

        self.x = x
        self.y = y
        self.direction: str | None = None

        self.edible: bool = False
        self.edible_until: float = 0.0

        self.respawning: bool = False
        self.respawn_until: float = 0.0

        self.behavior = behavior

        self.spawn: tuple[int, int] = (x, y)
        self.ghost_flee_target: tuple[int, int] | None = None
        self.last_move: float = 0.0
