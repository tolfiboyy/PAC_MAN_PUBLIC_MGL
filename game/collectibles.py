from config import Config
import random


def create_pacgums(
        maze: list[list[int]],
        config: Config
        ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:

    height = len(maze)
    width = len(maze[0])

    corners = {
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1)
        }

    if width % 2 == 0:
        spawn = (width // 2 - 1, height // 2)
    else:
        spawn = (width // 2, height // 2)

    available_cells: list[tuple[int, int]] = []

    for y in range(height):
        for x in range(width):
            if (
                    maze[y][x] != 15
                    and (x, y) not in corners
                    and (x, y) != spawn
                    ):
                available_cells.append((x, y))

    pacgum_count = min(
        config.pacgum,
        len(available_cells)
    )

    rng = random.Random(config.seed)

    selected_cells = rng.sample(
        available_cells,
        pacgum_count
    )

    pacgums = set(selected_cells)
    super_pacgums = corners.copy()

    return pacgums, super_pacgums


def eat_pacgums(
        pacgums: set[tuple[int, int]],
        super_pacgums: set[tuple[int, int]],
        player_position: tuple[int, int],
        config: Config
        ) -> tuple[int, bool]:

    if player_position in pacgums:
        pacgums.remove(player_position)
        return config.points_per_pacgum, False
    elif player_position in super_pacgums:
        super_pacgums.remove(player_position)
        return config.points_per_super_pacgum, True

    return 0, False


def is_level_complete(
        pacgums: set[tuple[int, int]],
        super_pacgums: set[tuple[int, int]]
        ) -> bool:

    if not pacgums and not super_pacgums:
        return True

    return False
