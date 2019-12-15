from typing import List, Tuple
from math import atan2, sqrt, pi


def read_map(filename: str) -> List[Tuple[int, int]]:
    with open(filename, 'r') as f:
        tmp = f.read()
    return parse_map(tmp.split('\n'))


def parse_map(asteroid_map: List[str]) -> List[Tuple[int, int]]:
    asteroid_locations = []
    for row_num, row in enumerate(asteroid_map):
        for col_num, col in enumerate(row):
            if col == '#':
                asteroid_locations.append((col_num, row_num))
    return asteroid_locations


def get_number_of_visible_asteroids(asteroid_locations: List[Tuple[int, int]]) -> List[int]:

    number_of_visible_asteroids = []

    for i, asteroid in enumerate(asteroid_locations):
        angles = []
        for j, other_asteroid in enumerate(asteroid_locations):
            if j == i:
                continue
            
            dy = other_asteroid[1] - asteroid[1]
            dx = other_asteroid[0] - asteroid[0]

            angles.append(atan2(dy, dx))

        number_of_visible_asteroids.append(len(set(angles)))

    return number_of_visible_asteroids


def get_best_location(asteroid_locations: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], int]:
    
    n_visible = get_number_of_visible_asteroids(asteroid_locations)

    max_loc, max_n = max([(loc, n) for (loc, n) in zip(asteroid_locations, n_visible)], key=lambda x: x[1])
    return max_loc, max_n


def get_vaporization_order(
    central_asteroid: Tuple[int, int], asteroid_locations: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:

    angle_distances = []

    for asteroid_location in asteroid_locations:
        if asteroid_location == central_asteroid:
            continue
        
        # Flipping these because I want 0 deg to be up and increasing to CW
        dy = asteroid_location[0] - central_asteroid[0]
        dx = -asteroid_location[1] + central_asteroid[1]  

        angle_distances.append((
            asteroid_location, 
            (atan2(dy, dx) + pi * 2) % (pi * 2),  # To convert to the range [0, 2pi] rather than [-pi, pi]
            sqrt(dx ** 2 + dy ** 2)
        ))

    # Sort by angle then distance 
    angle_distances = sorted(angle_distances, key=lambda x: (x[1], x[2]))

    adjusted_angle_distances = [angle_distances[0]]
    for angle_dist, next_angle_dist in zip(angle_distances[:-1], angle_distances[1:]):
        if next_angle_dist[1] == angle_dist[1]:  
            # At the same angle as another. The next one must be behind another so 
            # we have to sweep around before blasting it, so add 2pi to angle
            adjusted_angle_distances.append(
                (
                    next_angle_dist[0], 
                    adjusted_angle_distances[-1][1] + pi * 2, 
                    next_angle_dist[2]
                )
            )
        else:
            adjusted_angle_distances.append(next_angle_dist)
    
    return sorted(adjusted_angle_distances, key=lambda x: x[1])



if __name__ == '__main__':

    test_map = '''.#..#
.....
#####
....#
...##'''.split('\n')
    asteroid_locations = parse_map(test_map)
    best_loc, max_n = get_best_location(asteroid_locations)
    assert best_loc[0] == 3 and best_loc[1] == 4
    assert max_n == 8

    test_map = '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''.split('\n')
    asteroid_locations = parse_map(test_map)
    best_loc, max_n = get_best_location(asteroid_locations)
    assert best_loc[0] == 5 and best_loc[1] == 8
    assert max_n == 33

    test_map = '''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.'''.split('\n')
    asteroid_locations = parse_map(test_map)
    best_loc, max_n = get_best_location(asteroid_locations)
    assert best_loc[0] == 1 and best_loc[1] == 2
    assert max_n == 35

    test_map = '''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..'''.split('\n')
    asteroid_locations = parse_map(test_map)
    best_loc, max_n = get_best_location(asteroid_locations)
    assert best_loc[0] == 6 and best_loc[1] == 3
    assert max_n == 41

    test_map = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''.split('\n')
    asteroid_locations = parse_map(test_map)
    best_loc, max_n = get_best_location(asteroid_locations)
    assert best_loc[0] == 11 and best_loc[1] == 13
    assert max_n == 210

    vaporization_order = get_vaporization_order((11, 13), asteroid_locations)
    assert vaporization_order[199][0][0] == 8
    assert vaporization_order[199][0][1] == 2

    asteroid_locations = read_map('./inputs/day10.txt')
    best_loc, max_n = get_best_location(asteroid_locations)
    print(f"({best_loc[0], best_loc[1]}): {max_n}")
    vaporization_order = get_vaporization_order(best_loc, asteroid_locations)
    print(f'200th asteroid to be vaporized at: ({vaporization_order[199][0][0]}, {vaporization_order[199][0][1]}): {100 * vaporization_order[199][0][0] + vaporization_order[199][0][1]}')
