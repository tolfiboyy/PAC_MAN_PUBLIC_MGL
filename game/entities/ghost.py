class Ghost:
    def __init__(
            self,
            x: int,
            y: int,
            behavior: str
            ) -> None:

        self.x: int = x
        self.y: int = y

        self.target_x: int = x
        self.target_y: int = y

        self.render_x: float = float(x)
        self.render_y: float = float(y)

        self.edible: bool = False
        self.edible_until: float = 0.0

        self.respawning: bool = False
        self.respawn_until: float = 0.0

        self.behavior: str = behavior

        self.spawn: tuple[int, int] = (x, y)
        self.ghost_flee_target: tuple[int, int] | None = None
        self.last_move: float = 0.0
        self.direction: str | None = None
