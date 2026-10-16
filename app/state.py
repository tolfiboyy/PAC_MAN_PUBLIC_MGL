from enum import Enum
from abc import ABC, abstractmethod
import pygame
import game.constants as colors
from app.game_session import GameSession
from app.config import Config
from app.highscores import save_highscores, add_score, is_valid_name
from game.level_logic import (setup_level)
from game.input import (get_direction, handle_cheat_input, CHEATINPUT)
from game.reset_logic import (reset_after_loss)
from game.player_logic import (update_player, update_player_render)
from game.ghost_logic import (update_ghost,
                              update_ghost_render,
                              update_frightened_status)
from game.collectibles import (eat_pacgums, is_level_complete)
from game.collisions import (handle_collisions)
from game.rendering import (draw_game)


class StateName(Enum):

    """Holds every state"""

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
    next_state = None : Stay in the same state,
    = any other value : change to this state"""

    def __init__(self, fonts: dict[str, pygame.font.Font]) -> None:
        self.next_state: StateName | None = None
        self.fonts = fonts

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:

        """Abstract function that takes inputs, to handle events"""
        ...

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:

        """Abstract function, used to draw whatever needed,
        depending on the class"""
        ...

    def update(self, dt: float) -> None:
        """Abstract function that updates certain parameters
        during the game"""
        ...


class Playing(State):

    """Class that handles the game when playing.
    Contains the game loop, the cheat menu and the inputs"""

    def __init__(
            self,
            fonts: dict[str, pygame.font.Font],
            config: Config,
            session: GameSession,
            images: tuple[dict[str, pygame.Surface],
                          pygame.Surface,
                          list[dict[str, pygame.Surface]]]
                          ) -> None:
        super().__init__(fonts)

        (
            self.maze, self.width,
            self.height, self.player_spawn,
            self.player, self.ghosts,
            self.pacgums, self.super_pacgums
            ) = setup_level(config, session.level_index)

        self.blinky = self.ghosts[0]

        self.pacman_images, self.frightened_image, self.ghost_images = images

        self.session = session
        self.config = config
        self.fonts = fonts

        self.edible_duration: float = 5.0
        self.respawn_delay: float = 2.0
        self.cheats = session.cheats
        self.show_cheats = False

        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
        self.hud_height: int = 50

        available_width = desktop_width - 100
        available_height = desktop_height - 100

        cell_width = available_width // self.width
        cell_height = (available_height - self.hud_height) // self.height

        self.cell_size = min(60, cell_width, cell_height)
        self.sprite_size = 35
        self.windows_size = (
            self.width * self.cell_size,
            self.height * self.cell_size + self.hud_height
            )

        self.ghost_speed: float = 2.8
        self.player_speed: float = 4.0

        self.game_time = 0.0
        self.level_start_time = 0.0
        self.remaining_time = config.level_max_time

        self.cheats.reset_timer_reference(self.game_time)

        self.menu_padding = 30
        self.menu_line_height = fonts["SemiMedium"].get_linesize() + 10
        self.menu_col_width = \
            fonts["SemiMedium"].size("F2 Invincibility")[0] + 20
        menu_width = self.menu_col_width * 2 + self.menu_padding * 2
        menu_height = self.menu_line_height * 2 + self.menu_padding * 2
        self.menu_screen = pygame.Surface(
            (menu_width, menu_height), pygame.SRCALPHA)
        self.menu_screen.fill((40, 40, 40, 180))

    def handle_event(self, event: pygame.event.Event) -> None:

        """Dispatch the inputs when playing"""

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            self.next_state = StateName.PAUSED
        elif event.key == pygame.K_PAUSE:
            self.next_state = StateName.PAUSED
        elif event.key == pygame.K_END:
            self.next_state = StateName.END
        elif event.key == pygame.K_TAB:
            self.show_cheats = not self.show_cheats
        elif event.key == CHEATINPUT["skip_level_input"]:
            self.session.cheated = True

        new_direction = get_direction(event)
        frozen_duration = handle_cheat_input(
            event, self.cheats, self.game_time)
        self.level_start_time += frozen_duration

        if new_direction is not None:
            self.player.requested_direction = new_direction

    def draw(self, screen: pygame.Surface) -> None:

        """Calls the fonction that draws
        the Game and the cheat menu when active"""

        draw_game(
            screen, self.maze,
            self.pacgums, self.super_pacgums,
            self.player, self.ghosts,
            self.pacman_images, self.ghost_images,
            self.frightened_image,
            self.cell_size, self.sprite_size,
            self.session.score, self.session.lives, self.fonts["SemiBold"],
            self.hud_height, self.remaining_time,
            self.session.level_index + 1)
        if self.show_cheats:
            self.cheat_menu(screen)

    def update(self, dt: float) -> None:

        """Main utility called by the loop.
        Mainly calls all the functions when needed"""

        self.game_time += dt

        timer_time = self.cheats.get_timer_time(self.game_time)
        elapsed_time = int(timer_time - self.level_start_time)
        self.remaining_time = int(
            max(0, self.config.level_max_time - elapsed_time))

        if self.remaining_time <= 0:
            self.session.lives -= 1

            if self.session.lives <= 0:
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

            update_ghost_render(ghost, dt, self.ghost_speed)

        player_position = (self.player.x, self.player.y)

        points, ate_super = eat_pacgums(
            self.pacgums, self.super_pacgums, player_position, self.config)

        update_frightened_status(
            self.ghosts,
            ate_super,
            self.game_time,
            self.edible_duration,
            self.maze
            )

        self.session.score += points

        self.session.score, self.session.lives, life_lost = handle_collisions(
            self.player_spawn, self.player, self.ghosts, self.config,
            self.game_time, self.respawn_delay, self.session.score,
            self.session.lives, self.cheats.invincible)

        if life_lost:
            self.level_start_time = self.game_time
            self.cheats.reset_timer_reference(self.game_time)

            if self.session.lives <= 0:
                self.session.won = False
                self.next_state = StateName.END
                return

            return

        skip_requested = self.cheats.consume_skip_request()

        if is_level_complete(self.pacgums,
                             self.super_pacgums) or skip_requested:

            if self.session.level_index + 1 >= len(self.config.level):
                self.session.won = True
                self.next_state = StateName.END

            else:
                self.session.level_index += 1
                self.next_state = StateName.PLAYING

        if (
            self.cheats.speed_enabled
            or self.cheats.invincible
            or self.cheats.timer_frozen
                ):
            self.session.cheated = True

    def cheat_menu(self, screen: pygame.Surface) -> None:

        """takes the cheats and show the little
        tab menu ingame. Green when a cheat is active"""

        cheat_status = {
            "speed_input":
            ("Speed", self.cheats.speed_enabled),
            "invincibility_input":
            ("Invincibility", self.cheats.invincible),
            "freeze_input":
            ("Freeze Timer", self.cheats.timer_frozen),
            "skip_level_input":
            ("Skip level", self.cheats.skip_level_requested),
        }

        menu_x = screen.get_width() // 2 - self.menu_screen.get_width() // 2
        menu_y = screen.get_height() // 2 - self.menu_screen.get_height() // 2
        screen.blit(self.menu_screen, (menu_x, menu_y))

        for i, (name, key) in enumerate(CHEATINPUT.items()):
            label, status = cheat_status[name]
            col = i % 2
            row = i // 2
            x = menu_x + self.menu_padding + col * self.menu_col_width
            y = menu_y + self.menu_padding + row * self.menu_line_height
            text = f"{pygame.key.name(key).upper()} {label}"
            if status:
                color = colors.GREEN
            else:
                color = colors.WHITE
            draw_cheat_text(screen,
                            self.fonts["SemiMedium"], text, x, y, color)


class Paused(State):

    """Class that handles the pause of the game.
    Countains the text for it and dispatchs the inputs"""

    def __init__(
            self,
            fonts: dict[str, pygame.font.Font],
            playing: Playing
            ) -> None:
        super().__init__(fonts)
        self.playing = playing

    def handle_event(self, event: pygame.event.Event) -> None:

        """Dispatch the inputs when paused"""

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_SPACE:
            self.next_state = StateName.RESUME
        elif event.key == pygame.K_RETURN:
            self.next_state = StateName.RESUME
        elif event.key == pygame.K_ESCAPE:
            self.next_state = StateName.RESUME
        elif event.key == pygame.K_END:
            self.next_state = StateName.END

    def draw(self, screen: pygame.Surface) -> None:

        """Calls the fonction that draw the
        paused menu on top of the last playing frame"""

        self.playing.draw(screen)
        screen_height = screen.get_height()

        draw_screen_centered(screen, self.fonts["Bold"],
                             "GAME PAUSED", colors.WHITE)
        draw_center_text(screen, self.fonts["Medium"],
                         "Press SPACE/ENTER/ESCAPE to resume",
                         screen_height - 100, colors.WHITE)
        draw_center_text(screen, self.fonts["Medium"],
                         "Press END to end the game",
                         screen_height - 50, colors.WHITE)


class End(State):

    """Class that handles the game when the end menu is up.
    Countains the text for victory,
    lose / cheated or not and dispatchs the inputs"""

    def __init__(
            self,
            fonts: dict[str, pygame.font.Font],
            session: GameSession,
            highscores: list[tuple[str, int]],
            path: str,
            ) -> None:
        super().__init__(fonts)
        self.session = session
        self.highscores = highscores
        self.path = path
        self.name = ""

    def handle_event(self, event: pygame.event.Event) -> None:

        """Dispatch the inputs when the game end"""

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            self.next_state = StateName.MENU
        elif event.key == pygame.K_END:
            self.next_state = StateName.MENU
        elif event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif not self.session.cheated:
            if event.key == pygame.K_RETURN:
                if is_valid_name(self.name):
                    add_score(
                        self.highscores,
                        self.name.strip(),
                        self.session.score
                        )
                    save_highscores(self.path, self.highscores)
                    self.next_state = StateName.MENU
            else:
                candidat = self.name + event.unicode
                if is_valid_name(candidat):
                    self.name += event.unicode

    def draw(self, screen: pygame.Surface) -> None:

        """Calls the fonction that draw the end screen.
        A if for win/ lose and a if for cheated or not """

        screen.fill(colors.BLACK)
        screen_height = screen.get_height()

        if self.session.won:
            draw_center_text(
                screen,
                self.fonts["Title"],
                "VICTORY",
                100, colors.WHITE
                )
            draw_center_text(
                screen,
                self.fonts["Bold"],
                "Congratulations !",
                300, colors.WHITE
                )

        else:
            draw_center_text(
                screen,
                self.fonts["Title"],
                "GAME OVER",
                100, colors.WHITE
                )
            draw_center_text(
                screen,
                self.fonts["Bold"],
                "Try again, loser !",
                300, colors.WHITE
                )

        if self.session.cheated:
            draw_center_text(
                screen,
                self.fonts["SemiBold"],
                f"Final score : {self.session.score}",
                screen_height // 2, colors.WHITE
                )
            draw_center_text(
                screen,
                self.fonts["Medium"],
                "No highscore registration for you cheater !",
                screen_height // 2 + 100, colors.WHITE
                )
        else:
            draw_center_text(
                screen,
                self.fonts["SemiBold"],
                f"Final score : {self.session.score}",
                screen_height // 2, colors.WHITE
                )
            draw_center_text(
                screen,
                self.fonts["Medium"],
                f"Enter your name : {self.name}_",
                screen_height // 2 + 100, colors.WHITE
                )
            draw_center_text(
                screen,
                self.fonts["Medium"],
                "ENTER to save, BACKSPACE to delete",
                screen_height - 100, colors.WHITE
                )
        draw_center_text(screen,
                         self.fonts["Medium"],
                         "Press ESCAPE/END to go to the MENU",
                         screen_height - 50, colors.WHITE)


class Menu(State):

    """Class that handles the Menu.
    Countains the text for it and dispatchs the inputs.
    Also displays the top 3 highscores"""

    def __init__(
            self,
            fonts: dict[str, pygame.font.Font],
            highscores: list[tuple[str, int]],
            backgrounds: list[pygame.Surface]
            ) -> None:
        super().__init__(fonts)
        self.options = [
            ("Start", StateName.PLAYING),
            ("Highscores", StateName.HIGHSCORES),
            ("Instructions", StateName.INSTRUCTIONS),
            ("Exit", StateName.QUIT),
            ]
        self.selected = 0
        self.highscores = highscores
        self.backgrounds = backgrounds
        self.background_index: int = 0
        self.background_timer: float = 0.0
        self.background_delay: float = 6.0
        self.fade_duration: float = 1.5

    def update(self, dt: float) -> None:

        if not self.backgrounds:
            return None

        self.background_timer += dt

        if self.background_timer >= self.background_delay:
            self.background_index = (
                (self.background_index + 1) % len(self.backgrounds))

            self.background_timer = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:

        """Dispatch the inputs in the Menu"""

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            self.next_state = self.options[self.selected][1]

    def draw(self, screen: pygame.Surface) -> None:

        """Calls the fonction that draw the Menu and
        puts >>> <<< around the selected option
        also fills the background of the main menu"""

        if not self.backgrounds:
            screen.fill(colors.BLACK)
        else:
            current_background = self.backgrounds[self.background_index]

            current_x = (
                screen.get_width() - current_background.get_width()
            ) // 2

            current_y = (
                screen.get_height() - current_background.get_height()
            ) // 2

            screen.blit(
                current_background,
                (current_x, current_y)
            )

            fade_start = self.background_delay - self.fade_duration

            if self.background_timer >= fade_start:
                progress = (
                    self.background_timer - fade_start
                ) / self.fade_duration

                alpha = int(progress * 255)

                next_index = (
                    self.background_index + 1
                ) % len(self.backgrounds)

                next_background = self.backgrounds[next_index].copy()
                next_background.set_alpha(alpha)

                next_x = (
                    screen.get_width() - next_background.get_width()
                ) // 2

                next_y = (
                    screen.get_height() - next_background.get_height()
                ) // 2

                screen.blit(
                    next_background,
                    (next_x, next_y)
                )

        draw_center_text(
            screen,
            self.fonts["Title"],
            "PAC-MAN",
            50,
            colors.WHITE
        )

        y = 200
        for index, (option, _) in enumerate(self.options):
            if index == self.selected:
                draw_center_text(
                    screen,
                    self.fonts["Bold"],
                    f">>> {option} <<<",
                    y,
                    colors.YELLOW
                )
            else:
                draw_center_text(
                    screen,
                    self.fonts["Bold"],
                    option,
                    y,
                    colors.WHITE
                )

            y += self.fonts["Bold"].get_linesize() + 50

        y += 30

        for index, (name, score) in enumerate(self.highscores[:3], 1):
            draw_center_text(
                screen,
                self.fonts["SemiBold"],
                f"{index}. {name} - {score}",
                y,
                colors.WHITE
            )

            y += self.fonts["SemiBold"].get_linesize() + 30

        credit_surface = self.fonts["SemiMedium"].render(
            "By Didou & Bibou", True, colors.WHITE)
        screen.blit(credit_surface, (1135, 980))


class Highscores(State):

    """Class that handles the Highscores.
    Countains the text for it and dispatchs the inputs"""

    def __init__(
            self,
            fonts: dict[str, pygame.font.Font],
            highscores: list[tuple[str, int]]
            ) -> None:
        super().__init__(fonts)
        self.highscores = highscores

    def handle_event(self, event: pygame.event.Event) -> None:

        """Dispatch the inputs in the highscores"""

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_SPACE:
            self.next_state = StateName.MENU
        elif event.key == pygame.K_ESCAPE:
            self.next_state = StateName.MENU

    def draw(self, screen: pygame.Surface) -> None:

        """Calls the fonction that draw the highscores"""

        screen_height = screen.get_height()

        if not self.highscores:
            lines = ["No highscores yet."]
        else:
            lines = [f"{index}. {name} - {score}" for index,
                     (name, score) in enumerate(self.highscores, 1)]

        screen.fill(colors.BLACK)
        write_lines(screen, self.fonts, [("HIGHSCORES :", lines)])
        draw_center_text(screen,
                         self.fonts["Medium"],
                         "Press SPACE/ESCAPE to return to the menu",
                         screen_height - 50, colors.WHITE)


class Instructions(State):

    """Class that handles the instructions menu.
    Countains the text for it and dispatchs the inputs"""

    def handle_event(self, event: pygame.event.Event) -> None:

        """Dispatch the inputs in the instrustions"""

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_SPACE:
            self.next_state = StateName.MENU
        elif event.key == pygame.K_ESCAPE:
            self.next_state = StateName.MENU

    def draw(self, screen: pygame.Surface) -> None:

        """Calls the fonction that draw the instructions"""

        screen_height = screen.get_height()

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
            ["Press TAB to show the Cheatsheet"]),
            ]

        screen.fill(colors.BLACK)
        write_lines(screen, self.fonts, lines)
        draw_center_text(
            screen,
            self.fonts["Medium"],
            "Press SPACE/ESCAPE to return to the menu",
            screen_height - 50, colors.WHITE)


def draw_center_text(
        screen: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        height: int,
        color: tuple[int, int, int]) -> None:

    """Called to draw a text horizontally in the middle"""

    text_surface = font.render(text, True, color)
    width_center = (screen.get_width() - text_surface.get_width()) // 2
    screen.blit(text_surface, (width_center, height))


def draw_cheat_text(
        screen: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        x: int,
        y: int,
        color: tuple[int, int, int]) -> None:

    """Called to draw a text with given coordonates"""

    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def write_lines(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        lines: list[tuple[str, list[str]]]) -> None:

    """Used to write a title then every line in its list,
    for instructions/highscores"""

    y = 40
    for lists in lines:
        title, line = lists
        draw_center_text(screen, fonts["Bold"], title, y, colors.WHITE)
        y += fonts["Bold"].get_linesize() + 30
        for text in line:
            draw_center_text(screen, fonts["SemiBold"], text, y, colors.WHITE)
            y += fonts["SemiBold"].get_linesize() + 40


def draw_screen_centered(
        screen: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        color: tuple[int, int, int]
        ) -> None:

    """Used to draw a text at the exact center of the screen"""

    screen_height = screen.get_height()
    center = (screen_height - font.get_height()) // 2
    draw_center_text(screen, font, text, center, color)
