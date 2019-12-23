from typing import List, Dict, Tuple, Any
from day15_maze_explorer import deserialize_maze, destination_coordinate, NORTH, SOUTH, WEST, EAST
from day15_maze_explorer import WALL, UNKNOWN, PATH, START, GOAL
from collections import defaultdict
import random
import time
 
# See day15_maze_solver.py for a script that just solves the maze
#     day15_maze_explorer.py for a script that uncovers the full maze and stores to json
#     day15_oxygen_flood_fill.py for a script that figures out how long it takes to fill the maze with oxygen

# This script just solves part 1 for day 15 AFTER HAVING FIRST RUN THE MAZE EXPLORER!


def find_shortest_path(maze_map: Dict[Tuple[int, int], str]) -> int:

    start_location = [k for k in maze_map if maze_map[k] == START][0]
    end_location = [k for k in maze_map if maze_map[k] == GOAL][0]

    unvisited_locations = set([
        k for k in maze_map 
        if maze_map[k] == PATH or maze_map[k] == GOAL or maze_map[k] == START
    ])

    distances = {k: 0 if k == start_location else 1e6 for k in unvisited_locations}

    while end_location in unvisited_locations:

        unvisited_distances = {k: distances[k] for k in distances if k in unvisited_locations}
        current_location = min(unvisited_distances, key=lambda x: distances[x])

        tenatitive_distance = distances[current_location] + 1

        for neighbor in [
            destination_coordinate(current_location, NORTH),
            destination_coordinate(current_location, SOUTH),
            destination_coordinate(current_location, EAST),
            destination_coordinate(current_location, WEST)
        ]:
            if maze_map[neighbor] != WALL and tenatitive_distance < distances[neighbor]:
                distances[neighbor] = tenatitive_distance
        
        unvisited_locations.remove(current_location)

    return distances[end_location]


if __name__ == '__main__':

    maze_map = deserialize_maze('day15_maze_map.json')

    shortest_path = find_shortest_path(maze_map)

    print(f'Shortest path: {shortest_path}')
