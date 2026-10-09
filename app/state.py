from enum import Enum
from abc import ABC, abstractmethod
import pygame
import game.constants as colors
from game_session import GameSession
from config import Config
from game.cheats import CheatState
from game.level_logic import (setup_level)
from game.input import (get_direction, handle_cheat_input)
from game.reset_logic import (reset_after_loss)
from game.player_logic import (update_player, update_player_render)
from game.ghost_logic import (update_ghost,
                              update_ghost_render,
                              update_frightened_status)
from game.collectibles import (eat_pacgums, is_level_complete)
from game.collisions import (handle_collisions)
from game.rendering import (draw_game)


class StateName(Enum):
    PLAYING = "1"
    PAUSED = "2"
    END = "3"
    RESUME = "4"
    MENU = "5"
    QUIT = "6"
    HIGHSCORES = "7"
    INSTRUCTIONS = "8"
    

class State(ABC):

    """Abstract class for every State of the game. 
    next_state = None : Stay in the same state, = any other value : change to this state"""

    def __init__(self, fonts: dict[str, pygame.font.Font]) -> None:
        self.next_state: StateName | None = None
        self.fonts = fonts

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        ...

    def update(self, dt: float) -> None:
        ...


class Playing(State):

    """"""
    def __init__(self, fonts: dict[str, pygame.font.Font], config: Config, session: GameSession, images: tuple[dict[str, pygame.Surface], pygame.Surface, list[dict[str, pygame.Surface]]]) -> None:
        super().__init__(fonts)

        (self.maze, self.width,
        self.height, self.player_spawn,
        self.player, self.ghosts,
        self.pacgums, self.super_pacgums) = setup_level(config, session.level_index)

        self.blinky = self.ghosts[0]

        self.pacman_images, self.frightened_image, self.ghost_images = images

        self.session = session

        self.edible_duration: float = 5.0
        self.respawn_delay: float = 2.0
        self.cheats = CheatState()

        self.cell_size = 60
        self.sprite_size = 35
        self.hud_height: int = 50

        self.ghost_speed: float = 2.8
        self.player_speed: float = 4.0

        self.game_time = 0.0
        self.level_start_time = 0.0
        self.remaining_time = config.level_max_time

    def handle_event(self, event: pygame.event.Event) -> None:

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            self.next_state = StateName.PAUSED
        elif event.key == pygame.K_PAUSE:
            self.next_state = StateName.PAUSED
        elif event.key == pygame.K_END:
            self.next_state = StateName.END

        new_direction = get_direction(event)
        frozen_duration = handle_cheat_input(event, self.cheats, self.game_time)
        self.level_start_time += frozen_duration

        if new_direction is not None:
            self.player.requested_direction = new_direction


    def draw(self, screen: pygame.Surface) -> None:
        draw_game(
            screen, self.maze,
            self.pacgums, self.super_pacgums,
            self.player, self.ghosts,
            self.pacman_images, self.ghost_images,
            self.frightened_image,
            self.cell_size, self.sprite_size,
            self.session.score, self.session.lives, self.session.font,
            self.hud_height, self.remaining_time,
            self.session.level)

    def update(self, dt:float) -> None:
        self.game_time += dt

        timer_time = self.cheats.get_timer_time(self.game_time)
        elapsed_time = int(timer_time - self.level_start_time)
        self.remaining_time = int(max(0, self.config.level_max_time - elapsed_time))

        if self.remaining_time <= 0:
            lives -= 1

            if lives <= 0:
                print("GAME OVER")
                self.session.won = False
                self.next_state = StateName.END

            reset_after_loss(self.player, self.ghosts, self.player_spawn)
            self.level_start_time = self.game_time
            self.cheats.reset_timer_reference(self.game_time)
            return

        current_player_speed = self.cheats.get_player_speed(self.player_speed)

        update_player(self.player, self.maze)

        update_player_render(self.player, dt, current_player_speed)

        for ghost in self.ghosts:
            update_ghost(
                ghost, self.blinky,
                self.maze,
                self.player,
                self.game_time
                )

            update_ghost_render(self.ghost, dt, self.ghost_speed)

        player_position = (self.player.x, self.player.y)

        points, ate_super = eat_pacgums(
            self.pacgums, self.super_pacgums, player_position, self.config)

        update_frightened_status(self.ghosts, ate_super, self.game_time, self.edible_duration, self.maze)

        self.session.score += points

        self.session.score, self.session.lives, life_lost = handle_collisions(
            self.player_spawn, self.player, self.ghosts, self.config,
            self.game_time, self.respawn_delay, self.session.score, self.session.lives, self.cheats.invincible)

        if life_lost:
            self.level_start_time = self.game_time
            self.cheats.reset_timer_reference(self.game_time)

            if self.session.lives <= 0:
                print("GAME OVER")
                self.session.won = False
                self.next_state = StateName.END
                return

            return

        skip_requested = self.cheats.consume_skip_request()

        if is_level_complete(self.pacgums, self.super_pacgums) or skip_requested:
            print("LEVEL COMPLETE")

            if self.session.level_index + 1 >= len(self.config.level):
                print("GAME COMPLETE")
                self.session.won = True
                self.next_state = StateName.END

            else:
                self.session.level_index += 1
                self.next_state = StateName.PLAYING

