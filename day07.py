from typing import List
from day05 import IntcodeComputer, read_program


def run_amplifiers(program: List[int], input_value: int, phases: List[int]) -> int:

    amplifiers: List[IntcodeComputer] = [IntcodeComputer(program) for name in 'ABCDE']

    for phase, amp in zip(phases, amplifiers):
        output = amp.run(phase, input_value)[0]
        input_value = output

    return output


if __name__ == '__main__':
    test_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert run_amplifiers(test_program, 0, [4, 3, 2, 1, 0]) == 43210

    test_program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert run_amplifiers(test_program, 0, [0, 1, 2, 3, 4]) == 54321

    test_program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert run_amplifiers(test_program, 0, [1, 0, 4, 3, 2]) == 65210

    amplifier_program = read_program('./inputs/day07.txt')
    
    results = []
    for a in range(5):
        for b in range(5):
            if b == a:
                continue
            for c in range(5):
                if c == b or c == a:
                    continue
                for d in range(5):
                    if d == c or d == b or d == a:
                        continue
                    for e in range(5):
                        if e == a or e == b or e == c or e == d:
                            continue
                        
                        amp_output = run_amplifiers(amplifier_program, 0, [a, b, c, d, e])

                        results.append(((a, b, c, d, e), amp_output))

    max_output_phases = max(results, key=lambda x: x[1])

    print(f'Max output: {str(max_output_phases[1])} from phases {str(max_output_phases[0])}')
                        
