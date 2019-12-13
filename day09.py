from day05 import IntcodeComputer, read_program

if __name__ == "__main__":
    test_program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    test_computer = IntcodeComputer(test_program)
    output = test_computer.run()
    assert len(output) == len(test_program)
    assert all(o == p for o, p in zip(output, test_program))


    test_program = [109, -1, 4, 1, 99]  # -1
    test_program = [109, -1, 104, 1, 99]  # 1
    test_program = [109, -1, 204, 1, 99]  # 109
    test_program = [109, 1, 9, 2, 204, -6, 99]  # 204
    test_program = [109, 1, 109, 9, 204, -6, 99]  # 204
    test_program = [109, 1, 209, -1, 204, -106, 99]  # 204
    test_computer = IntcodeComputer(test_program)
    output = test_computer.run()
    assert output[0] == 204
    test_program = [109, 1, 3, 3, 204, 2, 99]  # input
    test_program = [109, 1, 203, 2, 204, 2, 99]  # input
    test_computer = IntcodeComputer(test_program)
    output = test_computer.run(234)
    print(test_computer.memory)
    assert output[0] == 234

    test_program = [1102,34915192,34915192,7,4,7,99,0]
    test_computer = IntcodeComputer(test_program)
    output = test_computer.run()[0]
    assert len(str(output)) == 16

    test_program = [104,1125899906842624,99]
    test_computer = IntcodeComputer(test_program)
    output = test_computer.run()[0]
    assert output == test_program[1]

    program = read_program('./inputs/day09.txt')
    computer = IntcodeComputer(program)
    output = computer.run(1)
    assert len(output) == 1

    print(f"BOOST keycode: {output[0]}")

    computer = IntcodeComputer(program)
    output = computer.run(2)
    assert len(output) == 1

    print(f"Distress coordinates: {output[0]}")
