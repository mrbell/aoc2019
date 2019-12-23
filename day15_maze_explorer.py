from typing import List, Dict, Tuple, Any
from day05 import IntcodeComputer, read_program
from collections import defaultdict
import sys
import curses
import random
import time
import json

# You need to find a thing, but only have a robot that you send movement commands to 
# (one step in direction N, S, E, W) and it sends back a status indicating what happened 
# (it hit a wall, made a move, found the thing). The robot is controlled by an Intcode program.

# The objective is to find the shortest path to the goal. I wrote a maze solver, but it is
# exceedingly unlikely that the solver will find the shortest path. 

# Instead I think I need to explore the entire maze, then use a routing algorithm to 
# find the shortest path. This script is used to explore the entire maze.
# 
# To figure out if I've explored the entire maze I have to go until all open spaces 
# (including start and goal) do not have undiscovered neighbors.

# I want to save the full maze to a file so I don't have to repeat this process. What format?
# Maybe just pickle the map?

# Once I mapped the full maze I just counted on the screen... 204 steps is the shortest path.

# Movement directions
NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4

# Statuses
HIT_WALL, MOVED, FOUND_GOAL = 0, 1, 2

LARGE_NUMBER = 10000

REFRESH_RATE = 120

# Rendering
WALL = '#'
UNKNOWN = '░'
PATH = ' '
START = 'X'
POSITION = 'R'
GOAL = '$'
NX, NY = 60, 45

def serialize_maze(maze_map: Dict[Tuple[int, int], str], filename: str) -> None:

    # Have to convert tuples to a string to dump to json
    maze_map_json_friendly = {str(k): maze_map[k] for k in maze_map}

    with open(filename, 'w') as f:
        json.dump(maze_map_json_friendly, f)


def deserialize_maze(filename: str) -> Dict[Tuple[int, int], str]:
    with open(filename, 'r') as f:
        maze_map_json = json.load(f)

    maze_map = {}
    for k in maze_map_json:
        coords_str = k.replace('(', '').replace(')', '').split(', ')
        k_tuple = (int(coords_str[0]), int(coords_str[1]))
        maze_map[k_tuple] = maze_map_json[k]

    return maze_map


def get_next_direction(current_location: Tuple[int, int], exploration_history: Dict[Tuple[int, int], int]) -> int:
    '''
    Move in the direction that has been visited least thus far. If multiple directions have been visited an equal
    number of times, choose one randomly.
    '''

    north_coordinate = destination_coordinate(current_location, NORTH)
    south_coordinate = destination_coordinate(current_location, SOUTH)
    west_coordinate = destination_coordinate(current_location, WEST)
    east_coordinate = destination_coordinate(current_location, EAST)

    number_of_visits = [
        exploration_history[coord] for coord in [north_coordinate, south_coordinate, west_coordinate, east_coordinate]
    ]

    fewest_visits = min(number_of_visits)
    directions_with_fewest_visits = [i + 1 for i, v in enumerate(number_of_visits) if v == fewest_visits]

    return random.sample(directions_with_fewest_visits, 1)[0]


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


def is_exploration_complete(maze_map: Dict[Tuple[int, int], str]) -> bool:

    for k in maze_map:
        if maze_map[k] != UNKNOWN and maze_map[k] != WALL:
            # For any non-wall explored area, all surrounding locations have to be explored for the maze to 
            # be complete
            if not all([
                maze_map[destination_coordinate(k, NORTH)] != UNKNOWN,
                maze_map[destination_coordinate(k, SOUTH)] != UNKNOWN,
                maze_map[destination_coordinate(k, EAST)] != UNKNOWN,
                maze_map[destination_coordinate(k, WEST)] != UNKNOWN 
            ]):
                return False

    return True


def main_rendered(screen: Any, program: List[int]) -> None:
    '''
    Navigate through the maze to find the end and display progress on screen.
    '''
    curses.curs_set(0)

    # A dict, keyed on coordinates, with the number of times each direction has been traversed
    exploration_history: Dict[Tuple[int, int], int] = defaultdict(lambda: 0)

    # A dict, keyed on coordinates, with the character to render for that location
    maze_map: Dict[Tuple[int, int], str] = defaultdict(lambda: UNKNOWN)

    current_location: Tuple[int, int] = (0, 0)
    status: int = None  # used to store result of the last instruction
    exploration_history[current_location] += 1
    maze_map[current_location] = START

    robot = IntcodeComputer(program)

    steps = 0

    while True:

        render_scene(screen, current_location, maze_map)

        direction_to_move = get_next_direction(current_location, exploration_history)

        status = robot.run_until_input_required(direction_to_move)[0]

        if status == HIT_WALL:
            exploration_history[destination_coordinate(current_location, direction_to_move)] = LARGE_NUMBER
            maze_map[destination_coordinate(current_location, direction_to_move)] = WALL
        elif status == MOVED:
            current_location = destination_coordinate(current_location, direction_to_move)
            exploration_history[current_location] += 1
            if maze_map[current_location] == UNKNOWN:
                maze_map[current_location] = PATH
        else:  # GOAL
            current_location = destination_coordinate(current_location, direction_to_move)
            exploration_history[current_location] += 1
            maze_map[current_location] = GOAL

        steps += 1

        time.sleep(1 / REFRESH_RATE)

        if steps % 100 == 0 and is_exploration_complete(maze_map):
            break

    serialize_maze(maze_map, 'day15_maze_map.json')

    render_scene(screen, (0, 0), maze_map)
    screen.addstr(0, 0, ('{:^' + str(NX) + 's}').format('MAZE MAPPED!'))
    screen.getch()


def run():
    program = read_program('./inputs/day15.txt')

    # if display_solution:
    curses.wrapper(main_rendered, program)


if __name__ == '__main__':

    assert destination_coordinate((0, 0), NORTH) == (0, 1)
    assert destination_coordinate((0, 0), SOUTH) == (0, -1)
    assert destination_coordinate((0, 0), EAST) == (1, 0)
    assert destination_coordinate((0, 0), WEST) == (-1, 0)

    test_history = {(1, 0): 1, (-1, 0): 2, (0, 1): 3, (0, -1): 4}
    assert get_next_direction((0, 0), test_history) == EAST

    test_history = {(1, 0): 1, (-1, 0): 1, (0, 1): 1, (0, -1): 4}
    assert get_next_direction((0, 0), test_history) != SOUTH

    # display_solution = False
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == '1':
    #         display_solution = True
    run()
    # program = read_program('./inputs/day15.txt')

    # # if display_solution:
    # curses.wrapper(main_rendered, program)
        