class Paused(State):
    def __init__(self, fonts: dict[str, pygame.font.Font], playing: Playing) -> None:
        super().__init__(fonts)
        self.playing = playing

    def handle_event(self, event: pygame.event.Event) -> None:

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_SPACE:
            self.next_state = StateName.RESUME
        elif event.key == pygame.K_RETURN:
            self.next_state = StateName.RESUME
        elif event.key == pygame.K_ESCAPE:
            self.next_state = StateName.RESUME
        elif event.key == pygame.K_END:
            self.next_state = StateName.MENU

    def draw(self, screen: pygame.Surface) -> None:
        self.playing.draw(screen)
        screen_heigth = screen.get_height()

        draw_screen_centered(screen, self.fonts["Bold"], "GAME PAUSED", colors.WHITE)
        draw_center_text(screen, self.fonts["Medium"], "Press SPACE/ENTER/ESCAPE to resume", screen_heigth - 100, colors.WHITE)
        draw_center_text(screen, self.fonts["Medium"], "Press END to go to the MENU", screen_heigth - 50, colors.WHITE)


class End(State):

    def __init__(self, fonts: dict[str, pygame.font.Font], session: GameSession) -> None:
        super().__init__(fonts)
        self.session = session

    def handle_event(self, event: pygame.event.Event) -> None:

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_SPACE:
            self.next_state = StateName.MENU
        elif event.key == pygame.K_RETURN:
            self.next_state = StateName.MENU

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(colors.BLACK)
        if self.session.won:
            draw_screen_centered(screen, self.fonts["Bold"], "VICTORY", colors.WHITE)
        else:
            draw_screen_centered(screen, self.fonts["Bold"], "GAME OVER", colors.WHITE)


class Menu(State):
    def __init__(self, fonts: dict[str, pygame.font.Font], highscores: list[tuple[str, int]]) -> None:
        super().__init__(fonts)
        self.options = [
        ("Start", StateName.PLAYING),
        ("Highscores", StateName.HIGHSCORES),
        ("Instructions", StateName.INSTRUCTIONS),
        ("Exit", StateName.QUIT),
        ]
        self.selected = 0
        self.highscores = highscores

    def handle_event(self, event: pygame.event.Event) -> None:

        if event.type != pygame.KEYDOWN:
            return None
        
        if event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            self.next_state = self.options[self.selected][1]

    def draw(self, screen: pygame.Surface) -> None:

        screen.fill(colors.BLACK)
        draw_center_text(screen, self.fonts["Bold"], "PAC-MAN", 30, colors.WHITE)

        y = 100 
        for index, (option, _) in enumerate(self.options):
            if index == self.selected: 
                draw_center_text(screen, self.fonts["SemiBold"], f">>> {option} <<<", y, colors.YELLOW)
            else:
                draw_center_text(screen, self.fonts["SemiBold"], option, y, colors.WHITE)
            y += self.fonts["SemiBold"].get_linesize() + 50
        y += 30
        for index, (name, score) in enumerate(self.highscores[:3], 1):
            draw_center_text(screen, self.fonts["Medium"], f"{index}. {name} - {score}", y, colors.WHITE)
            y += self.fonts["Medium"].get_linesize() + 30



