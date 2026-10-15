import pygame
import sys
import game.constants as colors
from app.game_session import GameSession
from app.config import Config
from app.highscores import load_highscores
from app.state import (State, Playing, Menu, End,
                       Instructions, Highscores, Paused, StateName)
from game.assets import (load_images, load_backgrounds)

pygame.init()


class App():

    """The main. Holds everything needed for the state.py classes.
    Contains the main loop and dispatch the state when changing"""

    def __init__(self, config: Config) -> None:

        self.hand_screen_size = (22 * 60, 16 * 60 + 50)

        self.screen = pygame.display.set_mode(self.hand_screen_size)

        self.fonts = load_fonts()

        self.config: Config = config

        self.highscores = load_highscores(config.highscore_filename)

        self.images = load_images()

        self.backgrounds = load_backgrounds()

        self.current_state: State = Menu(
            self.fonts, self.highscores, self.backgrounds)

        self.running = True

        self.session: GameSession | None = None

    def run(self) -> None:

        """The main loop. Contains the dt and calls the states classes"""

        pygame.display.set_caption("pac_man")

        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000.0
            dt = min(dt, 0.1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_state.handle_event(event)

            self.current_state.update(dt)
            self.current_state.draw(self.screen)
            pygame.display.flip()

            if self.current_state.next_state is not None:
                self.change_state(self.current_state.next_state)

        pygame.quit()

    def change_state(self, requested: StateName) -> None:

        """Calls the asked state class when
        self.current_state.next_state is not None"""

        self.current_state.next_state = None

        match requested:
            case StateName.PLAYING:
                try:
                    if self.session is None:
                        self.session = GameSession(self.config.lives)
                    self.current_state = Playing(
                        self.fonts, self.config, self.session, self.images)
                    self.screen = pygame.display.set_mode(
                        self.current_state.windows_size)
                except Exception as e:
                    print(f"Mazegerator error: {e}", file=sys.stderr)
                    self.current_state = Menu(
                        self.fonts, self.highscores, self.backgrounds)

            case StateName.PAUSED:
                if isinstance(self.current_state, Playing):
                    self.current_state = Paused(self.fonts, self.current_state)
                else:
                    raise RuntimeError(
                        "Trying to pause while the game is not in Playing.")

            case StateName.RESUME:
                if isinstance(self.current_state, Paused):
                    self.current_state = self.current_state.playing
                else:
                    raise RuntimeError(
                        "Trying to resume while game is not Paused.")

            case StateName.MENU:
                self.session = None
                self.current_state = Menu(
                    self.fonts, self.highscores, self.backgrounds)
                self.screen = pygame.display.set_mode(self.hand_screen_size)

            case StateName.HIGHSCORES:
                self.current_state = Highscores(self.fonts, self.highscores)

            case StateName.INSTRUCTIONS:
                self.current_state = Instructions(self.fonts)

            case StateName.END:
                if self.session is not None:
                    self.screen = pygame.display.set_mode(
                        self.hand_screen_size
                        )
                    self.current_state = End(
                        self.fonts,
                        self.session,
                        self.highscores,
                        self.config.highscore_filename
                        )
                else:
                    raise RuntimeError(
                        "Trying to END while there is no active game session.")

            case StateName.QUIT:
                self.running = False

            case _:
                raise RuntimeError(f"{requested} is not a StateName.")


def load_fonts() -> dict[str, pygame.font.Font]:

    """Just loads the fonts and make sure it does not crash"""

    try:
        font_title = pygame.font.Font("assets/fonts/Montserrat-Black.ttf", 80)
        font_bold = pygame.font.Font("assets/fonts/Montserrat-Bold.ttf", 50)
        font_semibold = pygame.font.Font(
            "assets/fonts/Montserrat-SemiBold.ttf", 30)
        font_medium = pygame.font.Font(
            "assets/fonts/Montserrat-Medium.ttf", 30)
        font_semimedium = pygame.font.Font(
            "assets/fonts/Montserrat-Medium.ttf", 20)
        font_title.render("Test", True, colors.WHITE)
        font_bold.render("Test", True, colors.WHITE)
        font_semibold.render("Test", True, colors.WHITE)
        font_medium.render("Test", True, colors.WHITE)
        font_semimedium.render("Test", True, colors.WHITE)

    except (FileNotFoundError, pygame.error) as e:
        print(f"Font error : {e}.\n Using default.", file=sys.stderr)
        font_title = pygame.font.Font(None, 80)
        font_bold = pygame.font.Font(None, 50)
        font_semibold = pygame.font.Font(None, 30)
        font_medium = pygame.font.Font(None, 30)
        font_semimedium = pygame.font.Font(None, 20)

    return {
            "SemiBold": font_semibold,
            "Bold": font_bold,
            "Medium": font_medium,
            "SemiMedium": font_semimedium,
            "Title": font_title
            }
