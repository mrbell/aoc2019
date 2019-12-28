from typing import List, Dict, Any
import math


def parse_signal(signal: str) -> List[int]:
    return [int(v) for v in signal]


def read_signal(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        return parse_signal(f.read())


def apply_pattern(base_pattern: List[int], phase_input_signal: List[int], position: int) -> int:

    pattern = []
    for bpval in base_pattern:
        pattern.extend([bpval] * (position + 1))

    pattern_len = len(pattern)
    total = 0
    pattern_position = 1

    for v in phase_input_signal:

        total += v * pattern[pattern_position]

        pattern_position = (pattern_position + 1) % pattern_len

    return total


def ones_digit(value: int) -> int:
    return int(str(value)[-1])


def FFT(signal: List[int], n_phases: int, verbose: bool=False) -> List[int]:

    base_pattern = [0, 1, 0, -1]

    phase_input_signal = signal.copy()

    for phase in range(n_phases):

        output_signal = []

        for i in range(len(phase_input_signal)):

            result = apply_pattern(base_pattern, phase_input_signal, i)
            output_signal.append(ones_digit(result))

        if verbose and (phase + 1) % 10 == 0:
            print(f'Phase {phase + 1}')

        phase_input_signal = output_signal.copy()

    return output_signal


def lists_equal(list1: List[Any], list2: List[Any]) -> bool:
    if len(list1) != len(list2):
        return False
    
    return all(val1 == val2 for val1, val2 in zip(list1, list2))


if __name__ == '__main__':
    test_signal = parse_signal('12345678')
    test_answer = parse_signal('01029498')

    test_result = FFT(test_signal, 4)
    assert lists_equal(test_result, test_answer)


    test_signal = parse_signal('80871224585914546619083218645595')
    test_answer = parse_signal('24176176')

    test_result = FFT(test_signal, 100)
    assert lists_equal(test_result[:8], test_answer)

    signal = read_signal('./inputs/day16.txt')
    result = FFT(signal, 100, True)

    print(f'Result: {"".join([str(v) for v in result[:8]])}')
