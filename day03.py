from typing import List, Tuple


def parse_wire_paths(path_specification: str) -> List[List[str]]:
    per_wire_specification = path_specification.split('\n')
    return [ps.split(',') for ps in per_wire_specification if len(ps.strip()) > 0]


def load_wire_paths(filename: str) -> List[List[str]]: 
    with open(filename, 'r') as f:
        raw_data = f.read()

    return parse_wire_paths(raw_data)


def wire_path_to_coordinates(wire_path: List[str]) -> List[Tuple[int]]:
    current_x = 0
    current_y = 0

    path_coordinates = [(current_x, current_y)]

    for path_segment in wire_path:

        path_direction = path_segment[0]
        step_length = int(path_segment[1:])

        for y in range(step_length):

            if path_direction == 'U':
                current_y += 1
            elif path_direction == 'D':
                current_y -= 1
            elif path_direction == 'L':
                current_x -= 1
            elif path_direction == 'R':
                current_x += 1
            else:
                raise ValueError(f'Unknown wire path direction {path_direction}')
                
            path_coordinates.append((current_x, current_y))

    return path_coordinates


def get_intersection_coords(wire_paths: List[List[str]]) -> Tuple[int]:
    first_wire_coords = wire_path_to_coordinates(wire_paths[0])
    second_wire_coords = wire_path_to_coordinates(wire_paths[1])

    return [
        v for v in set(first_wire_coords).intersection(set(second_wire_coords))
        if (abs(v[0]) + abs(v[1])) != 0
    ]


def get_intersection_distances(wire_paths: List[List[str]]) -> int:
    intersection_coords = get_intersection_coords(wire_paths)

    return [
        (abs(v[0]) + abs(v[1]))
        for v in intersection_coords
    ]


def get_intersection_distance_closest_to_start(wire_paths: List[List[str]]) -> int:

    return min(get_intersection_distances(wire_paths))


def get_best_path_to_intersection(wire_paths: List[List[str]]) -> int:

    intersection_coords = get_intersection_coords(wire_paths)

    first_wire_coords = wire_path_to_coordinates(wire_paths[0])
    second_wire_coords = wire_path_to_coordinates(wire_paths[1])

    intersection_path_legths = []

    for intersection_coord in intersection_coords:
        wire1path = min([i for i, coord in enumerate(first_wire_coords) if coord == intersection_coord])
        wire2path = min([i for i, coord in enumerate(second_wire_coords) if coord == intersection_coord])

        intersection_path_legths.append(wire1path + wire2path)

    return min(intersection_path_legths)


if __name__ == '__main__':

    test_input = '''R8,U5,L5,D3
U7,R6,D4,L4'''

    wire_paths = parse_wire_paths(test_input)
    assert get_intersection_distance_closest_to_start(wire_paths) == 6
    assert get_best_path_to_intersection(wire_paths) == 30
    
    test_input = '''R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83'''

    wire_paths = parse_wire_paths(test_input)
    assert get_intersection_distance_closest_to_start(wire_paths) == 159
    assert get_best_path_to_intersection(wire_paths) == 610

    test_input = '''R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'''

    wire_paths = parse_wire_paths(test_input)
    assert get_intersection_distance_closest_to_start(wire_paths) == 135
    assert get_best_path_to_intersection(wire_paths) == 410

    wire_paths = load_wire_paths('./inputs/day03.txt')
    closest_intersection = get_intersection_distance_closest_to_start(wire_paths)
    print(f"Solution to part 1: {closest_intersection}")
    best_path = get_best_path_to_intersection(wire_paths)
    print(f'Solution to part 2: {best_path}')