import json
import sys


def is_valid_name(name: str) -> bool:

    """Makes sure the name is between 1 and 10 character and human readable"""

    if not 0 < len(name) < 11:
        return False
    if not all(c.isalnum() or c == " " for c in name):
        return False
    if not name.strip(" "):
        return False

    return True


def load_highscores(path: str) -> list[tuple[str, int]]:

    """The function that uses the json.load to
    transform the raw highscore in a list of max 10 scores"""

    validated: list[tuple[str, int]] = []

    try:
        with open(path, encoding="utf-8") as f:
            try:
                highscores = json.load(f)
            except json.JSONDecodeError as e:
                print(
                    f"Invalid JSON in {path}",
                    f"{e.lineno}, {e.colno}: {e.msg}", file=sys.stderr)
                return []

    except FileNotFoundError:
        return []
    except IsADirectoryError:
        print(f"IsADirectoryError in {path}.", file=sys.stderr)
        return []
    except PermissionError:
        print(f"PermissionError in {path}.", file=sys.stderr)
        return []
    except OSError:
        print(f"OSError in {path}.", file=sys.stderr)
        return []
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError in {path}.", file=sys.stderr)
        return []

    if not isinstance(highscores, list):
        print(
            "Invalid Highscore type: "
            "The JSON file must contain a list of dict", file=sys.stderr)
        return []
    for highscore in highscores:
        if not isinstance(highscore, dict):
            continue
        name = highscore.get("name")
        score = highscore.get("score")
        if not isinstance(name, str) or not is_valid_name(name):
            continue
        if not isinstance(score, int) or isinstance(score, bool) or score < 0:
            continue
        validated.append((name, score))

    validated.sort(key=lambda x: x[1], reverse=True)
    validated = validated[:10]

    return validated


def add_score(
        highscores: list[tuple[str, int]],
        name: str,
        score: int
        ) -> None:

    """Takes the highscores, adds the new score,
    sorts the list then return the 10 first"""

    highscores.append((name, score))
    highscores.sort(key=lambda x: x[1], reverse=True)
    del highscores[10:]


def save_highscores(
        path: str,
        highscores: list[tuple[str, int]]
        ) -> None:

    """Transfers the tuples into dicts and opens the file and give
    it to json.dump that writes a proper .json file with the info"""

    dict_highscores: list[dict[str, str | int]] = []
    for (name, score) in highscores:
        dict_highscores.append({"name": name, "score": score})

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dict_highscores, f, indent=1)
            print("Highscore saved")

    except FileNotFoundError:
        print(f"FileNotFoundError in {path}.", file=sys.stderr)
        return
    except IsADirectoryError:
        print(f"IsADirectoryError in {path}.", file=sys.stderr)
        return
    except PermissionError:
        print(f"PermissionError in {path}.", file=sys.stderr)
        return
    except OSError:
        print(f"OSError in {path}.", file=sys.stderr)
        return
