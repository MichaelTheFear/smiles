from itertools import combinations
import json

with open('valency.json') as json_file:
    json_pvals = json.load(json_file)
    
pvals = {ind:obj.get("valencies") for ind, obj in enumerate(json_pvals)}

# ---------------------------------------------------------------------------
# 1. Havel–Hakimi for checking if a valence list is "graphical"
# ---------------------------------------------------------------------------
def havel_hakimi(deg_sequence):
    """
    Classic Havel–Hakimi algorithm to check if 'deg_sequence' 
    is a valid degree sequence of a simple undirected graph.
    """
    # Remove zeros
    deg_sequence = [d for d in deg_sequence if d > 0]

    while True:
        if not deg_sequence:
            return True  # everything used up

        # Sort descending
        deg_sequence.sort(reverse=True)

        # If the largest is 0, then all are 0 => done
        if deg_sequence[0] == 0:
            return True

        # Pop the first (largest)
        d = deg_sequence.pop(0)

        if d > len(deg_sequence):
            return False  # can't "connect" to more vertices than exist

        # Decrement next d elements
        for i in range(d):
            deg_sequence[i] -= 1
            if deg_sequence[i] < 0:
                return False

        # Remove zeros again
        deg_sequence = [x for x in deg_sequence if x > 0]


# ---------------------------------------------------------------------------
# 2. Generating all charge distributions for a given net charge
#    (Brute force: we pick exactly 'net_charge' atoms to adjust by ±1)
# ---------------------------------------------------------------------------
def all_charge_distributions(base_valences, net_charge):
    """
    Yields all possible ways to add or remove 'net_charge' electrons 
    among the atoms in 'base_valences'.
    net_charge > 0 => remove electrons => valence - 1 from 'net_charge' atoms
    net_charge < 0 => add electrons => valence + 1 from 'abs(net_charge)' atoms
    """
    if net_charge == 0:
        # No charge => yield the base list
        yield base_valences
        return

    n = len(base_valences)
    magnitude = abs(net_charge)

    # For each combination of 'magnitude' distinct atoms:
    for combo in combinations(range(n), magnitude):
        valences = base_valences[:]

        if net_charge > 0:
            # We remove 1 electron from each chosen atom => val - 1
            valid = True
            for i in combo:
                if valences[i] == 0:
                    valid = False
                    break
                valences[i] -= 1
            if valid:
                yield valences
        else:
            # net_charge < 0 => add electrons => val + 1
            for i in combo:
                valences[i] += 1
            yield valences


# ---------------------------------------------------------------------------
# 3. Backtracking over all possible valences for each atom
# ---------------------------------------------------------------------------
def backtrack_valences(
    atoms,              # list of atomic numbers, e.g. [7,7,1,1,1,1]
    possible_valences,  # dict: atomic_number -> list of possible valences
    index=0, 
    current_assignment=None
):
    """
    A generator that yields all possible "valence assignments" 
    for the list of atoms.
    
    atoms: list of atomic numbers
    possible_valences: dict, e.g. {7: [3,5,-3], 1: [1]} 
                       meaning N can be 3,5,-3; H can be 1
    index: which atom index we're assigning
    current_assignment: the valences assigned so far
    """
    if current_assignment is None:
        current_assignment = []

    # Base case: if we've assigned valences to all atoms, yield
    if index == len(atoms):
        yield current_assignment
        return

    # The atomic number of the current atom
    z = atoms[index]

    # For each possible valence of this element:
    for v in possible_valences.get(z, []):
        # Append this valence
        current_assignment.append(v)
        # Recurse
        yield from backtrack_valences(atoms, possible_valences, index+1, current_assignment)
        # Remove it to try another valence
        current_assignment.pop()


# ---------------------------------------------------------------------------
# 4. The main function that ties it all together
# ---------------------------------------------------------------------------
def is_valid_molecule_multivalence(
    molecule_list,     # e.g. [(7,2),(1,4)] for N2H4
    possible_valences, # dict: 7: [3,5,-3], 1: [1], etc.
    net_charge=0
):
    """
    1) Expand molecule_list into a 'list of atoms'.
    2) For each atom, try all possible valences from 'possible_valences'.
    3) For each complete assignment, try distributing net_charge 
       in all possible ways.
    4) Check if sum-of-valences is even and run Havel-Hakimi.
    5) Return True if any combination works, else False.
    """

    # Step A: expand e.g. [(7,2),(1,4)] => [7,7,1,1,1,1]
    atoms = []
    for (atomic_num, count) in molecule_list:
        atoms.extend([atomic_num]*count)

    # Step B: backtrack over all possible valence assignments
    for base_valences in backtrack_valences(atoms, possible_valences):
        # Now we have something like [3,5,1,1,1,1] 
        # if the first N took val=3, the second N took val=5, etc.

        # Step C: incorporate net_charge in all possible ways
        for charged_valences in all_charge_distributions(base_valences, net_charge):
            # Step D: check sum-of-valences is even
            s = sum(charged_valences)
            if s % 2 != 0:
                continue

            # Step E: run Havel-Hakimi
            if havel_hakimi(charged_valences):
                return True

    # If we exhaust all combos, it's not valid
    return False


# ---------------------------------------------------------------------------
# 5. Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # possible_valences dictionary:
    # let's say:
    #  - H (1) can only be 1
    #  - N (7) can be 3, 5, or -3
    #  - O (8) can be 2
    #  - etc...

    # Example 1: N2H4 with no net charge
    # i.e. [(7,2),(1,4)] => "atoms" => [7,7,1,1,1,1]
    # We'll see if there's any combination of (3,5,-3) for each N 
    # that yields a valid single-bond structure once we add 4 H with val=1.
    # This might or might not be realistic, but the algorithm will check.
    n2h4 = [(7,2),(1,4)]
    valid_n2h4 = is_valid_molecule_multivalence(n2h4, pvals, net_charge=0)
    print("Is N2H4 valid under these possible valences?", valid_n2h4)

    # Example 2: Let's try NH4+ (ammonium).
    # That would be [(7,1),(1,4)] => [7,1,1,1,1], net_charge=+1
    # We'll see if there's a combo that passes. 
    # Realistically, we might want N=5 for NH4+ or treat it as (N=3 with +1 charge).
    # But the algorithm tries everything in pvals[7] = [3,5,-3],
    # then tries distributing the +1 net charge in all possible ways.
    nh4plus = [(7,1),(1,4)]
    valid_nh4plus = is_valid_molecule_multivalence(nh4plus, pvals, net_charge=+1)
    print("Is NH4+ valid?", valid_nh4plus)
