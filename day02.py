
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


opcodes = {
    1: add_op,
    2: multiply_op,
    99: None,
}


def run_program(original_code: List[int]) -> List[int]:

    code = original_code.copy()

    current_position = 0
    operation = opcodes[
        code[current_position]
    ]

    while operation is not None:
        input1_position = code[current_position + 1]
        input2_position = code[current_position + 2]
        output_position = code[current_position + 3]

        code = operation(code, input1_position, input2_position, output_position)

        current_position += 4
        operation = opcodes[
            code[current_position]
        ]
    
    return code


if __name__ == '__main__':

    test_program = [1,0,0,0,99]
    test_output = run_program(test_program)
    assert all(truth == test for truth, test in zip(test_output, [2,0,0,0,99]))

    test_program = [2,3,0,3,99]
    test_output = run_program(test_program)
    assert all(truth == test for truth, test in zip(test_output, [2,3,0,6,99]))

    test_program = [2,4,4,5,99,0]
    test_output = run_program(test_program)
    assert all(truth == test for truth, test in zip(test_output, [2,4,4,5,99,9801]))

    test_program = [1,1,1,4,99,5,6,0,99]
    test_output = run_program(test_program)
    assert all(truth == test for truth, test in zip(test_output, [30,1,1,4,2,5,6,0,99]))

    print('All Tests Passed!')

    code = read_program('./inputs/day02.txt')

    modified_code = code.copy()
    modified_code[1] = 12
    modified_code[2] = 2
    
    output1 = run_program(modified_code)

    print(f"First answer: {output1[0]}")
    