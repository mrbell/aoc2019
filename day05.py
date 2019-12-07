
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
        self.memory = initial_memory.copy()

        self.instruction_pointer = 0

        # Tuples are  
        #    the op function and # of parameters to pass to the function
        self.instructions = {
            1: (self.add_op, 3),
            2: (self.multiply_op, 3),
            3: (self.set_op, 1),
            4: (self.get_op, 1),
            5: (self.jump_if_true_op, 2),
            6: (self.jump_if_false_op, 2),
            7: (self.less_than_op, 3),
            8: (self.equal_to_op, 3),
            99: (None, 0),
        }

    def parse_instruction(self) -> Tuple[Callable[[List[int]], None], List[Parameter]]:
        
        opcode_parammode = self.memory[self.instruction_pointer]

        op_string = str(opcode_parammode)
        opcode = int(op_string[-2:])

        (op_function, n_params) = self.instructions[opcode]

        params = []
        index = -3
        for i in range(n_params):
            try:
                params.append(
                    Parameter(
                        self.memory[self.instruction_pointer + 1 + i],
                        int(op_string[index])
                    )
                )
                index -= 1
            except IndexError:
                params.append(
                    Parameter(
                        self.memory[self.instruction_pointer + 1 + i],
                        0
                    )
                )

        return op_function, params

    def add_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        self.memory[parameter3.value] = parameter1.get(self.memory) + parameter2.get(self.memory)
        self.instruction_pointer += 4
        return None

    def multiply_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        self.memory[parameter3.value] = parameter1.get(self.memory) * parameter2.get(self.memory)
        self.instruction_pointer += 4
        return None

    def set_op(self, parameter1: Parameter) -> None:

        while True:
            try:
                value = int(input("Input: "))
                break
            except ValueError:
                print("Input must be an integer. Please try again.")

        self.memory[parameter1.value] = value
        self.instruction_pointer += 2

        return None

    def get_op(self, parameter1: Parameter) -> None:
        print(parameter1.get(self.memory))
        self.instruction_pointer += 2

    def jump_if_true_op(self, parameter1: Parameter, parameter2: Parameter) -> None:
        if parameter1.get(self.memory) != 0:
            self.instruction_pointer = parameter2.get(self.memory)
        else:
            self.instruction_pointer += 3
        return None

    def jump_if_false_op(self, parameter1: Parameter, parameter2: Parameter) -> None:
        if parameter1.get(self.memory) == 0:
            self.instruction_pointer = parameter2.get(self.memory)
        else:
            self.instruction_pointer += 3
        return None

    def less_than_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        if parameter1.get(self.memory) < parameter2.get(self.memory):
            self.memory[parameter3.value] = 1
        else:
            self.memory[parameter3.value] = 0
        self.instruction_pointer += 4

    def equal_to_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        if parameter1.get(self.memory) == parameter2.get(self.memory):
            self.memory[parameter3.value] = 1
        else:
            self.memory[parameter3.value] = 0
        self.instruction_pointer += 4

    def run(self) -> None:

        self.instruction_pointer = 0

        op_function, parameters = self.parse_instruction()

        while op_function is not None:

            op_function(*parameters)

            op_function, parameters = self.parse_instruction()

        return None


if __name__ == '__main__':


    print("Part 1 tests")
    test_program = IntcodeComputer([1002,4,3,4,33])
    test_program.run()
    print(test_program.memory)

    test_program = IntcodeComputer([3,0,4,0,99])
    test_program.run()
    print(test_program.memory)
    print("Tests passed")

    print("")
    print("Part 2 tests")
    print("Should return true if input is equal to 8")
    test_program = IntcodeComputer([3,9,8,9,10,9,4,9,99,-1,8])
    test_program.run()
    print(test_program.memory)

    print("Should return true if input is less than 8")
    test_program = IntcodeComputer([3,9,7,9,10,9,4,9,99,-1,8])
    test_program.run()
    print(test_program.memory)

    print("Should return true if input is equal to 8")
    test_program = IntcodeComputer([3,3,1108,-1,8,3,4,3,99])
    test_program.run()
    print(test_program.memory)

    print("Should return true if input is less than 8")
    test_program = IntcodeComputer([3,3,1107,-1,8,3,4,3,99])
    test_program.run()
    print(test_program.memory)

    print("Should return 1 if input is non-zero")
    test_program = IntcodeComputer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
    test_program.run()
    print(test_program.memory)

    print("Should return 1 if input is non-zero")
    test_program = IntcodeComputer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
    test_program.run()
    print(test_program.memory)

    print("Should return 999 if input is below 8, 1000 if equal to 8, 1001 if greater")
    test_program = IntcodeComputer([
        3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
    ])
    test_program.run()
    print(test_program.memory)

    print("Tests passed")


    initial_memory = read_program('./inputs/day05.txt')
    print("Running part 1, input 1")
    program = IntcodeComputer(initial_memory)
    program.run()

    print("Running part 2, input 5")
    program = IntcodeComputer(initial_memory)
    program.run()
