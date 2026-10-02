from .entities.player import Player
from .movement import move_entity, can_move


def update_player(
        player: Player,
        maze: list[list[int]],
        now: float,
        last_move: float,
        move_delay: float
        ) -> float:

    if now - last_move >= move_delay:

        if player.requested_direction is not None:
            if can_move(
                    player.x,
                    player.y,
                    player.requested_direction,
                    maze
                    ):
                player.direction = player.requested_direction

        if player.direction is not None:
            player.x, player.y = move_entity(
                player.x,
                player.y,
                player.direction,
                maze
                )

        last_move = now

    return last_move
