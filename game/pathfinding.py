
from collections import deque
from .movement import get_available_directions


def get_direction_from_path(
        current: tuple[int, int],
        next_cell: tuple[int, int]
        ) -> str | None:

    x_current, y_current = current
    x_next, y_next = next_cell

    if x_next > x_current:
        return "right"
    elif x_next < x_current:
        return "left"
    elif y_next > y_current:
        return "down"
    elif y_next < y_current:
        return "up"

    return None


def get_accessible_neighbors(
        x: int,
        y: int,
        maze: list[list[int]]
        ) -> list[tuple[int, int]]:

    accessible: list[tuple[int, int]] = []
    directions = get_available_directions(x, y, maze)

    for direction in directions:

        if direction == "up":
            accessible.append((x, y - 1))
        elif direction == "down":
            accessible.append((x, y + 1))
        elif direction == "right":
            accessible.append((x + 1, y))
        elif direction == "left":
            accessible.append((x - 1, y))

    return accessible


def shortest_path(
        maze: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int],
        ) -> list[tuple[int, int]]:

    """
    Breadth-First Search algorithm, not bread.
    It runs through a start to and end cell.
    It works with a First In First Out method.
    The deque module is used to create the queue.
    It's faster than the traditional list method.
    The function returns a path that's gonna be used
    later in our program.
    """

    queue = deque([start])
    visited: set[tuple[int, int]] = {start}
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    found = False

    if start == end:
        return [start]

    while queue and found is False:
        current = queue.popleft()
        x_current, y_current = current
        neighbors = get_accessible_neighbors(x_current, y_current, maze)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current

                if neighbor == end:
                    found = True
                    break
                else:
                    queue.append(neighbor)

    current = end
    path: list[tuple[int, int]] = [end]

    if not found:
        return []

    while current != start:
        current = came_from[current]
        path.append(current)

    return path[::-1]
