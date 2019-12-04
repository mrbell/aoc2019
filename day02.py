
from typing import List


def read_program(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        raw_code = f.read()
    return [int(val) for val in raw_code.split(',')]


def add_op(code: List[int], input1: int, input2: int, output: int) -> List[int]:
    new_code = code.copy()

    new_code[output] = code[input1] + code[input2]

    return new_code


def multiply_op(code: List[int], input1: int, input2: int, output: int) -> List[int]:
    new_code = code.copy()

    new_code[output] = code[input1] * code[input2]

    return new_code


instructions = {
    1: add_op,
    2: multiply_op,
    99: None,
}


def run_program(initial_memory: List[int], input1: int, input2: int) -> int:

    memory = initial_memory.copy()

    memory[1] = input1
    memory[2] = input2

    instruction_pointer = 0
    instruction = instructions[
        memory[instruction_pointer]
    ]

    while instruction is not None:
        parameter1_address = memory[instruction_pointer + 1]
        parameter2_address = memory[instruction_pointer + 2]
        output_address = memory[instruction_pointer + 3]

        memory = instruction(memory, parameter1_address, parameter2_address, output_address)

        instruction_pointer += 4
        instruction = instructions[
            memory[instruction_pointer]
        ]
    
    return memory


if __name__ == '__main__':

    test_program = [1,0,0,0,99]
    test_output = run_program(test_program, 0, 0)
    assert all(truth == test for truth, test in zip(test_output, [2,0,0,0,99]))

    test_program = [2,3,0,3,99]
    test_output = run_program(test_program, 3, 0)
    assert all(truth == test for truth, test in zip(test_output, [2,3,0,6,99]))

    test_program = [2,4,4,5,99,0]
    test_output = run_program(test_program, 4, 4)
    assert all(truth == test for truth, test in zip(test_output, [2,4,4,5,99,9801]))

    test_program = [1,1,1,4,99,5,6,0,99]
    test_output = run_program(test_program, 1, 1)
    assert all(truth == test for truth, test in zip(test_output, [30,1,1,4,2,5,6,0,99]))

    print('All Tests Passed!')

    program_memory = read_program('./inputs/day02.txt')
    
    output1 = run_program(program_memory, 12, 2)

    print(f"First answer: {output1[0]}")

    found_it = False
    for noun in range(0, 99):
        for verb in range(0, 99):
            test_output = run_program(program_memory, noun, verb)

            if test_output[0] == 19690720:
                print(f'Found it! Second answer: 100 * {noun} + {verb} = {100 * noun + verb}')
                found_it = True
                break
        if found_it:
            break
