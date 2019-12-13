from typing import List
from itertools import permutations
from day05 import IntcodeComputer, read_program


def run_amplifiers(program: List[int], input_value: int, phases: List[int]) -> int:

    amplifiers: List[IntcodeComputer] = [IntcodeComputer(program) for name in 'ABCDE']

    for phase, amp in zip(phases, amplifiers):
        output = amp.run(phase, input_value)[0]
        input_value = output

    return output


def run_amplifiers_with_feedback(program: List[int], input_value: int, phases: List[int]) -> int:

    amplifiers: List[IntcodeComputer] = [IntcodeComputer(program) for name in 'ABCDE']
    program_state: List[int] = [-1 for name in 'ABCDE']  # -1 for not initialized, 0 for executing, 1 for done

    while program_state[-1] <= 0:
        for i, amp in enumerate(amplifiers):
            if program_state[i] < 0:
                output = amp.run_and_halt(phases[i], input_value)
                program_state[i] = 0
            elif program_state[i] == 0:
                output = amp.run_and_halt(input_value)
            else:
                continue
                
            if output is not None:
                input_value = output
            else:
                program_state[i] = 1

    return input_value


if __name__ == '__main__':
    test_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert run_amplifiers(test_program, 0, [4, 3, 2, 1, 0]) == 43210

    test_program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert run_amplifiers(test_program, 0, [0, 1, 2, 3, 4]) == 54321

    test_program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert run_amplifiers(test_program, 0, [1, 0, 4, 3, 2]) == 65210


    test_program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    assert run_amplifiers_with_feedback(test_program, 0, [9,8,7,6,5]) == 139629729

    test_program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    assert run_amplifiers_with_feedback(test_program, 0, [9,7,8,5,6]) == 18216

    amplifier_program = read_program('./inputs/day07.txt')
    
    results = []
    for phases in permutations(range(5)):

        amp_output = run_amplifiers(amplifier_program, 0, phases)

        results.append((phases, amp_output))

    max_output_phases = max(results, key=lambda x: x[1])

    print(f'Max output: {str(max_output_phases[1])} from phases {str(max_output_phases[0])}')

    results = []
    for phases in permutations(range(5, 10)):

        amp_output = run_amplifiers_with_feedback(amplifier_program, 0, phases)

        results.append((phases, amp_output))

    max_output_phases = max(results, key=lambda x: x[1])

    print(f'Max output with feedback loop: {str(max_output_phases[1])} from phases {str(max_output_phases[0])}')
