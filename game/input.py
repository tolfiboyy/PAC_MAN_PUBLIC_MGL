import pygame
from .cheats import CheatState

CHEATINPUT = {
    "speed_input": pygame.K_F1,
    "invincibility_input": pygame.K_F2,
    "freeze_input": pygame.K_F3,
    "skip_level_input": pygame.K_F4,
}


def get_direction(event: pygame.event.Event) -> str | None:

    '''Gets direction from the user'''

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

    '''Handles and modifies the cheat class if the key for a cheat
    is pressed'''

    if event.type != pygame.KEYDOWN:
        return 0.0

    if event.key == CHEATINPUT["speed_input"]:
        cheats.toggle_speed()
    if event.key == CHEATINPUT["invincibility_input"]:
        cheats.toggle_invincibility()
    if event.key == CHEATINPUT["freeze_input"]:
        frozen_duration = cheats.toggle_timer(now)
        return frozen_duration
    if event.key == CHEATINPUT["skip_level_input"]:
        cheats.request_skip_level()
    return 0.0
