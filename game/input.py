import pygame
from .cheats import CheatState


def get_direction(event: pygame.event.Event) -> str | None:

    if event.type != pygame.KEYDOWN:
        return None

    if event.key == pygame.K_UP:
        return "up"
    if event.key == pygame.K_DOWN:
        return "down"
    if event.key == pygame.K_LEFT:
        return "left"
    if event.key == pygame.K_RIGHT:
        return "right"

    return None


def handle_cheat_input(
        event: pygame.event.Event,
        cheats: CheatState,
        now: float
        ) -> float:

    if event.type != pygame.KEYDOWN:
        return 0.0

    if event.key == pygame.K_F1:
        cheats.toggle_speed()
    if event.key == pygame.K_F2:
        cheats.toggle_invincibility()
    if event.key == pygame.K_F3:
        frozen_duration = cheats.toggle_timer(now)
        return frozen_duration
    if event.key == pygame.K_F4:
        cheats.request_skip_level()
    return 0.0
