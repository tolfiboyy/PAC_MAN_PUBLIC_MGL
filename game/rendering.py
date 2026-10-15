from .constants import (
    WHITE, BLACK, ELECTRIC, WALL_OFFSET, NORTH, EAST, SOUTH, WEST)
from .entities.ghost import Ghost
from .entities.player import Player
import pygame
import math


def draw_horizontal_line(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        start_x: int,
        end_x: int,
        y: int
        ) -> None:

    '''Draws only one line when called two times
    by the functions under it creates our
    double sided walls, it works by drawing pixel by pixel
    in range of one side of the cell'''

    for pixel in range(start_x, end_x + 1):
        screen.set_at((pixel, y), color)


def draw_vertical_line(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        start_y: int,
        end_y: int,
        x: int
        ) -> None:

    '''Draws only one line when called two times
    by the functions under this one it creates our
    double sided walls'''

    for pixel in range(start_y, end_y + 1):
        screen.set_at((x, pixel), color)


def draw_double_horizontal_wall(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        start_x: int,
        end_x: int,
        y: int) -> None:

    '''Draws the horizontal wall with two lines'''

    draw_horizontal_line(
        screen, color, start_x + WALL_OFFSET,
        end_x - WALL_OFFSET, y - WALL_OFFSET)
    draw_horizontal_line(
        screen, color, start_x + WALL_OFFSET,
        end_x - WALL_OFFSET, y + WALL_OFFSET)


def draw_double_vertical_wall(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        start_y: int,
        end_y: int,
        x: int) -> None:

    '''This draws the vertical walls with 2 lines'''

    draw_vertical_line(
        screen, color, start_y + WALL_OFFSET,
        end_y - WALL_OFFSET, x - WALL_OFFSET)
    draw_vertical_line(
        screen, color, start_y + WALL_OFFSET,
        end_y - WALL_OFFSET, x + WALL_OFFSET)


def draw_circles(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        center_x: int,
        center_y: int,
        radius: int
        ) -> None:

    '''draws circle i guess'''

    for y in range(center_y - radius, center_y + radius + 1):
        for x in range(center_x - radius, center_x + radius + 1):
            dx = x - center_x
            dy = y - center_y

            if dx * dx + dy * dy <= radius * radius:
                screen.set_at((x, y), color)


def draw_corners(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        pixel_x: int,
        pixel_y: int,
        cell_size: int,
        corner: str
        ) -> None:

    '''Draws the 90 degree angle of two walls'''

    if corner not in (
        "top_right",
        "bottom_right",
        "top_left",
        "bottom_left"
            ):
        return

    is_right = "right" in corner
    is_bottom = "bottom" in corner

    sign_x = 1 if is_right else -1
    sign_y = 1 if is_bottom else -1

    corner_x = pixel_x + cell_size if is_right else pixel_x
    corner_y = pixel_y + cell_size if is_bottom else pixel_y

    center_x = corner_x - sign_x * WALL_OFFSET
    center_y = corner_y - sign_y * WALL_OFFSET

    radius = WALL_OFFSET * 2

    previous_y: int | None = None

    for dx in range(radius + 1):
        dy = round(math.sqrt(radius * radius - dx * dx))

        current_x = center_x + sign_x * dx
        current_y = center_y + sign_y * dy

        if previous_y is not None:
            draw_vertical_line(
                screen,
                color,
                min(previous_y, current_y),
                max(previous_y, current_y),
                current_x
            )
        else:
            screen.set_at((current_x, current_y), color)

        previous_y = current_y


def draw_right_cap(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        end_x: int,
        y: int
        ) -> None:

    '''Draws the rounded edge of a wall'''

    center_x = end_x - WALL_OFFSET
    center_y = y
    radius = WALL_OFFSET

    for dx in range(radius + 1):
        dy = round(math.sqrt(radius * radius - dx * dx))

        current_x = center_x + dx

        top_y = center_y - dy
        bottom_y = center_y + dy

        screen.set_at((current_x, top_y), color)
        screen.set_at((current_x, bottom_y), color)


