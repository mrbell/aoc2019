from typing import List, Tuple, Any
from day05 import IntcodeComputer, read_program
import curses
import time
import sys


class ArcadeCabinet(object):
    tile_rendering = {

        0: ' ',  # Blank
        1: '$',  # Wall
        2: '#',  # Block
        3: '-',  # Paddle
        4: 'o'   # Ball

    }
    
    def __init__(self, screen: Any, program: List[int], free_play: bool=True) -> None:
        if free_play:
            tmp = program.copy()
            tmp[0] = 2 
        else:
            tmp = program.copy()
        self.score: int = 0
        self.paddle_x_position = -1
        self.ball_x_position = -1
        self.computer = IntcodeComputer(tmp)
        self.screen = screen
        initial_screen = self.computer.run_until_input_required()
        self.render_screen(initial_screen)
        curses.curs_set(0)
        
    def render_screen(self, tiles: List[int]) -> None:

        for i in range(0, len(tiles), 3):

            if tiles[i] == -1 and tiles[i+1] == 0:
                new_score = tiles[i+2]
                if new_score > self.score:
                    self.score = new_score
                self.screen.addstr(0, 0, f'Score: {self.score:>10}')

            else:
                self.screen.addch(
                    tiles[i+1] + 1,
                    tiles[i],
                    self.tile_rendering[tiles[i+2]]
                )

                if tiles[i+2] == 3:
                    self.paddle_x_position = tiles[i]
                if tiles[i+2] == 4:
                    self.ball_x_position = tiles[i]

        self.screen.refresh()

    def game_loop(self, bot_player: bool=False) -> None:

        while True:
            if not bot_player:
                key = self.screen.getch()
                if key == curses.KEY_LEFT:
                    input_value = -1
                elif key == curses.KEY_RIGHT:
                    input_value = 1
                else:
                    input_value = 0
            else:
                diff = self.ball_x_position - self.paddle_x_position
                if diff > 0:
                    input_value = 1
                elif diff < 0:
                    input_value = -1
                else:
                    input_value = 0
                time.sleep(0.01)
            
            tiles = self.computer.run_until_input_required(input_value)

            if tiles is None:
                self.screen.addstr(18, 13, f'GAME OVER')
                self.screen.addstr(19, 13, f'SCORE: {self.score}')
                key = self.screen.getch()
                break
            else:
                self.render_screen(tiles)
    

def main(screen: Any, bot_player: bool):

    program = read_program('./inputs/day13.txt')
    cabinet = ArcadeCabinet(screen, program)
    cabinet.game_loop(bot_player=bot_player)


if __name__ == '__main__':

    program = read_program('./inputs/day13.txt')
    computer = IntcodeComputer(program)
    output = computer.run()
    print(f"Number of block tiles: {sum([1 for i in range(2, len(output), 3) if output[i] == 2])}")

    if len(sys.argv) > 1:
        bot_player = int(sys.argv[1]) == 1
    else:
        bot_player = False

    curses.wrapper(main, bot_player)
    