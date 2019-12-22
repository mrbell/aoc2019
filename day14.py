from typing import List, Dict, Tuple, Any
from collections import defaultdict
from math import ceil


def read_reactions(filename: str) -> Dict[str, Dict[str, Any]]:
    with open(filename, 'r') as f:
        reaction_sheet = f.read()
    return parse_reactions(reaction_sheet)


def parse_reactions(reaction_sheet: str) -> Dict[str, Dict[str, Any]]:

    reactions = dict()

    reaction_specs = reaction_sheet.split('\n')

    for reaction_spec in reaction_specs:
        in_out = reaction_spec.split(' => ')

        output_parts = in_out[1].split()
        output_type = output_parts[1]
        output_quantity = int(output_parts[0])

        input_specs = in_out[0].split(', ')
        inputs = {}
        for input_spec in input_specs:
            input_parts = input_spec.split()
            inputs[input_parts[1]] = int(input_parts[0])
        
        reactions[output_type] = {'quantity': output_quantity, 'inputs': inputs}

    return reactions


def gather_required_ore(reactions: Dict[str, Any], remainders: Dict[str, int]=None) -> Tuple[int, Dict[str, int]]:

    # Expand the inputs for one fuel as a list of tuples where each tuple is 
    #   (fuel_type, quantity)
    one_fuel = [(k, reactions['FUEL']['inputs'][k]) for k in reactions['FUEL']['inputs']]

    # At times we have to overproduce to create a quantity of an element
    # Keep track of remainders here
    if remainders is None:
        remainders: Dict[str, int] = defaultdict(lambda: 0)
    else: 
        tmp = []

        for fuel_type, fuel_quantity in one_fuel:

            if remainders[fuel_type] > 0 and remainders[fuel_type] <= fuel_quantity:
                fuel_quantity -= remainders[fuel_type]
                remainders[fuel_type] = 0
            elif remainders[fuel_type] > 0 and remainders[fuel_type] > fuel_quantity:
                remainders[fuel_type] -= fuel_quantity
                continue  # We don't have any more of this input required, omit from the list
            tmp.append((fuel_type, fuel_quantity))
        
        one_fuel = tmp

    while any(inp[0] != 'ORE' for inp in one_fuel):
        
        extended_one_fuel = []

        # Iterate through each input in one_fuel, replace with more fundamental inputs

        for fuel_type, fuel_quantity in one_fuel:
            if fuel_type == 'ORE':
                extended_one_fuel.append((fuel_type, fuel_quantity))
                continue

            reaction_min_yield = reactions[fuel_type]['quantity']
            multiplier = ceil(fuel_quantity / reaction_min_yield)
            remainders[fuel_type] += (multiplier * reaction_min_yield - fuel_quantity)

            reaction_inputs = [(k, reactions[fuel_type]['inputs'][k] * multiplier) for k in reactions[fuel_type]['inputs']]
            extended_one_fuel.extend(reaction_inputs)

        # Consolidate one_fuel by type
        consolidated_extended_one_fuel = defaultdict(lambda: 0)
        for fuel_type, fuel_quantity in extended_one_fuel:
            consolidated_extended_one_fuel[fuel_type] += fuel_quantity
        
        # Subtract remainders
        for fuel_type in consolidated_extended_one_fuel:

            if remainders[fuel_type] == 0 or consolidated_extended_one_fuel[fuel_type] == 0:
                continue
            elif remainders[fuel_type] <= consolidated_extended_one_fuel[fuel_type]:
                consolidated_extended_one_fuel[fuel_type] -= remainders[fuel_type]
                remainders[fuel_type] = 0
            elif remainders[fuel_type] > consolidated_extended_one_fuel[fuel_type]:
                remainders[fuel_type] -= consolidated_extended_one_fuel[fuel_type]
                consolidated_extended_one_fuel[fuel_type] = 0

        one_fuel = [
            (k, consolidated_extended_one_fuel[k]) 
            for k in consolidated_extended_one_fuel 
            if (consolidated_extended_one_fuel[k] > 0)
        ]

    return one_fuel[0][1], remainders


def total_fuel_yield(total_ore: int, reactions: Dict[str, Any]) -> int:

    remaining_ore = total_ore
    remainders = None
    total_fuel = 0

    while True:

        # After producing a single unit of fuel, we will have some elements left over that 
        # we can use to reduce the amount of ore we need to produce the next unit of 
        # fuel.
        required_ore, remainders = gather_required_ore(reactions, remainders=remainders)
        if required_ore <= remaining_ore:
            remaining_ore -= required_ore
            total_fuel += 1

            if total_fuel % 10000 == 0:
                print(f'{total_fuel}    {remaining_ore}')
            
            # After some number of iterations, generating one unit of fuel per iteration,
            # we will have no left-over supplies and it's like starting from 
            # iteration 0. So we can see how much fuel we produced and ore we consumed 
            # over that period and repeat. Then we need to iterate one by one 
            # through the remainder.
            if len(remainders) == 0 or all(remainders[k] == 0 for k in remainders):
                
                fuel_per_period = total_fuel
                ore_per_period = total_ore - remaining_ore
                n_complete_periods = int(total_ore / ore_per_period)

                total_fuel = fuel_per_period * n_complete_periods
                remaining_ore = total_ore - ore_per_period * n_complete_periods

        else:
            break

    return total_fuel 


if __name__ == '__main__':

    test_reaction_sheet = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''

    reactions = parse_reactions(test_reaction_sheet)

    total_ore, _ = gather_required_ore(reactions)

    assert total_ore == 31

    test_reaction_sheet = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''

    reactions = parse_reactions(test_reaction_sheet)

    total_ore, _ = gather_required_ore(reactions)

    assert total_ore == 165


    test_reaction_sheet = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF'''
    reactions = parse_reactions(test_reaction_sheet)

    total_ore, _ = gather_required_ore(reactions)

    assert total_ore == 180697

    total_yield = total_fuel_yield(int(1e12), reactions)
    assert total_yield == 5586022

    print('Tests passed!')

    reactions = read_reactions('./inputs/day14.txt')
    total_ore, _ = gather_required_ore(reactions)
    total_yield = total_fuel_yield(int(1e12), reactions)

    print(f"Minimum ORE required for 1 FUEL: {total_ore}")
    # My clever trick didn't work for this one
    print(f"Total FUEL yield from 1 trillion ORE: {total_yield}")