def draw_left_cap(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        start_x: int,
        y: int
        ) -> None:

    '''Draws the rounded edge of a wall'''

    center_x = start_x + WALL_OFFSET
    center_y = y
    radius = WALL_OFFSET

    for dx in range(radius + 1):
        dy = round(math.sqrt(radius * radius - dx * dx))

        current_x = center_x - dx

        top_y = center_y - dy
        bottom_y = center_y + dy

        screen.set_at((current_x, top_y), color)
        screen.set_at((current_x, bottom_y), color)


def draw_top_cap(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        x: int,
        start_y: int
        ) -> None:

    '''Draws the rounded edge of a wall'''

    center_x = x
    center_y = start_y + WALL_OFFSET
    radius = WALL_OFFSET

    for dy in range(radius + 1):
        dx = round(math.sqrt(radius * radius - dy * dy))

        current_y = center_y - dy

        left_x = center_x - dx
        right_x = center_x + dx

        screen.set_at((left_x, current_y), color)
        screen.set_at((right_x, current_y), color)


def draw_bottom_cap(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        x: int,
        end_y: int
        ) -> None:

    '''A cap is the rounded edge of a wall. This one draws the bottom one'''

    center_x = x
    center_y = end_y - WALL_OFFSET
    radius = WALL_OFFSET

    for dy in range(radius + 1):
        dx = round(math.sqrt(radius * radius - dy * dy))

        current_y = center_y + dy

        left_x = center_x - dx
        right_x = center_x + dx

        screen.set_at((left_x, current_y), color)
        screen.set_at((right_x, current_y), color)


def draw_pacgums(
        pacgums: set[tuple[int, int]],
        screen: pygame.Surface,
        cell_size: int,
        hud_height: int
        ) -> None:

    '''Wonder what it draws ?'''

    for x, y in pacgums:
        center_x = x * cell_size + cell_size // 2
        center_y = y * cell_size + cell_size // 2 + hud_height

        draw_circles(screen, WHITE, center_x, center_y, 3)


def draw_super_pacgums(
        super_pacgums: set[tuple[int, int]],
        screen: pygame.Surface,
        cell_size: int,
        hud_height: int
        ) -> None:

    '''draws the super pacgums, yea'''

    for x, y in super_pacgums:

        center_x = x * cell_size + cell_size // 2
        center_y = y * cell_size + cell_size // 2 + hud_height

        draw_circles(screen, WHITE, center_x, center_y, 7)


def draw_cell(
        x: int,
        y: int,
        cell: int,
        cell_size: int,
        color: tuple[int, int, int],
        screen: pygame.Surface,
        y_offset: int,
        maze: list[list[int]]
        ) -> None:

    '''This function is pretty big, it draws what makes a cell.
    Including the walls but also some parameters draws the
    rounded corners of a wall to make the game pretty.'''

    pixel_x = x * cell_size
    pixel_y = y * cell_size + y_offset

    if cell & NORTH:
        draw_double_horizontal_wall(
            screen, color, pixel_x, pixel_x + cell_size, pixel_y)

        continues_right = (
            x + 1 < len(maze[0])) and bool(maze[y][x + 1] & NORTH)

        continues_down_right = bool(cell & EAST)
        continues_up_right = (y > 0 and bool(maze[y - 1][x] & EAST))

        if (
                not continues_right
                and not continues_down_right
                and not continues_up_right
                ):
            draw_right_cap(screen, color, pixel_x + cell_size, pixel_y)

        continues_left = (x > 0 and bool(maze[y][x - 1] & NORTH))

        continues_down_left = bool(cell & WEST)
        continues_up_left = (y > 0 and bool(maze[y - 1][x] & WEST))

        if (
                not continues_left
                and not continues_down_left
                and not continues_up_left
                ):
            draw_left_cap(screen, color, pixel_x, pixel_y)

    if cell & EAST:
        draw_double_vertical_wall(
            screen, color, pixel_y, pixel_y + cell_size, pixel_x + cell_size)

    if cell & SOUTH:
        draw_double_horizontal_wall(
            screen, color, pixel_x, pixel_x + cell_size, pixel_y + cell_size)

    if cell & WEST:
        draw_double_vertical_wall(
            screen, color, pixel_y, pixel_y + cell_size, pixel_x)

        continues_up = (y > 0 and bool(maze[y - 1][x] & WEST))
        continues_right_top = bool(cell & NORTH)
        continues_left_top = (x > 0 and bool(maze[y][x - 1] & NORTH))

        if (
                not continues_up
                and not continues_right_top
                and not continues_left_top
                ):
            draw_top_cap(screen, color, pixel_x, pixel_y)

        continues_down = (y + 1 < len(maze) and bool(maze[y + 1][x] & WEST))
        continues_right_bottom = bool(cell & SOUTH)
        continues_left_bottom = (x > 0 and bool(maze[y][x - 1] & SOUTH))

        if (
                not continues_down
                and not continues_right_bottom
                and not continues_left_bottom
                ):
            draw_bottom_cap(screen, color, pixel_x, pixel_y + cell_size)

    if cell & NORTH and cell & EAST:
        draw_corners(
            screen, color, pixel_x, pixel_y, cell_size, "top_right")

    if cell & EAST and cell & SOUTH:
        draw_corners(
            screen, color, pixel_x, pixel_y, cell_size, "bottom_right")

    if cell & SOUTH and cell & WEST:
        draw_corners(
            screen, color, pixel_x, pixel_y, cell_size, "bottom_left")

    if cell & WEST and cell & NORTH:
        draw_corners(
            screen, color, pixel_x, pixel_y, cell_size, "top_left")


