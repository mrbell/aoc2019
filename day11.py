from typing import List, DefaultDict, Tuple
from collections import defaultdict
from math import cos, sin, radians
from day05 import IntcodeComputer, read_program
from day08 import print_image


def plot_panel_map(panel_map: DefaultDict[Tuple[int, int], int]) -> None:
    
    min_x = min(loc[0] for loc in panel_map)
    max_x = max(loc[0] for loc in panel_map)
    min_y = min(loc[1] for loc in panel_map)
    max_y = max(loc[1] for loc in panel_map)

    nx = max_x - min_x + 1
    ny = max_y - min_y + 1

    panel_grid = [[0 for _ in range(nx)] for _ in range(ny)]

    for loc in panel_map:
        color = panel_map[loc]
        panel_grid[loc[1] - min_y][loc[0] - min_x] = color

    print_image(panel_grid)
    
    return 


class PaintingRobot(object):
    def __init__(self, program: List[int]) -> None:
        self.computer = IntcodeComputer(program)
        self.x: int = 0
        self.y: int  = 0
        self.direction: int = 90
    
    def step(self, panel: DefaultDict[Tuple[int, int], int]) -> bool:

        current_panel_color = panel[(self.x, self.y)]
        
        color_to_paint = self.computer.run_and_halt(current_panel_color)
        if color_to_paint is None:
            return True

        direction_to_turn = self.computer.run_and_halt()
        if direction_to_turn is None:
            return True

        direction_to_turn = 90 if direction_to_turn == 0 else -90

        panel[(self.x, self.y)] = color_to_paint
        self.direction += direction_to_turn

        self.x = int(round(self.x + cos(radians(self.direction))))
        self.y = int(round(self.y + sin(radians(self.direction))))

        return False


if __name__ == '__main__':

    program = read_program('./inputs/day11.txt')
    robot = PaintingRobot(program)
    panel_map = defaultdict(lambda: 0)

    program_halted = False

    while not program_halted:
        program_halted = robot.step(panel_map)

    print(f'Number of panels painted, starting w/ black panel: {len(panel_map)}')

    robot = PaintingRobot(program)
    panel_map = defaultdict(lambda: 0)
    panel_map[(0, 0)] = 1

    program_halted = False

    while not program_halted:
        program_halted = robot.step(panel_map)

    print(f'Number of panels painted, starting w/ white panel: {len(panel_map)}')

    plot_panel_map(panel_map)