class Highscores(State):
    def __init__(self,fonts: dict[str, pygame.font.Font], highscores: list[tuple[str, int]]) -> None:
        super().__init__(fonts)
        self.highscores = highscores

    def handle_event(self, event: pygame.event.Event) -> None:

        if event.type != pygame.KEYDOWN:
            return None
        
        if event.key == pygame.K_SPACE:
            self.next_state = StateName.MENU
        elif event.key == pygame.K_ESCAPE:
            self.next_state = StateName.MENU

    def draw(self, screen: pygame.Surface) -> None:
        
        screen_heigth = screen.get_height()

        if not self.highscores: 
            lines = ["No highscores yet."]
        else:
            lines = [f"{index}. {name} - {score}" for index, (name, score) in enumerate(self.highscores, 1)]

        screen.fill(colors.BLACK)
        write_lines(screen, self.fonts, [("HIGHSCORES :", lines)])
        draw_center_text(screen, self.fonts["Medium"], "Press SPACE/ESCAPE to return to the menu", screen_heigth - 50, colors.WHITE)



class Instructions(State):

    def handle_event(self, event: pygame.event.Event) -> None:

        if event.type != pygame.KEYDOWN:
            return None
        
        if event.key == pygame.K_SPACE:
            self.next_state = StateName.MENU
        elif event.key == pygame.K_ESCAPE:
            self.next_state = StateName.MENU

    def draw(self, screen: pygame.Surface) -> None:

        screen_heigth = screen.get_height()

        lines = [(
            ("WHILE PLAYING:"),
            ["Press ARROWKEYS to navigate",
            "Press ESCAPE to pause",
            "Press END to stop the game"]),
            (
            ("RULES:"),
            ["Don't get caught by the ghosts",
            "Eat all the pacgums to finish the level",
            "Finish the ten levels to win the game",
            "Super-pacgums make the ghosts edible"]),
            (
            ("CHEATS:"),
            ["Press INSERT to be invincible"]),
            ]
        
        screen.fill(colors.BLACK)
        write_lines(screen, self.fonts, lines)
        draw_center_text(screen, self.fonts["Medium"], "Press SPACE/ESCAPE to return to the menu", screen_heigth - 50, colors.WHITE)


def draw_center_text(
        screen: pygame.Surface, 
        font: pygame.font.Font, 
        text: str, 
        height: int, 
        color: tuple[int, int, int]) -> None:
    
    text_surface = font.render(text, True, color)
    width_center = (screen.get_width() - text_surface.get_width()) // 2
    screen.blit(text_surface, (width_center, height))


def write_lines(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        lines: list[tuple[str, list[str]]]) -> None:
    
    y = 50
    for lists in lines:
        title, line = lists
        draw_center_text(screen, fonts["Bold"], title, y, colors.WHITE)
        y += fonts["Bold"].get_linesize() + 30
        for text in line:
            draw_center_text(screen, fonts["Medium"], text, y, colors.WHITE)
            y += fonts["Medium"].get_linesize() + 20


def draw_screen_centered(screen, font, text, color) -> None:
        
        screen_heigth = screen.get_height()
        center = (screen_heigth - font.get_height()) // 2
        draw_center_text(screen, font, text, center, color)