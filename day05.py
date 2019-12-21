
from typing import List, Tuple, Callable, Dict, Union


def read_program(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        raw_code = f.read()
    return [int(val) for val in raw_code.split(',')]


class Parameter(object):
    def __init__(self, value: int, mode: int) -> None:
        self.value = value
        self.mode = mode
    def get(self, memory: List[int], relative_base: int) -> int:
        if self.mode == 1:
            return self.value
        elif self.mode == 2:
            try:
                value = memory[self.value + relative_base]
            except IndexError:
                memory.extend([0 for _ in range(self.value + relative_base - len(memory) + 1)])
                value = 0
            return value
        else:
            try:
                value = memory[self.value]
            except IndexError:
                memory.extend([0 for _ in range(self.value - len(memory) + 1)])
                value = 0
            return value


class IntcodeComputer(object):

    def __init__(self, initial_memory: List[int]) -> None:
        self.initial_memory = initial_memory.copy()
        self.memory = initial_memory.copy()

        self.instruction_pointer = 0
        self.relative_base = 0

        # Tuples are  
        #    the op function, whether it takes input, gives output, 
        #    and # of parameters to pass to the function
        self.instructions: Dict[int, Tuple[Callable, bool, bool, int]] = {
            1: (self.add_op, False, False, 3),
            2: (self.multiply_op, False, False, 3),
            3: (self.set_op, True, False, 1),
            4: (self.get_op, False, True, 1),
            5: (self.jump_if_true_op, False, False, 2),
            6: (self.jump_if_false_op, False, False, 2),
            7: (self.less_than_op, False, False, 3),
            8: (self.equal_to_op, False, False, 3),
            9: (self.relative_base_offset_op, False, False, 1),
            99: (None, False, False, 0),
        }

    def parse_instruction(self) -> Tuple[Callable, bool, bool, List[Parameter]]:
        
        opcode_parammode = self.memory[self.instruction_pointer]

        op_string = str(opcode_parammode)
        opcode = int(op_string[-2:])

        (op_function, takes_input, sends_output, n_params) = self.instructions[opcode]

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

        return op_function, takes_input, sends_output, params

    def add_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        if parameter3.mode == 2:
            value = parameter3.value + self.relative_base
        else: 
            value = parameter3.value

        if value >= len(self.memory):
            self.memory.extend([0 for _ in range(value - len(self.memory) + 1)])

        self.memory[value] = parameter1.get(self.memory, self.relative_base) + parameter2.get(self.memory, self.relative_base)
        self.instruction_pointer += 4
        return None

    def multiply_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        if parameter3.mode == 2:
            value = parameter3.value + self.relative_base
        else: 
            value = parameter3.value

        if value >= len(self.memory):
            self.memory.extend([0 for _ in range(value - len(self.memory) + 1)])

        self.memory[value] = parameter1.get(self.memory, self.relative_base) * parameter2.get(self.memory, self.relative_base)
        self.instruction_pointer += 4
        return None

    def set_op(self, input_value: int, parameter1: Parameter) -> None:
        if parameter1.mode == 2:
            value = parameter1.value + self.relative_base
        else: 
            value = parameter1.value

        if value >= len(self.memory):
            self.memory.extend([0 for _ in range(value - len(self.memory) + 1)])

        self.memory[value] = input_value
        self.instruction_pointer += 2

        return None

    def get_op(self, parameter1: Parameter) -> int:
        self.instruction_pointer += 2

        return parameter1.get(self.memory, self.relative_base)

    def jump_if_true_op(self, parameter1: Parameter, parameter2: Parameter) -> None:
        if parameter1.get(self.memory, self.relative_base) != 0:
            self.instruction_pointer = parameter2.get(self.memory, self.relative_base)
        else:
            self.instruction_pointer += 3
        return None

    def jump_if_false_op(self, parameter1: Parameter, parameter2: Parameter) -> None:
        if parameter1.get(self.memory, self.relative_base) == 0:
            self.instruction_pointer = parameter2.get(self.memory, self.relative_base)
        else:
            self.instruction_pointer += 3
        return None

    def less_than_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None:
        if parameter3.mode == 2:
            value = parameter3.value + self.relative_base
        else: 
            value = parameter3.value

        if value >= len(self.memory):
            self.memory.extend([0 for _ in range(value - len(self.memory) + 1)])

        if parameter1.get(self.memory, self.relative_base) < parameter2.get(self.memory, self.relative_base):
            self.memory[value] = 1
        else:
            self.memory[value] = 0
        self.instruction_pointer += 4

    def equal_to_op(self, parameter1: Parameter, parameter2: Parameter, parameter3: Parameter) -> None: 
        if parameter3.mode == 2:
            value = parameter3.value + self.relative_base
        else: 
            value = parameter3.value

        if value >= len(self.memory):
            self.memory.extend([0 for _ in range(value - len(self.memory) + 1)])

        if parameter1.get(self.memory, self.relative_base) == parameter2.get(self.memory, self.relative_base):
                self.memory[value] = 1
        else:
            self.memory[value] = 0
        self.instruction_pointer += 4

    def relative_base_offset_op(self, parameter1: Parameter) -> None:
        self.relative_base += parameter1.get(self.memory, self.relative_base)
        self.instruction_pointer += 2

    def run(self, *inputs: Tuple[int]) -> List[int]:
        """
        Run the program until opcode 99 is reached. Return all outputs produced as a list of integers.
        """

        self.memory = self.initial_memory.copy()

        self.instruction_pointer = 0
        inputs = list(inputs)
        inputs.reverse()

        op_function, takes_input, gives_output, parameters = self.parse_instruction()
        outputs = []

        while op_function is not None:

            if takes_input and not gives_output:
                op_function(inputs.pop(), *parameters)
            elif not takes_input and gives_output:
                outputs.append(op_function(*parameters))
            elif takes_input and gives_output:
                outputs.append(op_function(inputs.pop(), *parameters))
            else:
                op_function(*parameters)

            op_function, takes_input, gives_output, parameters = self.parse_instruction()

        return outputs

    def run_and_halt(self, *inputs: Tuple[int]) -> int:
        """
        Run the program until it produces output at which time it will return the output and halt execution.
        Program state and instruction pointer is maintained between calls. When opcode 99 is reached (program is terminated)
        this method will return None.
        """

        inputs = list(inputs)
        inputs.reverse()

        op_function, takes_input, gives_output, parameters = self.parse_instruction()

        while op_function is not None:

            if takes_input and not gives_output:
                op_function(inputs.pop(), *parameters)
            elif not takes_input and gives_output:
                return op_function(*parameters)
            elif takes_input and gives_output:
                return op_function(inputs.pop(), *parameters)
            else:
                op_function(*parameters)

            op_function, takes_input, gives_output, parameters = self.parse_instruction()

        return None

    def run_until_input_required(self, input_value: int=None) -> List[int]:
        """
        Run the program until it requires input at which time it will return the output and halt execution.
        Program state and instruction pointer is maintained between calls. When opcode 99 is reached (program is terminated)
        this method will return None.
        """

        op_function, takes_input, gives_output, parameters = self.parse_instruction()
        input_used = False
        outputs = []

        while op_function is not None:

            if takes_input and not gives_output:
                if not input_used and input_value is not None:
                    op_function(input_value, *parameters)
                    input_used = True
                else:
                    return outputs

            elif not takes_input and gives_output:
                outputs.append(op_function(*parameters))

            elif takes_input and gives_output:
                if not input_used and input_value is not None:
                    outputs.append(op_function(input_value, *parameters))
                    input_used = True
                else:
                    return outputs
                    
            else:
                op_function(*parameters)

            op_function, takes_input, gives_output, parameters = self.parse_instruction()

        if len(outputs) == 0:
            return None
        else: 
            return outputs


if __name__ == '__main__':


    print("Part 1 tests", end='...')
    test_program = IntcodeComputer([1002,4,3,4,33])
    test_output = test_program.run()
    assert len(test_output) == 0
    assert test_program.memory[4] == 99

    test_program = IntcodeComputer([3,0,4,0,99])
    test_output = test_program.run(43)
    assert len(test_output) == 1
    assert test_output[0] == 43
    print('Passed!')

    print("Part 2 tests", end='...')
    # print("Should return true if input is equal to 8")
    test_program = IntcodeComputer([3,9,8,9,10,9,4,9,99,-1,8])
    test_output = test_program.run(8)
    assert len(test_output) == 1
    assert test_output[0] == 1
    test_output = test_program.run(4)
    assert len(test_output) == 1
    assert test_output[0] == 0

    # print("Should return true if input is less than 8")
    test_program = IntcodeComputer([3,9,7,9,10,9,4,9,99,-1,8])
    test_output = test_program.run(8)
    assert len(test_output) == 1
    assert test_output[0] == 0
    test_output = test_program.run(4)
    assert len(test_output) == 1
    assert test_output[0] == 1

    # print("Should return true if input is equal to 8")
    test_program = IntcodeComputer([3,3,1108,-1,8,3,4,3,99])
    test_output = test_program.run(8)
    assert len(test_output) == 1
    assert test_output[0] == 1
    test_output = test_program.run(4)
    assert len(test_output) == 1
    assert test_output[0] == 0

    # print("Should return true if input is less than 8")
    test_program = IntcodeComputer([3,3,1107,-1,8,3,4,3,99])
    test_output = test_program.run(8)
    assert len(test_output) == 1
    assert test_output[0] == 0
    test_output = test_program.run(4)
    assert len(test_output) == 1
    assert test_output[0] == 1


    # print("Should return 1 if input is non-zero")
    test_program = IntcodeComputer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
    test_output = test_program.run(8)
    assert len(test_output) == 1
    assert test_output[0] == 1
    test_output = test_program.run(0)
    assert len(test_output) == 1
    assert test_output[0] == 0



    # print("Should return 1 if input is non-zero")
    test_program = IntcodeComputer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
    test_output = test_program.run(8)
    assert len(test_output) == 1
    assert test_output[0] == 1
    test_output = test_program.run(0)
    assert len(test_output) == 1
    assert test_output[0] == 0

    # print("Should return 999 if input is below 8, 1000 if equal to 8, 1001 if greater")
    test_program = IntcodeComputer([
        3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
    ])
    test_output = test_program.run(1)
    assert len(test_output) == 1
    assert test_output[0] == 999
    test_output = test_program.run(8)
    assert len(test_output) == 1
    assert test_output[0] == 1000
    test_output = test_program.run(700)
    assert len(test_output) == 1
    assert test_output[0] == 1001
    
    print("Passed!")


    initial_memory = read_program('./inputs/day05.txt')
    print("Running part 1: ", end='')
    program = IntcodeComputer(initial_memory)
    part1_output = program.run(1)
    print(f'{part1_output[-1]}')


    print("Running part 2: ", end='')
    program = IntcodeComputer(initial_memory)
    part2_output = program.run(5)
    print(f'{part2_output[0]}')
