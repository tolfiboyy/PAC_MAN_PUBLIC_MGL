from .constants import WHITE, BLACK, ELECTRIC
from .entities.ghost import Ghost
from .entities.player import Player
import pygame


def draw_horizontal_line(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        start_x: int,
        end_x: int,
        y: int
        ) -> None:

    for pixel in range(start_x, end_x + 1):
        screen.set_at((pixel, y), color)


def draw_vertical_line(
        screen: pygame.Surface,
        color: tuple[int, int, int],
        start_y: int,
        end_y: int,
        x: int
        ) -> None:

    for pixel in range(start_y, end_y + 1):
        screen.set_at((x, pixel), color)


def draw_circles(
        screen: pygame.Surface,
        color: tuple[int, int, int],
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
        screen: pygame.Surface,
        cell_size: int,
        hud_height: int
        ) -> None:

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
        y_offset: int
        ) -> None:

    pixel_x = x * cell_size
    pixel_y = y * cell_size + y_offset

    if cell & 1:
        draw_horizontal_line(
            screen, color, pixel_x, pixel_x + cell_size, pixel_y)

    if cell & 2:
        draw_vertical_line(
            screen, color, pixel_y, pixel_y + cell_size, pixel_x + cell_size)

    if cell & 4:
        draw_horizontal_line(
            screen, color, pixel_x, pixel_x + cell_size, pixel_y + cell_size)

    if cell & 8:
        draw_vertical_line(
            screen, color, pixel_y, pixel_y + cell_size, pixel_x)


def draw_hud(
        screen: pygame.Surface,
        font: pygame.font.Font,
        score: int,
        lives: int,
        remaining_time: int,
        level: int
        ) -> None:

    score_surface = font.render(f"Score: {score}", True, WHITE)
    lives_surface = font.render(f"Lives: {lives}", True, WHITE)
    time_surface = font.render(f"Time: {remaining_time}", True, WHITE)
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

    screen.fill(BLACK)

    height = len(maze)
    width = len(maze[0])

    for y in range(height):
        for x in range(width):
            cell = maze[y][x]
            draw_cell(x, y, cell, cell_size, ELECTRIC, screen, hud_height)

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
