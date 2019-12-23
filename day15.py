from typing import List, Dict, Tuple, Any
from day05 import IntcodeComputer, read_program
from collections import defaultdict
import sys
import curses
import random
import time

# TODO: Write a pathfinding algorithm to algorithmically determine shortest path! I 
# "cheated" to get the answer by rendering the maze and counting steps.
# 
# See day15_maze_solver.py for a script that just solves the maze
#     day15_maze_explorer.py for a script that uncovers the full maze and stores to json
#     day15_oxygen_flood_fill.py for a script that figures out how long it takes to fill the maze with oxygen
