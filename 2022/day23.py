from rich import print
from utils import load, file_to_lines, file_to_ints

directions = [
    (0, -1), # N
    (0, 1), # S
    (-1, 0), # W
    (1, 0), # E
]

around = [
    (0, -1),
    (1, -1),
    (-1, -1),
    (0, 1),
    (1, 1),
    (-1, 1),
    (-1, 0),
    (1, 0),
]

def get_boundaries(elves):
    minx, maxx, miny, maxy = 10, 0, 10, 0
    for elf in elves:
        if elf[0] < minx:
            minx = elf[0]
        if elf[0] > maxx:
            maxx = elf[0]
        if elf[1] < miny:
            miny = elf[1]
        if elf[1] > maxy:
            maxy = elf[1]
    return minx, maxx, miny, maxy

def show_elves(elves):
    minx, maxx, miny, maxy = get_boundaries(elves)
    for y in range(miny, maxy+1):
        line = ""
        for x in range(minx, maxx+1):
            if (x, y) in elves:
                line += "#"
            else:
                line += "."
        print(line)


def get_empty_tiles(elves):
    minx, maxx, miny, maxy = get_boundaries(elves)
    return (maxx-minx+1)*(maxy-miny+1) - len(elves)

def propose_moves(elves, index):
    proposed_moves = {}
    reversed_pm = {}
    

    for elf in elves:
        # First check all around, if no one is there, don't move
        free = True
        for test in around:
            if (elf[0]+test[0], elf[1]+test[1]) in elves:
                free = False
                break
        if not free:
            for i in range(4):
                free_dir = True
                index_direction = (index+i) % 4
                direction = directions[index_direction]
                tests = list((direction, ))
                if direction[0] == 0:
                    tests.extend([(1, direction[1]), (-1, direction[1])])
                else:
                    tests.extend([(direction[0], 1), (direction[0], -1)])
                for test in tests:
                    if (elf[0]+test[0], elf[1]+test[1]) in elves:
                        free_dir = False
                if free_dir:
                    move = (elf[0]+direction[0], elf[1]+direction[1])
                    proposed_moves[elf] = move
                    if move in reversed_pm:
                        reversed_pm[move].append(elf)
                    else:
                        reversed_pm[move] = list((elf, ))
                    break
                if not free_dir:
                    continue
                
    return proposed_moves, reversed_pm


def resolve_proposed_moves(elves, proposed_moves, reversed_pm):
    for elf, move in proposed_moves.items():
        if len(reversed_pm[move]) == 1:
            elves.remove(elf)
            elves.add(move)
        

def sol1(a):
    data = file_to_lines(a)
    elves = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "#":
                elves.add((x, y))
    index = 0
    for round in range(10):
        proposed_moves, reversed_pm = propose_moves(elves, index)
        resolve_proposed_moves(elves, proposed_moves, reversed_pm)
        index = (index + 1) % 4
    return get_empty_tiles(elves)


def sol2(a):
    data = file_to_lines(a)
    elves = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "#":
                elves.add((x, y))
    index = 0
    round = 1
    while True:
        proposed_moves, reversed_pm = propose_moves(elves, index)
        if not proposed_moves:
            break
        resolve_proposed_moves(elves, proposed_moves, reversed_pm)
        index = (index + 1) % 4
        round += 1
    return round

test = """.....
..##.
..#..
.....
..##.
....."""
test2 = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
asserts_sol1 = {
        test: 25,
        test2: 110
        }

asserts_sol2 = {
        test2: 20
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
