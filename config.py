import json
from dataclasses import dataclass, field, fields
import sys
from typing import Any

LEVELS = [
    {"width": 15, "height": 11},
    {"width": 15, "height": 13},
    {"width": 17, "height": 13},
    {"width": 19, "height": 13},
    {"width": 19, "height": 15},
    {"width": 21, "height": 15},
    {"width": 23, "height": 15},
    {"width": 23, "height": 17},
    {"width": 25, "height": 17},
    {"width": 25, "height": 19}
]


class ConfigError(Exception):

    """Custom error class to catch configuration errors"""

    def __init__(self, message: str = "Unknown config error") -> None:
        super().__init__(message)


@dataclass
class LevelConfig():

    """Dataclass holding the data for the level in the Config dataclass"""

    width: int = field(default=21, metadata={"min": 14, "max": 40})
    height: int = field(default=15, metadata={"min": 10, "max": 40})


def level_factory() -> list[LevelConfig]:

    """Simple function that creates LevelConfig
    classes from the default LEVELS"""

    return [LevelConfig(**lvl) for lvl in LEVELS]


@dataclass
class Config():

    """Dataclass holding the data of the config"""

    seed: int = field(default=500, metadata={"min": 1})
    highscore_filename: str = field(default="highscores.json")
    lives: int = field(default=3, metadata={"min": 1, "max": 9})
    pacgum: int = field(default=42, metadata={"min": 1})
    points_per_pacgum: int = field(
        default=10, metadata={"min": 0, "max": 10000})
    points_per_super_pacgum: int = field(
        default=50, metadata={"min": 0, "max": 10000})
    points_per_ghost: int = field(
        default=200, metadata={"min": 0, "max": 10000})
    level_max_time: int = field(default=90, metadata={"min": 10, "max": 600})
    level: list[LevelConfig] = field(default_factory=level_factory)

    @classmethod
    def from_file(cls, config_path: str) -> "Config":

        """The conductor of the config. It calls every fonction needed
        to dispatch the info of the config file in the Config class"""

        raw_config: str = read_config(config_path)
        config_dict: dict = load_config(raw_config, config_path)
        validated = config_validation(config_dict, cls)
        validated["level"] = levels_validation(config_dict)
        config = cls(**validated)
        return config


def read_config(config_path: str) -> str:

    """The function that opens the file and filter de comments out by
    making them empty lines"""

    config_trimmed: str = ""
    try:
        with open(config_path, encoding="utf-8") as f:
            for line in f:
                test_line = line.strip()
                if test_line.startswith("#") or not test_line:
                    config_trimmed += "\n"
                else:
                    config_trimmed += line
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {config_path}")
    except IsADirectoryError:
        raise ConfigError(f"Config file is a directory: {config_path}")
    except PermissionError:
        raise ConfigError(f"No permission to open the file: {config_path}")
    except OSError as e:
        raise ConfigError(f"OSError caught in {config_path}: {e}")
    except UnicodeDecodeError as e:
        raise ConfigError(f"UnicodeDecodeError caught in {config_path}: {e}")

    return config_trimmed


def load_config(raw_config: str, config_path: str) -> dict:

    """The function that uses the json.loads to
    transform the raw config in a dict"""

    try:
        config = json.loads(raw_config)
    except json.JSONDecodeError as e:
        raise ConfigError(
            f"Invalid JSON in {config_path}, {e.lineno}, {e.colno}: {e.msg}")
    if not isinstance(config, dict):
        raise ConfigError(
            "Invalid config type: The JSON file must contain a dict { }")

    return config


def config_validation(config_dict: dict, config_cls: type[Any],
                      prefix: str = "") -> dict:

    """Checks the config_dict that was send to it.
    Wrong type, empty or not in bound"""
    validated = {}
    for f in fields(config_cls):
        if f.name == "level":
            continue

        expected_type = f.type
        if not isinstance(expected_type, type):
            raise TypeError(f"{prefix}{f.name}: annotation is not a class")
        elif f.name not in config_dict:
            print(f"{prefix}{f.name} not found in the config file. "
                  f"Using default ({f.default}).", file=sys.stderr)
            continue

        value = config_dict[f.name]
        if not isinstance(value, expected_type) or isinstance(value, bool):
            print(f"{prefix}{f.name} has wrong type. "
                  f"Using default ({f.default}).", file=sys.stderr)
            continue
        elif f.name == "highscore_filename" and not value:
            print(f"{prefix}{f.name} is empty. "
                  f"Using default ({f.default}).", file=sys.stderr)
            continue
        elif f.metadata:
            min_value = f.metadata.get("min")
            max_value = f.metadata.get("max")
            if min_value is not None and value < min_value:
                print(f"{prefix}{f.name}={value} is lower than the minimum "
                      f"({min_value}). Using minimum ({min_value}).",
                      file=sys.stderr)
                value = min_value
            elif max_value is not None and value > max_value:
                print(f"{prefix}{f.name}={value} is higher than the maximum "
                      f"({max_value}). Using maximum ({max_value}).",
                      file=sys.stderr)
                value = max_value

        validated[f.name] = value

    return validated


def levels_validation(config_dict: dict) -> list[LevelConfig]:

    """Checks if there are at least 10 valid levels and send to config_validation"""

    validated_levels = []
    levels = config_dict.get("level")

    if levels is None:
        print("No levels found in the config file. "
              "Using defaults.", file=sys.stderr)
        return level_factory()
    elif not isinstance(levels, list):
        print("Levels has wrong type. "
              "Using defaults.", file=sys.stderr)
        return level_factory()

    for n, level in enumerate(levels):
        if not isinstance(level, dict):
            print(f"Level {n + 1} is not a dict. Skipping it.",
                  file=sys.stderr)
            continue

        temp_level = config_validation(level, LevelConfig, f"Level {n + 1}: ")
        validated_levels.append(LevelConfig(**temp_level))

    i = len(validated_levels)
    if i < 10:
        validated_levels.extend(level_factory()[i:])
        print(f"{10 - i} levels missing to have the 10 minimum. "
              f"{10 - i} default levels added.", file=sys.stderr)

    return validated_levels
