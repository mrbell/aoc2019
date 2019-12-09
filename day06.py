from __future__ import annotations
from typing import List, Dict, Tuple, Union


class OrbitalBody(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self._orbital_host: OrbitalBody = None
        self.bodies_in_orbit: List[OrbitalBody] = []
    
    @property
    def orbital_host(self) -> OrbitalBody:
        return self._orbital_host

    @orbital_host.setter
    def orbital_host(self, orbital_host: OrbitalBody) -> None:
        self._orbital_host = orbital_host

    def add_body_in_orbit(self, orbiting_body: OrbitalBody) -> None:
        self.bodies_in_orbit.append(orbiting_body)

    def get_all_orbital_hosts(self) -> List[OrbitalBody]:
        if self.orbital_host is None:
            return []
            
        host = self.orbital_host
        all_hosts = [host]
        while host.orbital_host is not None:
            host = host.orbital_host
            all_hosts.append(host)
        return all_hosts

    def distance_from_com(self) -> int:
        return len(self.get_all_orbital_hosts())

    def __repr__(self) -> str:
        return f"OrbitalBody({self.name})"


class OrbitalMap(object):
    def __init__(self, orbit_map_specification: List[Tuple[str, str]]):
        self.orbital_bodies: Dict[str, OrbitalBody] = {'COM': OrbitalBody('COM')}
        self.load_map(orbit_map_specification)

    def load_map(self, orbit_map_specification: List[Tuple[str, str]]) -> None:
        for pair in orbit_map_specification:
            self.add_orbital_pair(*pair)

    def add_orbital_pair(self, orbital_host_name: str, orbiting_body_name: str) -> None:
        if orbital_host_name not in self.orbital_bodies:
            orbital_host = OrbitalBody(orbital_host_name)
            self.orbital_bodies[orbital_host_name] = orbital_host
        else:
            orbital_host = self.orbital_bodies[orbital_host_name]
        
        if orbiting_body_name not in self.orbital_bodies:
            orbiting_body = OrbitalBody(orbiting_body_name)
            self.orbital_bodies[orbiting_body_name] = orbiting_body
        else:
            orbiting_body = self.orbital_bodies[orbiting_body_name]

        orbiting_body.orbital_host = orbital_host
        orbital_host.add_body_in_orbit(orbiting_body)

    def count_orbits(self):
        count = 0
        for orbital_body_name in self.orbital_bodies:
            current_object = self.orbital_bodies[orbital_body_name]
            while True:
                if current_object.orbital_host is not None:
                    current_object = current_object.orbital_host
                    count += 1
                else:
                    break
        return count

    def orbital_transfers_between(
        self, body_a: Union[str, OrbitalBody], body_b: Union[str, OrbitalBody]
    ) -> int:
        if isinstance(body_a, str):
            body_a = self.orbital_bodies[body_a]
        
        if isinstance(body_b, str):
            body_b = self.orbital_bodies[body_b]
        
        body_a_hosts = sorted(body_a.get_all_orbital_hosts(), key=lambda x: x.distance_from_com())
        body_b_hosts = sorted(body_b.get_all_orbital_hosts(), key=lambda x: x.distance_from_com())

        common_hosts = list(set(body_a_hosts).intersection(set(body_b_hosts)))

        common_hosts = sorted(
            common_hosts, key=lambda x: x.distance_from_com()
        )

        branching_host = common_hosts[-1]

        body_a_to_branch_distance = len(body_a_hosts) - body_a_hosts.index(branching_host) - 1
        body_b_to_branch_distance = len(body_b_hosts) - body_b_hosts.index(branching_host) - 1

        return body_a_to_branch_distance + body_b_to_branch_distance


def parse_orbit_map(map_definition: str) -> List[Tuple[str, str]]:
    return [line.split(')') for line in map_definition.split('\n')]


def load_orbit_map(map_file: str) -> List[Tuple[str, str]]:
    with open(map_file, 'r') as f:
        map_definition = f.read()
    return parse_orbit_map(map_definition)

if __name__ == '__main__':

    test_map_spec = parse_orbit_map('''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L''')

    test_map = OrbitalMap(test_map_spec)
    assert test_map.count_orbits() == 42

    test_map_spec = parse_orbit_map('''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN''')
    test_map = OrbitalMap(test_map_spec)
    assert test_map.orbital_bodies['D'].distance_from_com() == 3
    assert test_map.orbital_bodies['J'].distance_from_com() == 5
    test_hosts = test_map.orbital_bodies['D'].get_all_orbital_hosts()
    test_hosts = [x.name for x in test_hosts]
    assert 'COM' in test_hosts
    assert 'B' in test_hosts
    assert 'C' in test_hosts
    assert test_map.orbital_transfers_between('YOU', 'SAN') == 4

    map_spec = load_orbit_map('./inputs/day06.txt')
    orbital_map = OrbitalMap(map_spec)
    print(f"Number of orbits: {orbital_map.count_orbits()}")

    xfers = orbital_map.orbital_transfers_between('YOU', 'SAN')
    print(f"Orbital transfers between you and Santa: {xfers}")
