class Player:
    def __init__(
            self,
            x: int,
            y: int,
            ) -> None:

        self.x = x
        self.y = y
        self.direction: str | None = None
        self.requested_direction: str | None = None
