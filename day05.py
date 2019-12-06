
from typing import List, Tuple, Callable


def read_program(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        raw_code = f.read()
    return [int(val) for val in raw_code.split(',')]


class Parameter(object):
    def __init__(self, value: int, mode: int):
        self.value = value
        self.mode = mode
    def get(self, memory: List[int]):
        if self.mode:
            return self.value
        else:
            return memory[self.value]


class IntcodeComputer(object):

    def __init__(self, initial_memory: List[int]) -> None:
        self.memory = initial_memory

        # Tuples are  
        #    the op function, whether the function takes input, whether it has output, and # of parameters
        self.instructions = {
            1: (self.add_op, 3),
            2: (self.multiply_op, 3),
            3: (self.set_op, 1),
            4: (self.get_op, 1),
            99: (None, 0),
        }

    def parse_instruction(self, instruction_pointer: int) -> Tuple[Callable[[List[int]], None], List[Parameter]]:
        
        opcode_parammode = self.memory[instruction_pointer]

        op_string = str(opcode_parammode)
        opcode = int(op_string[-2:])

        (op_function, n_params) = self.instructions[opcode]

        params = []
        index = -3
        for i in range(n_params):
            try:
                params.append(
                    Parameter(
                        self.memory[instruction_pointer + 1 + i],
                        int(op_string[index])
                    )
                )
                index -= 1
            except IndexError:
                params.append(
                    Parameter(
                        self.memory[instruction_pointer + 1 + i],
                        0
                    )
                )

        return op_function, params

    def add_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        self.memory[parameter3.value] = parameter1.get(self.memory) + parameter2.get(self.memory)
        return None

    def multiply_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        self.memory[parameter3.value] = parameter1.get(self.memory) * parameter2.get(self.memory)
        return None

    def set_op(self, parameter1: Parameter) -> None:

        while True:
            try:
                value = int(input("Input: "))
                break
            except ValueError:
                print("Input must be an integer. Please try again.")

        self.memory[parameter1.value] = value

        return None

    def get_op(self, parameter1: Parameter) -> None:
        print(parameter1.get(self.memory))

    def run(self) -> None:

        instruction_pointer = 0

        op_function, parameters = self.parse_instruction(instruction_pointer)

        while op_function is not None:

            op_function(*parameters)

            instruction_pointer += (len(parameters) + 1)

            op_function, parameters = self.parse_instruction(instruction_pointer)

        return None


if __name__ == '__main__':

    test_program = IntcodeComputer([1002,4,3,4,33])
    test_program.run()
    print(test_program.memory)

    test_program = IntcodeComputer([3,0,4,0,99])
    test_program.run()
    print(test_program.memory)

    initial_memory = read_program('./inputs/day05.txt')
    program = IntcodeComputer(initial_memory)
    program.run()