def draw_hud(
        screen: pygame.Surface,
        font: pygame.font.Font,
        score: int,
        lives: int,
        remaining_time: int,
        level: int
        ) -> None:

    '''draws the HUD, pretty self explanatory'''

    score_surface = font.render(f"Score: {score}", True, WHITE)
    lives_surface = font.render(f"Lives: {lives}", True, WHITE)
    time_surface = font.render(f"Time: {remaining_time}", True, WHITE)
    level_surface = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_surface, (50, 5))
    screen.blit(lives_surface, (250, 5))
    screen.blit(time_surface, (450, 5))
    screen.blit(level_surface, (650, 5))


def draw_game(
        screen: pygame.Surface,
        maze: list[list[int]],
        pacgums: set[tuple[int, int]],
        super_pacgums: set[tuple[int, int]],
        player: Player,
        ghosts: list[Ghost],
        pacman_images: dict[str, pygame.Surface],
        ghost_images: list[dict[str, pygame.Surface]],
        frightened_image: pygame.Surface,
        cell_size: int,
        sprite_size: int,
        score: int,
        lives: int,
        font: pygame.font.Font,
        hud_height: int,
        remaining_time: int,
        level: int
        ) -> None:

    '''Renders the whole game, with a list of all the parameters needed'''

    screen.fill(BLACK)

    height = len(maze)
    width = len(maze[0])

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]
            draw_cell(
                x, y, cell, cell_size, ELECTRIC, screen, hud_height, maze)

    draw_pacgums(pacgums, screen, cell_size, hud_height)
    draw_super_pacgums(super_pacgums, screen, cell_size, hud_height)

    player_pixel_x = int(
        player.render_x * cell_size
        + (cell_size - sprite_size) // 2
        )
    player_pixel_y = int(
        player.render_y * cell_size
        + (cell_size - sprite_size) // 2
        + hud_height
        )

    #  calage bien au centre des images

    for ghost, ghost_images_by_direction in zip(ghosts, ghost_images):

        ghost_pixel_x = int((
            ghost.render_x * cell_size)
            + (cell_size - sprite_size) // 2)
        ghost_pixel_y = int((
            ghost.render_y * cell_size)
            + (cell_size - sprite_size) // 2 + hud_height)

        if ghost.edible:
            screen.blit(frightened_image, (ghost_pixel_x, ghost_pixel_y))
        else:
            direction = ghost.direction

            if direction is None:
                direction = "right"

            current_ghost_image = ghost_images_by_direction[direction]

            screen.blit(
                current_ghost_image, (ghost_pixel_x, ghost_pixel_y))

    current_pacman_image = pacman_images[player.facing_direction]

    screen.blit(current_pacman_image, (player_pixel_x, player_pixel_y))

    draw_hud(screen, font, score, lives, remaining_time, level)
