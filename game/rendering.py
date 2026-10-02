from .constants import WHITE, BLACK
from .entities.ghost import Ghost
import pygame


def draw_horizontal_line(
        screen,
        color,
        start_x: int,
        end_x: int,
        y: int
        ) -> None:

    for pixel in range(start_x, end_x + 1):
        screen.set_at((pixel, y), color)


def draw_vertical_line(
        screen,
        color,
        start_y: int,
        end_y: int,
        x: int
        ) -> None:

    for pixel in range(start_y, end_y + 1):
        screen.set_at((x, pixel), color)


def draw_circles(
        screen,
        color,
        center_x: int,
        center_y: int,
        radius: int
        ) -> None:

    for y in range(center_y - radius, center_y + radius + 1):
        for x in range(center_x - radius, center_x + radius + 1):
            dx = x - center_x
            dy = y - center_y

            if dx * dx + dy * dy <= radius * radius:
                screen.set_at((x, y), color)


def draw_pacgums(
        pacgums: set[tuple[int, int]],
        screen,
        cell_size,
        hud_height
        ) -> None:

    for x, y in pacgums:
        center_x = x * cell_size + cell_size // 2
        center_y = y * cell_size + cell_size // 2 + hud_height

        draw_circles(screen, WHITE, center_x, center_y, 3)


def draw_super_pacgums(
        super_pacgums: set[tuple[int, int]],
        screen,
        cell_size,
        hud_height: int
        ) -> None:

    for x, y in super_pacgums:

        center_x = x * cell_size + cell_size // 2
        center_y = y * cell_size + cell_size // 2 + hud_height

        draw_circles(screen, WHITE, center_x, center_y, 7)


def draw_cell(
        x: int,
        y: int,
        cell,
        cell_size: int,
        screen: pygame.Surface,
        y_offset: int
        ) -> None:

    pixel_x = x * cell_size
    pixel_y = y * cell_size + y_offset

    if cell & 1:
        draw_horizontal_line(
            screen, WHITE, pixel_x, pixel_x + cell_size, pixel_y)

    if cell & 2:
        draw_vertical_line(
            screen, WHITE, pixel_y, pixel_y + cell_size, pixel_x + cell_size)

    if cell & 4:
        draw_horizontal_line(
            screen, WHITE, pixel_x, pixel_x + cell_size, pixel_y + cell_size)

    if cell & 8:
        draw_vertical_line(
            screen, WHITE, pixel_y, pixel_y + cell_size, pixel_x)


def draw_hud(
        screen: pygame.Surface,
        font: pygame.font.Font,
        score: int,
        lives: int,
        elapsed_time: int,
        level: int
        ) -> None:

    score_surface = font.render(f"Score: {score}", True, WHITE)
    lives_surface = font.render(f"Lives: {lives}", True, WHITE)
    time_surface = font.render(f"Time: {elapsed_time}", True, WHITE)
    level_surface = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_surface, (10, 10))
    screen.blit(lives_surface, (150, 10))
    screen.blit(time_surface, (290, 10))
    screen.blit(level_surface, (430, 10))


def draw_game(
        screen: pygame.Surface,
        maze: list[list[int]],
        pacgums: set[tuple[int, int]],
        super_pacgums: set[tuple[int, int]],
        player_position: tuple[int, int],
        ghosts: list[Ghost],
        pacman_image: pygame.Surface,
        ghost_images: list[pygame.Surface],
        frightened_image: pygame.Surface,
        cell_size: int,
        sprite_size: int,
        score: int,
        lives: int,
        font: pygame.font.Font,
        hud_height: int,
        elapsed_time: int,
        level: int
        ) -> None:

    screen.fill(BLACK)

    height = len(maze)
    width = len(maze[0])

    player_x, player_y = player_position

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]
            draw_cell(x, y, cell, cell_size, screen, hud_height)

    draw_pacgums(pacgums, screen, cell_size, hud_height)
    draw_super_pacgums(super_pacgums, screen, cell_size, hud_height)

    player_pixel_x = (
        player_x * cell_size
        + (cell_size - sprite_size) // 2
        )
    player_pixel_y = (
        player_y * cell_size
        + (cell_size - sprite_size) // 2
        + hud_height
        )

    #  calage bien au centre des images

    for ghost, ghost_image in zip(ghosts, ghost_images):

        ghost_pixel_x = (
            ghost.x * cell_size) + (cell_size - sprite_size) // 2
        ghost_pixel_y = (
            ghost.y * cell_size) + (cell_size - sprite_size) // 2 + hud_height

        if ghost.edible:
            screen.blit(frightened_image, (ghost_pixel_x, ghost_pixel_y))
        else:
            screen.blit(ghost_image, (ghost_pixel_x, ghost_pixel_y))

    screen.blit(pacman_image, (player_pixel_x, player_pixel_y))

    draw_hud(screen, font, score, lives, elapsed_time, level)

    pygame.display.flip()
