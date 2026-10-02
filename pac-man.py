import pygame
import time
from game.input import get_direction
from game.collectibles import (create_pacgums, eat_pacgums, is_level_complete)
from game.entities.ghost import Ghost
from game.entities.player import Player
from game.collisions import (is_collision)
from game.rendering import (draw_game)
from game.ghost_logic import (update_ghost, assign_flee_target)
from game.player_logic import (update_player)
from game.level_logic import (generate_level, setup_level)
import sys
from config import ConfigError, Config

pygame.init()


def main():

    try:
        if len(sys.argv) != 2:
            raise ConfigError("Wrong command, exemple : python3 pac-man.py *config file name*")
        elif not sys.argv[1].endswith(".json"):
            raise ConfigError("File must be a JSON !")
        config = Config.from_file(sys.argv[1])
    except ConfigError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    level_index: int = 0
    level: int = 1
    maze = generate_level(config, level_index)

    height = len(maze)
    width = len(maze[0])

    cell_size = 60
    sprite_size = 35

    hud_height: int = 50
    screen = pygame.display.set_mode(
        (width * cell_size, height * cell_size + hud_height))
    font = pygame.font.Font(None, 30)
    pygame.display.set_caption("pac_man")

    #  load des images
    try:
        pacman_image = pygame.image.load("assets/pacman.png")

        blinky_image = pygame.image.load("assets/blinky.png")

        pinky_image = pygame.image.load("assets/pinky.png")

        inky_image = pygame.image.load("assets/inky.png")

        clyde_image = pygame.image.load("assets/clyde.png")

        frightened_image = pygame.image.load("assets/frightened.png")

    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    ghost_images = [blinky_image, pinky_image, inky_image, clyde_image]

    #  position des images pour centrage

    if width % 2 == 0:
        player = Player(width // 2 - 1, height // 2)
        player_spawn = (width // 2 - 1, height // 2)
    else:
        player = Player(width // 2, height // 2)
        player_spawn = (width // 2, height // 2)

    blinky = Ghost(0, 0, "direct")
    pinky = Ghost(width - 1, 0, "ahead")
    inky = Ghost(width - 1, height - 1, "vector")
    clyde = Ghost(0, height - 1, "distance")

    ghosts = [blinky, pinky, inky, clyde]

    pacgums, super_pacgums = create_pacgums(maze, config)

    last_move = time.monotonic()
    level_start_time = time.monotonic()
    edible_duration: float = 5.0
    move_delay: float = 0.25
    respawn_delay: float = 2.0

    ghost_start_time = time.monotonic()

    for ghost in ghosts:
        ghost.last_move = ghost_start_time

    ghost_move_delay: float = 1

    score: int = 0
    lives: int = config.lives

    running = True

    while running:

        now = time.monotonic()

        elapsed_time = int(now - level_start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            new_direction = get_direction(event)

            if new_direction is not None:
                player.requested_direction = new_direction

        last_move = update_player(player, maze, now, last_move, move_delay)

        for ghost in ghosts:
            update_ghost(
                ghost, blinky,
                maze,
                player,
                now,
                ghost_move_delay)

        player_position = (player.x, player.y)

        points, ate_super = eat_pacgums(
            pacgums, super_pacgums, player_position, config)

        if ate_super:
            assign_flee_target(ghosts, maze)

            for ghost in ghosts:
                ghost.edible = True
                ghost.edible_until = now + edible_duration
                print(ghost.edible)

        for ghost in ghosts:
            if ghost.edible and now >= ghost.edible_until:
                ghost.edible = False
                ghost.ghost_flee_target = None
                print("not edible anymore")

        score += points

        for ghost in ghosts:

            if ghost.respawning:
                continue

            ghost_position = (ghost.x, ghost.y)

            if is_collision(player_position, ghost_position):
                if ghost.edible:
                    score += config.points_per_ghost

                    ghost.respawning = True
                    ghost.respawn_until = now + respawn_delay

                    ghost.edible = False
                    ghost.x, ghost.y = ghost.spawn
                    ghost.direction = None
                    ghost.ghost_flee_target = None

                    ghost.last_move = now

                    print("Ghost EATEN")

                else:
                    lives -= 1

                    player.x, player.y = player_spawn
                    player.direction = None
                    player.requested_direction = None
                    last_move = now

                    for current_ghost in ghosts:
                        current_ghost.x, current_ghost.y = current_ghost.spawn
                        current_ghost.direction = None
                        current_ghost.last_move = now

                    print("COLLISION")

                    if lives == 0:
                        print("Game over")
                        running = False

                    break

        player_position = (player.x, player.y)

        if is_level_complete(pacgums, super_pacgums):
            print("LEVEL COMPLETE")

            if level_index + 1 >= len(config.level):
                print("GAME COMPLETE")
                running = False

            else:
                level_index += 1
                level = level_index + 1
                lives = config.lives
                level_start_time = now

                (
                    maze,
                    width,
                    height,
                    player_spawn,
                    ghosts,
                    pacgums,
                    super_pacgums
                ) = setup_level(config, level_index, player, now)

                blinky = ghosts[0]

                screen = pygame.display.set_mode(
                    (width * cell_size, height * cell_size + hud_height))

                last_move = now

        draw_game(
            screen, maze,
            pacgums, super_pacgums,
            player_position, ghosts,
            pacman_image, ghost_images,
            frightened_image,
            cell_size, sprite_size,
            score, lives, font,
            hud_height, elapsed_time,
            level)

    pygame.quit()


if __name__ == "__main__":
    main()
