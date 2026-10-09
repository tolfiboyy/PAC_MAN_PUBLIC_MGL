import pygame
import sys
from config import ConfigError, Config
from app.app import App

pygame.init()


def main() -> None:

    try:
        if len(sys.argv) != 2:
            raise ConfigError(
                "Wrong command, example: python3 pac-man.py *config file name*"
                )

        elif not sys.argv[1].endswith(".json"):
            raise ConfigError("File must be a JSON !")

        config = Config.from_file(sys.argv[1])
    except ConfigError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    App(config).run()




if __name__ == "__main__":
    main()
