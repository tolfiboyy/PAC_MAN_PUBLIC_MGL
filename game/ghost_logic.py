from .entities.ghost import Ghost
from .entities.player import Player
from .pathfinding import (shortest_path, get_direction_from_path)
from .movement import move_entity
import random


def assign_flee_target(
        ghosts: list[Ghost],
        maze: list[list[int]]
        ) -> None:

    height = len(maze)
    width = len(maze[0])

    corners = [
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1)
    ]

    random.shuffle(corners)

    for ghost, corner in zip(ghosts, corners):
        ghost.ghost_flee_target = corner


def choose_chase_target(
        ghost: Ghost,
        blinky: Ghost,
        player: Player,
        maze: list[list[int]]
        ) -> tuple[int, int]:

    height = len(maze)
    width = len(maze[0])

    if ghost.behavior == "direct":
        return (player.x, player.y)

    elif ghost.behavior == "distance":
        distance = (
            abs(ghost.x - player.x)
            + abs(ghost.y - player.y)
            )

        if distance >= 8:
            return player.x, player.y
        else:
            return ghost.spawn

    elif ghost.behavior == "vector":
        pivot_x = player.x
        pivot_y = player.y

        if player.direction == "right":
            pivot_x += 2
        elif player.direction == "left":
            pivot_x -= 2
        elif player.direction == "up":
            pivot_y -= 2
        elif player.direction == "down":
            pivot_y += 2

        vector_x = pivot_x - blinky.x
        vector_y = pivot_y - blinky.y

        target_x = pivot_x + vector_x
        target_y = pivot_y + vector_y

        if 0 <= target_x < width and 0 <= target_y < height:
            return (target_x, target_y)

    elif ghost.behavior == "ahead":

        ahead_x, ahead_y = player.x, player.y

        if player.direction == "right":
            ahead_x += 3
        elif player.direction == "left":
            ahead_x -= 3
        elif player.direction == "up":
            ahead_y -= 3
        elif player.direction == "down":
            ahead_y += 3

        if 0 <= ahead_x < width and 0 <= ahead_y < height:
            return (ahead_x, ahead_y)

    return (player.x, player.y)


def update_ghost_render(
        ghost: Ghost,
        dt: float,
        speed: float
        ) -> None:

    step = speed * dt

    if ghost.render_x < ghost.target_x:
        ghost.render_x = min(
            ghost.render_x + step,
            float(ghost.target_x)
        )
    elif ghost.render_x > ghost.target_x:
        ghost.render_x = max(
            ghost.render_x - step,
            float(ghost.target_x)
        )

    if ghost.render_y < ghost.target_y:
        ghost.render_y = min(
            ghost.render_y + step,
            float(ghost.target_y)
        )
    elif ghost.render_y > ghost.target_y:
        ghost.render_y = max(
            ghost.render_y - step,
            float(ghost.target_y)
        )

    if (
            ghost.render_x == float(ghost.target_x)
            and ghost.render_y == float(ghost.target_y)
            ):
        ghost.x = ghost.target_x
        ghost.y = ghost.target_y


def update_ghost(
        ghost: Ghost,
        blinky: Ghost,
        maze: list[list[int]],
        player: Player,
        now: float
        ) -> None:

    player_position = (player.x, player.y)

    if ghost.respawning:
        if now < ghost.respawn_until:
            return
        ghost.respawning = False

    if (
            ghost.x != ghost.target_x
            or ghost.y != ghost.target_y
            ):
        return

    if ghost.edible and ghost.ghost_flee_target is not None:
        target = ghost.ghost_flee_target
    else:
        target = choose_chase_target(ghost, blinky, player, maze)

    path = shortest_path(
        maze,
        (ghost.x, ghost.y),
        target
        )

    if not path:
        if ghost.edible:
            target = ghost.spawn
        else:
            target = player_position

        path = shortest_path(maze, (ghost.x, ghost.y), target)

    if len(path) >= 2:
        ghost_direction = get_direction_from_path(path[0], path[1])

        if ghost_direction is not None:
            ghost.direction = ghost_direction

            ghost.target_x, ghost.target_y = move_entity(
                ghost.x,
                ghost.y,
                ghost_direction,
                maze
                )


def update_frightened_status(
        ghosts: list[Ghost],
        ate_super: bool,
        now: float,
        edible_duration: float,
        maze: list[list[int]]
        ) -> None:

    if ate_super:
        assign_flee_target(ghosts, maze)

        for ghost in ghosts:
            ghost.edible = True
            ghost.edible_until = now + edible_duration

    for ghost in ghosts:
        if ghost.edible and now >= ghost.edible_until:
            ghost.edible = False
            ghost.ghost_flee_target = None
