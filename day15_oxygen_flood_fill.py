from typing import List, Dict, Tuple, Any
from day15_maze_explorer import deserialize_maze
import curses
import time

# Now oxygen is going to fill the map space spreading from the goal of the maze.
# How long does it take? For this I just need the maze map I uncovered before
# and a diffusion algorithm. No Intcode required.

# Movement directions
NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4

REFRESH_RATE = 30

# Rendering
WALL = '#'
UNKNOWN = '░'
PATH = ' '
START = 'X'
POSITION = 'R'
GOAL = '$'
OXYGEN = '°'
NX, NY = 60, 45


def destination_coordinate(current_coordinate: Tuple[int, int], direction: int) -> Tuple[int, int]:
    '''
    Given a position and direction, get the destination coordinate e.g. if at (1, 2) and going NORTH, the result is 
    (1, 3).
    '''
    if direction == NORTH:
        return (current_coordinate[0], current_coordinate[1] + 1)
    elif direction == SOUTH:
        return (current_coordinate[0], current_coordinate[1] - 1)
    elif direction == EAST:
        return (current_coordinate[0] + 1, current_coordinate[1])
    elif direction == WEST:
        return (current_coordinate[0] - 1, current_coordinate[1])
    else:
        raise ValueError(f'Ivalid direction {direction} given')


def render_scene(screen: Any, current_location: Tuple[int, int], maze_map: Dict[Tuple[int, int], str]) -> None:

    screen_left_edge = int(current_location[0] - NX / 2)
    screen_right_edge = int(current_location[0] + NX / 2 + 1)

    screen_top_edge = int(current_location[1] + NY / 2 + 1)
    screen_bottom_edge = int(current_location[1] - NY / 2)

    for y in range(screen_bottom_edge, screen_top_edge):
        for x in range(screen_left_edge, screen_right_edge):
            screen_y = screen_top_edge - y  # curses y coord is 0 at the top and increases downward
            screen_x = x - screen_left_edge

            screen.addch(screen_y, screen_x, maze_map[(x, y)])

    if maze_map[current_location] != GOAL:
        screen.addch(NY // 2 + 1, NX // 2, POSITION)

    screen.refresh()


def fill_neighbors(maze_map: Dict[Tuple[int, int], str], location: Tuple[int, int]) -> None:

    for neighbor in [
        destination_coordinate(location, NORTH),
        destination_coordinate(location, SOUTH),
        destination_coordinate(location, EAST),
        destination_coordinate(location, WEST)
    ]:

        if maze_map[neighbor] != WALL and maze_map[neighbor] != UNKNOWN and maze_map[neighbor] != OXYGEN:
            maze_map[neighbor] = OXYGEN
        
    return None


def any_empty_neighbors(maze_map: Dict[Tuple[int, int], str], location: Tuple[int, int]) -> bool:

    for neighbor in [
        destination_coordinate(location, NORTH),
        destination_coordinate(location, SOUTH),
        destination_coordinate(location, EAST),
        destination_coordinate(location, WEST)
    ]:
        if maze_map[neighbor] != WALL and maze_map[neighbor] != UNKNOWN and maze_map[neighbor] != OXYGEN:
            return True

    return False


def get_edge_coordinates(maze_map: Dict[Tuple[int, int], str]) -> List[Tuple[int, int]]:

    edge_coordinates = []

    for location in maze_map:
        if maze_map[location] == OXYGEN and any_empty_neighbors(maze_map, location):
            edge_coordinates.append(location)

    return edge_coordinates


def main_rendered(screen: Any, filename: str) -> None:
    '''
    Navigate through the maze to find the end and display progress on screen.
    '''
    curses.curs_set(0)

    maze_map = deserialize_maze(filename)

    seed_location = [k for k in maze_map if maze_map[k] == GOAL][0]
    maze_map[seed_location] = OXYGEN

    steps = 0

    while True:

        render_scene(screen, (0, 0), maze_map)

        edge_coordinates = get_edge_coordinates(maze_map)
        if len(edge_coordinates) == 0:
            break

        for edge_cell in edge_coordinates:
            fill_neighbors(maze_map, edge_cell)

        steps += 1

        time.sleep(1 / REFRESH_RATE)

    render_scene(screen, (0, 0), maze_map)
    screen.addstr(0, 0, ('{:^' + str(NX) + 's}').format(f'WE ARE SAVED AFTER {steps} MINUTES!'))
    screen.getch()


def run():
    curses.wrapper(main_rendered, 'day15_maze_map.json')


if __name__ == '__main__':

    run()
