from .entities.ghost import (Ghost)
from .entities.player import (Player)


def reset_after_loss(
        player: Player,
        ghosts: list[Ghost],
        player_spawn: tuple[int, int]
        ) -> None:

    player.x, player.y = player_spawn
    player.target_x = player.x
    player.target_y = player.y
    player.render_x = float(player.x)
    player.render_y = float(player.y)
    player.direction = None
    player.requested_direction = None

    for current_ghost in ghosts:
        current_ghost.x, current_ghost.y = current_ghost.spawn
        current_ghost.target_x = current_ghost.x
        current_ghost.target_y = current_ghost.y
        current_ghost.render_x = float(current_ghost.x)
        current_ghost.render_y = float(current_ghost.y)

        current_ghost.direction = None
        current_ghost.edible = False
        current_ghost.respawning = False
        current_ghost.ghost_flee_target = None

        current_ghost.edible_until = 0.0
        current_ghost.respawn_until = 0.0


def reset_ghost_after_eaten(
        ghost: Ghost
        ) -> None:

    ghost.edible = False
    ghost.edible_until = 0.0
    ghost.x, ghost.y = ghost.spawn
    ghost.target_x = ghost.x
    ghost.target_y = ghost.y
    ghost.render_x = float(ghost.x)
    ghost.render_y = float(ghost.y)
    ghost.direction = None
    ghost.ghost_flee_target = None
