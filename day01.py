from typing import List

def load_module_masses(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        raw_file = f.read()
    masses = [int(mass) for mass in raw_file.split('\n')]

    return masses


def calculate_fuel_requirements(mass: int) -> int:
    return mass // 3 - 2


def calculate_fuel_requirements_incl_fuel_mass(mass: int) -> int:
    base_fuel = calculate_fuel_requirements(mass)
    incremental_fuel = base_fuel

    total_fuel = base_fuel

    while incremental_fuel > 0:
        incremental_fuel = max([calculate_fuel_requirements(incremental_fuel), 0])
        total_fuel += incremental_fuel
        if incremental_fuel == 0:
            break

    return total_fuel
    

if __name__ == '__main__':
    
    assert calculate_fuel_requirements(12) == 2
    assert calculate_fuel_requirements(14) == 2
    assert calculate_fuel_requirements(1969) == 654
    assert calculate_fuel_requirements(100756) == 33583
    print('Part 1 tests passed')

    assert calculate_fuel_requirements_incl_fuel_mass(14) == 2
    assert calculate_fuel_requirements_incl_fuel_mass(1969) == 966
    assert calculate_fuel_requirements_incl_fuel_mass(100756) == 50346
    print('Part 2 tests passed')

    masses = load_module_masses('./inputs/day01.txt')

    all_fuel = sum(calculate_fuel_requirements(mass) for mass in masses)
    print(f"Total fuel needed, part 1: {all_fuel}")

    all_fuel_including_self_mass = sum(
        calculate_fuel_requirements_incl_fuel_mass(mass) for mass in masses
    )
    print(f"Total fuel needed, part 2: {all_fuel_including_self_mass}")
