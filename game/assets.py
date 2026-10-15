import pygame
import sys


def load_images(
            ) -> (
                tuple[
                    dict[str, pygame.Surface],
                    pygame.Surface,
                    list[dict[str, pygame.Surface]]]
                    ):

    '''I wonder what this one does. Actually all ghosts and pacman
    are loaded into four differents images to respect the MLX library
    criteria in the subject. We can't have only one image that rotates
    depend on the angle. It was the system at first, but then we wanted
    the eyes to moves also depending on the direction'''

    try:

        # pacman
        pac_man_up = pygame.image.load("assets/pacman_up.png")
        pac_man_down = pygame.image.load("assets/pacman_down.png")
        pac_man_left = pygame.image.load("assets/pacman_left.png")
        pac_man_right = pygame.image.load("assets/pacman_right.png")

        #  blinky
        blinky_up = pygame.image.load("assets/blinky_up.png")
        blinky_down = pygame.image.load("assets/blinky_down.png")
        blinky_left = pygame.image.load("assets/blinky_left.png")
        blinky_right = pygame.image.load("assets/blinky_right.png")
        #  clyde
        clyde_up = pygame.image.load("assets/clyde_up.png")
        clyde_down = pygame.image.load("assets/clyde_down.png")
        clyde_left = pygame.image.load("assets/clyde_left.png")
        clyde_right = pygame.image.load("assets/clyde_right.png")
        #  pinky
        pinky_up = pygame.image.load("assets/pinky_up.png")
        pinky_down = pygame.image.load("assets/pinky_down.png")
        pinky_left = pygame.image.load("assets/pinky_left.png")
        pinky_right = pygame.image.load("assets/pinky_right.png")
        #  inky
        inky_up = pygame.image.load("assets/inky_up.png")
        inky_down = pygame.image.load("assets/inky_down.png")
        inky_left = pygame.image.load("assets/inky_left.png")
        inky_right = pygame.image.load("assets/inky_right.png")

        pacman_images = {
            "right": pac_man_right,
            "up": pac_man_up,
            "left": pac_man_left,
            "down": pac_man_down
        }

        blinky_images = {
            "up": blinky_up,
            "down": blinky_down,
            "left": blinky_left,
            "right": blinky_right
        }

        clyde_images = {
            "up": clyde_up,
            "down": clyde_down,
            "left": clyde_left,
            "right": clyde_right
        }

        pinky_images = {
            "up": pinky_up,
            "down": pinky_down,
            "left": pinky_left,
            "right": pinky_right
        }

        inky_images = {
            "up": inky_up,
            "down": inky_down,
            "left": inky_left,
            "right": inky_right
        }

        frightened_image = pygame.image.load("assets/frightened.png")

        ghost_images = [
                  blinky_images,
                  pinky_images,
                  inky_images,
                  clyde_images,
                 ]

    except (FileNotFoundError, pygame.error) as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    return pacman_images, frightened_image, ghost_images


def load_backgrounds() -> list[pygame.Surface]:
    try:
        backgrounds = [
            pygame.image.load("assets/backgrounds/menu1.png"),
            pygame.image.load("assets/backgrounds/menu2.png"),
            pygame.image.load("assets/backgrounds/menu3.png")
            ]
    except (FileNotFoundError, pygame.error) as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    return backgrounds
