from .entities.player import Player
from .entities.ghost import Ghost
from .reset_logic import (reset_ghost_after_eaten, reset_after_loss)
from config import Config


def is_collision(
        first_position: tuple[float, float],
        second_position: tuple[float, float]
        ) -> bool:

    collision_distance = 0.40

    player_x, player_y = first_position
    ghost_x, ghost_y = second_position

    dx = abs(player_x - ghost_x)
    dy = abs(player_y - ghost_y)

    distance_squared = dx * dx + dy * dy
    collision_distance_squared = collision_distance * collision_distance

    return distance_squared <= collision_distance_squared


def handle_collisions(
        player_spawn: tuple[int, int],
        player: Player,
        ghosts: list[Ghost],
        config: Config,
        now: float,
        respawn_delay: float,
        score: int,
        lives: int,
        invincible: bool
        ) -> tuple[int, int, bool]:

    player_render_position: tuple[float, float] = (
        player.render_x, player.render_y)

    life_lost: bool = False

    for ghost in ghosts:

        if ghost.respawning:
            continue

        ghost_render_position = (ghost.render_x, ghost.render_y)

        if is_collision(player_render_position, ghost_render_position):
            if ghost.edible:
                score += config.points_per_ghost

                ghost.respawning = True
                ghost.respawn_until = now + respawn_delay

                reset_ghost_after_eaten(ghost)

                return score, lives, life_lost

            elif not invincible:
                lives -= 1
                reset_after_loss(player, ghosts, player_spawn)

                life_lost = True

                return score, lives, life_lost

    return score, lives, life_lost
