from typing import List, Dict, Tuple, Any
from day05 import IntcodeComputer, read_program
from collections import defaultdict
import sys
import curses
import random
import time

# You need to find a thing, but only have a robot that you send movement commands to 
# (one step in direction N, S, E, W) and it sends back a status indicating what happened 
# (it hit a wall, made a move, found the thing). You have no information about the 
# surroundings of the robot. The robot is controlled by an Intcode program.

# The objective is to find the shortest path to the goal.

# This script contains an algorithm that solves a maze, but there is no way the algorithm will stumble on the 
# shortest path. I've rendered the search to the console for funsies.

# I think what I have to do is to explore the whole maze, then use Dijkstra's algorithm or something to 
# find the shortest path. But I'm keeping this file because I think it's fun to watch the bot 
# explore the space.

# Movement directions
NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4

# Statuses
HIT_WALL, MOVED, FOUND_GOAL = 0, 1, 2

LARGE_NUMBER = 10000

REFRESH_RATE = 20

# Rendering
WALL = '#'
UNKNOWN = '░'
PATH = ' '
START = 'X'
POSITION = 'R'
GOAL = '$'
# Screen size
NX, NY = 60, 45


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

    while status != FOUND_GOAL:

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
        
        time.sleep(1 / REFRESH_RATE)

    render_scene(screen, current_location, maze_map)
    screen.addstr(0, 0, ('{:^' + str(NX) + 's}').format('FOUND THE THING!'))
    screen.getch()


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
    
    program = read_program('./inputs/day15.txt')

    # if display_solution:
    curses.wrapper(main_rendered, program)
        

