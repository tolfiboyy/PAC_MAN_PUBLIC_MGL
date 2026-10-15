from .constants import NORTH, EAST, WEST, SOUTH


def can_move(
        x: int,
        y: int,
        direction: str,
        maze: list[list[int]]
        ) -> bool:

    '''Returns true or false if the next direction is possible'''

    cell = maze[y][x]

    if direction == "up":
        return (cell & NORTH) == 0
    if direction == "down":
        return (cell & SOUTH) == 0
    if direction == "left":
        return (cell & WEST) == 0
    if direction == "right":
        return (cell & EAST) == 0

    return False


def move_entity(
        player_x: int,
        player_y: int,
        direction: str,
        maze: list[list[int]]
        ) -> tuple[int, int]:

    '''Moves ghost, or pacman if it's possible'''

    if not can_move(player_x, player_y, direction, maze):
        return player_x, player_y

    if direction == "up":
        player_y -= 1

    elif direction == "right":
        player_x += 1

    elif direction == "down":
        player_y += 1

    elif direction == "left":
        player_x -= 1

    return player_x, player_y


def get_available_directions(
        x: int,
        y: int,
        maze: list[list[int]]
        ) -> list[str]:

    '''Gets every possible directions on a cell,
    used by the ghosts'''

    directions: list[str] = []

    if can_move(x, y, "up", maze):
        directions.append("up")

    if can_move(x, y, "right", maze):
        directions.append("right")

    if can_move(x, y, "down", maze):
        directions.append("down")

    if can_move(x, y, "left", maze):
        directions.append("left")

    return directions
