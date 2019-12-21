from typing import List, Tuple
from time import time
from math import gcd


class Moon(object):
    def __init__(self, x, y, z, v_x=0, v_y=0, v_z=0) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

    # def __repr__(self) -> str:
    #     return f'Moon(x={self.x}, y={self.y}, z={self.z}, v_x={self.v_x}, v_y={self.v_y}, v_z={self.v_z})'

    def potential_energy(self) -> int:
        return (abs(self.x) + abs(self.y) + abs(self.z))
    
    def kinetic_energy(self) -> int:
        return (abs(self.v_x) + abs(self.v_y) + abs(self.v_z))

    def energy(self) -> int:
        return (
            self.potential_energy() * self.kinetic_energy()
        )
    
    def vector(self) -> Tuple[int]:
        return (self.x, self.y, self.z, self.v_x, self.v_y, self.v_z)


def read_positions(filename: str) -> List[Moon]:
    with open(filename, 'r') as f:
        positions_spec = f.read()
    return parse_positions(positions_spec)


def parse_positions(positions_spec: str) -> List[Moon]:
    moon_positions = positions_spec.split('\n')
    moons = []
    for moon_position in moon_positions:
        position_parts = moon_position.split(',')
        position_x = int(position_parts[0].split('=')[1])
        position_y = int(position_parts[1].split('=')[1])
        position_z = int(position_parts[2].split('=')[1].replace('>', ''))
        moons.append(Moon(position_x, position_y, position_z))
    return moons


def simulate_motion(moons: List[Moon], time_steps: int) -> None:

    for _ in range(time_steps):

        # Update velocity by applying gravity between pairs of moons
        for i, moon_a in enumerate(moons[:-1]):
            for moon_b in moons[i+1:]:
                for coord in ['x', 'y', 'z']:
                    if moon_a.__getattribute__(coord) < moon_b.__getattribute__(coord):
                        moon_a.__setattr__('v_' + coord, moon_a.__getattribute__('v_' + coord) + 1)
                        moon_b.__setattr__('v_' + coord, moon_b.__getattribute__('v_' + coord) - 1)
                    elif moon_a.__getattribute__(coord) > moon_b.__getattribute__(coord):
                        moon_a.__setattr__('v_' + coord, moon_a.__getattribute__('v_' + coord) - 1)
                        moon_b.__setattr__('v_' + coord, moon_b.__getattribute__('v_' + coord) + 1)

            for coord in ['x', 'y', 'z']:
                moon_a.__setattr__(
                    coord, 
                    moon_a.__getattribute__(coord) + moon_a.__getattribute__('v_' + coord)
                )
        
        moon_a = moons[-1]
        for coord in ['x', 'y', 'z']:
            moon_a.__setattr__(
                coord, 
                moon_a.__getattribute__(coord) + moon_a.__getattribute__('v_' + coord)
            )

    return None


def get_state_on_dim(moons: List[Moon], dim: str) -> List[int]:

    dim_state = []
    for m in moons:
        dim_state.extend([getattr(m, dim), getattr(m, 'v_'+dim)])    
    dim_state = tuple(dim_state)

    return dim_state


def lcm(val1: int, val2: int) -> int:
    return int(abs(val1 * val2) / gcd(val1, val2))


def find_steps_to_repeat(moons: List[Moon]) -> int:

    t = 0

    # A dictionary storing states for each moon and the times when the moon was in that state
    seen_states = {dim: {get_state_on_dim(moons, dim): [t]} for dim in 'xyz'}
    any_repeats = {dim: False for dim in 'xyz'}

    while True:
        simulate_motion(moons, 1)
        
        t += 1

        for dim in 'xyz':
            if any_repeats[dim]:
                continue
            
            state_on_dim = get_state_on_dim(moons, dim)

            if state_on_dim in seen_states[dim]:
                seen_states[dim][state_on_dim].append(t)
                any_repeats[dim] = True
            else:
                seen_states[dim][state_on_dim] = [t]

        if all(any_repeats[k] for k in any_repeats):
            break

    repeat_periods = []
    for dim in 'xyz':
        for state in seen_states[dim]:
            if len(seen_states[dim][state]) > 1:
                repeat_periods.append(
                    seen_states[dim][state][1] - seen_states[dim][state][0]
                )
    
    repeat_period = lcm(
        repeat_periods[0], 
        lcm(repeat_periods[1], repeat_periods[2])
    )

    return repeat_period


if __name__ == '__main__':

    # Test
    test_moon = Moon(8, -12, -9, -7, 3, 0)
    assert test_moon.energy() == 290

    assert lcm(18, 28) == 252

    # Test 
    test_positions = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''
    test_moons = parse_positions(test_positions)

    simulate_motion(test_moons, 3)

    assert (
        test_moons[0].x, test_moons[0].y, test_moons[0].z, 
        test_moons[0].v_x, test_moons[0].v_y, test_moons[0].v_z
    ) == (5, -6, -1, 0, -3, 0)

    # Test
    test_moons = parse_positions(test_positions)
    
    assert find_steps_to_repeat(test_moons) == 2772

    # Test
    test_positions = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''
    test_moons = parse_positions(test_positions)

    # Test
    simulate_motion(test_moons, 100)
    total_energy = sum(moon.energy() for moon in test_moons)
    assert total_energy == 1940

    # Test
    test_moons = parse_positions(test_positions)
    test_period = find_steps_to_repeat(test_moons)
    assert test_period == 4686774924

    # Part 1
    moons = read_positions('./inputs/day12.txt')
    simulate_motion(moons, 1000)
    total_energy = sum(moon.energy() for moon in moons)
    print(f"Total energy after 1000 time steps: {total_energy}")

    # Part 2
    moons = read_positions('./inputs/day12.txt')
    repeat_period = find_steps_to_repeat(moons)
    print(f'Steps required to find a repeated state: {repeat_period}')
