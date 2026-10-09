class Player:
    def __init__(
            self,
            x: int,
            y: int,
            ) -> None:

        self.x: int = x
        self.y: int = y

        self.target_x: int = x
        self.target_y: int = y

        self.render_x: float = float(x)
        self.render_y: float = float(y)

        self.direction: str | None = None
        self.requested_direction: str | None = None

        self.facing_direction: str = "right"
