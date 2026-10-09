class CheatState:
    def __init__(self) -> None:
        self.speed_enabled: bool = False
        self.invincible: bool = False
        self.timer_frozen: bool = False
        self.skip_level_requested: bool = False
        self.freeze_started_at: float | None = None

    def toggle_speed(self) -> None:
        self.speed_enabled = not self.speed_enabled

    def toggle_invincibility(self) -> None:
        self.invincible = not self.invincible

    def reset_timer_reference(self, now: float) -> None:
        if self.timer_frozen:
            self.freeze_started_at = now

    def get_timer_time(self, now: float) -> float:
        if self.timer_frozen and self.freeze_started_at is not None:
            return self.freeze_started_at
        return now

    def toggle_timer(self, now: float) -> float:
        if not self.timer_frozen:
            self.timer_frozen = True
            self.freeze_started_at = now
            return 0.0

        if self.freeze_started_at is None:
            self.timer_frozen = False
            return 0.0

        frozen_duration = now - self.freeze_started_at
        self.timer_frozen = False
        self.freeze_started_at = None

        return frozen_duration

    def request_skip_level(self) -> None:
        self.skip_level_requested = True

    def consume_skip_request(self) -> bool:
        if self.skip_level_requested:
            self.skip_level_requested = False
            return True
        return False

    def get_player_speed(self, player_speed: float) -> float:
        if self.speed_enabled:
            player_speed += 4
            return player_speed
        return player_speed
