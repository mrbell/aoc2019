from typing import List, Tuple
from time import time


class Moon(object):
    def __init__(self, x, y, z, v_x=0, v_y=0, v_z=0):
        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

    def __repr__(self):
        return f'Moon(x={self.x}, y={self.y}, z={self.z}, v_x={self.v_x}, v_y={self.v_y}, v_z={self.v_z})'

    def potential_energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z))
    
    def kinetic_energy(self):
        return (abs(self.v_x) + abs(self.v_y) + abs(self.v_z))

    def energy(self):
        return (
            self.potential_energy() * self.kinetic_energy()
        )
    
    def vector(self):
        return [self.x, self.y, self.z, self.v_x, self.v_y, self.v_z]


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


def get_moon_vectors(moons: List[Moon]) -> Tuple[int]:

    moon_vectors = []
    for moon in moons:
        moon_vectors.extend(moon.vector())
    return tuple(moon_vectors)


if __name__ == '__main__':

    # Test
    test_moon = Moon(8, -12, -9, -7, 3, 0)
    assert test_moon.energy() == 290

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
    test_positions = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''
    test_moons = parse_positions(test_positions)
    
    seen_states = {
        get_moon_vectors(test_moons): 1
    }

    t = 0
    while True:
        simulate_motion(test_moons, 1)
        pv = get_moon_vectors(test_moons)
        t += 1
        if pv in seen_states:
            break
        else: 
            seen_states[pv] = 1
        
    print(t)

    # Test
    test_positions = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''
    test_moons = parse_positions(test_positions)

    seen_states = {
        get_moon_vectors(test_moons): 1
    }

    t = 0
    timer = time()
    while True:
        simulate_motion(test_moons, 1)
        pv = get_moon_vectors(test_moons)
        t += 1
        if pv in seen_states:
            break
        else: 
            seen_states[pv] = 1
        if (t % 10000) == 0:
            print(t, end=' ')
            print(time() - timer)

    print(t)

    # Test
    simulate_motion(test_moons, 100)
    total_energy = sum(moon.energy() for moon in test_moons)
    assert total_energy == 1940

    # Part 1
    moons = read_positions('./inputs/day12.txt')
    simulate_motion(moons, 1000)
    total_energy = sum(moon.energy() for moon in moons)
    print(f"Total energy after 1000 time steps: {total_energy}")


