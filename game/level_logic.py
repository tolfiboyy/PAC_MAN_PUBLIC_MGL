from generator import MazeGenerator
from config import Config
from .entities.player import Player
from .entities.ghost import Ghost
from .collectibles import create_pacgums


def generate_level(
        config: Config,
        level_index: int
        ) -> list[list[int]]:

    level_config = config.level[level_index]

    generator = MazeGenerator(
        (level_config.width, level_config.height),
        False,
        (0, 0),
        (2, 2),
        config.seed
    )

    return generator.maze


def setup_level(
        config: Config,
        level_index: int
        ) -> (
            tuple[
                list[list[int]],
                int, int,
                tuple[int, int],
                Player, list[Ghost],
                set[tuple[int, int]],
                set[tuple[int, int]]]
                ):

    maze = generate_level(config, level_index)

    height = len(maze)
    width = len(maze[0])

    if width % 2 == 0:
        player_spawn = (width // 2 - 1, height // 2)
    else:
        player_spawn = (width // 2, height // 2)

    player = Player(player_spawn[0], player_spawn[1])

    blinky = Ghost(0, 0, "direct")
    pinky = Ghost(width - 1, 0, "ahead")
    inky = Ghost(width - 1, height - 1, "vector")
    clyde = Ghost(0, height - 1, "distance")

    ghosts = [blinky, pinky, inky, clyde]

    pacgums, super_pacgums = create_pacgums(maze, config)

    return (
        maze,
        width,
        height,
        player_spawn,
        player,
        ghosts,
        pacgums,
        super_pacgums
    )
