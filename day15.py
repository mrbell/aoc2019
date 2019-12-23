from typing import List, Dict, Tuple, Any
from day15_maze_explorer import run as run_maze_explorer
from day15_maze_explorer import deserialize_maze
from day15_shortest_path import find_shortest_path
from day15_oxygen_flood_fill import run as run_oxygen_flood_fill
from collections import defaultdict
import random
import curses
import time
import os
 
# See day15_maze_solver.py for a script that just solves the maze. Not needed, just for funsies!
#     day15_maze_explorer.py for a script that uncovers the full maze and stores to json
#     day15_oxygen_flood_fill.py for a script that figures out how long it takes to fill the maze with oxygen

# This script just solves part 1 for day 15 AFTER HAVING FIRST RUN THE MAZE EXPLORER!


if __name__ == '__main__':

    if not os.path.exists('day15_maze_map.json'):
        run_maze_explorer()
    else:
        print('Map loaded from a previous run!')
    maze_map = deserialize_maze('day15_maze_map.json')

    shortest_path = find_shortest_path(maze_map)

    print(f'Shortest path: {shortest_path}')

    input('Press a key')

    run_oxygen_flood_fill()
