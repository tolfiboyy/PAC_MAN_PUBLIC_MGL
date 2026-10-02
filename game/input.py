import pygame


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
