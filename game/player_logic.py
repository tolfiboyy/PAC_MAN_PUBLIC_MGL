from .entities.player import Player
from .movement import move_entity, can_move


def update_player_render(
        player: Player,
        dt: float,
        speed: float
        ) -> None:

    step = speed * dt

    if player.render_x < player.target_x:
        player.render_x = min(
            player.render_x + step,
            float(player.target_x)
        )
    elif player.render_x > player.target_x:
        player.render_x = max(
            player.render_x - step,
            float(player.target_x)
        )

    if player.render_y < player.target_y:
        player.render_y = min(
            player.render_y + step,
            float(player.target_y)
        )
    elif player.render_y > player.target_y:
        player.render_y = max(
            player.render_y - step,
            float(player.target_y)
        )

    if (
            player.render_x == float(player.target_x)
            and player.render_y == float(player.target_y)
            ):
        player.x = player.target_x
        player.y = player.target_y


def update_player(
        player: Player,
        maze: list[list[int]]
        ) -> None:

    if (
            player.x != player.target_x
            or player.y != player.target_y
            ):
        return

    if player.requested_direction is not None:
        if can_move(
                player.x,
                player.y,
                player.requested_direction,
                maze
                ):
            player.direction = player.requested_direction
            player.facing_direction = player.direction

    if player.direction is not None:
        if can_move(
                player.x,
                player.y,
                player.direction,
                maze
                ):
            player.target_x, player.target_y = move_entity(
                player.x,
                player.y,
                player.direction,
                maze
            )
        else:
            player.direction = None
