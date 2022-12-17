from rich import print
from utils import load, file_to_lines, file_to_ints
from time import time

def show_map(map, highest):
    print()
    for y in range(highest, -1, -1):
        l = "|"
        for x in range(0, 7):
            l += map.get((x, y), '.')
        print(l+"|")
    print("+-------+")
    print()

blocks = (
    """####""",
    """.#.
###
.#.""",
    """..#
..#
###""",
    """#
#
#
#""",
    """##
##""",
)

def compute_highest(map):
    highest = 0
    for k in map:
        if k[1] > highest:
            highest = k[1]
    return highest+1

def spawn_block(map, year, highest):
    block = blocks[year % len(blocks)]
    #print(block)
    for y, line in enumerate(block.splitlines()[::-1]):
        for x, c in enumerate(line):
            if c == "#":
                map[(x+2, highest+3+y)] = "@"

def falling(map, highest):
    bottom = 0
    for y in range(highest, highest+6):
        if "@" in [map.get((x,y), " ") for x in range(7)]:
            bottom = y
            break
    count, empty = 0, 0
    ats, next_ats = [], []
    for y in range(highest+6, bottom-1, -1):
        for x in range(7):
            if map.get((x, y), " ") == "@":
                ats.append((x, y))
                next_ats.append((x, y-1))
                count += 1
                if map.get((x, y-1), " ") in (" ", "@"):
                    empty += 1
    if bottom == 0:
        for at in ats:
            map[at] = "#"
        return True
    else:
        # Check if all space below is empty, or another "@"
        if count == empty:
            # drop by one all @ shapes
            for at in ats:
                map.pop(at, None)
            for at in next_ats:
                if map.get(at, " ") == "#":
                    print("ERROR")
                    exit()
                map[at] = "@"
            return False
        else:
            for at in ats:
                map[at] = "#"
            return True

def move(map, direction, highest):
    minx, maxx = 6, 0
    left_stuck, right_stuck = False, False
    ats=[]
    for y in range(highest, highest+7):
        for x in range(7):
            if map.get((x,y), " ") == "@":
                ats.append((x,y))
                if x < minx:
                    minx=x
                if x > maxx:
                    maxx=x
                if map.get((x-1,y), " ") == "#":
                    left_stuck = True
                if map.get((x+1, y), " ") == "#":
                    right_stuck = True
    if direction == ">" and maxx < 6 and not right_stuck:
        for at in ats:
            map.pop(at, None)
        for at in ats:
            map[(at[0]+1, at[1])] = "@"
    elif direction == "<" and minx > 0 and not left_stuck:
        for at in ats:
            map.pop(at, None)
        for at in ats:
            map[(at[0]-1, at[1])] = "@"

def evolve(map, pattern, start, highest):
    t0 = time()
    steps = 0
    stopped = False
    tt = 0
    while not stopped:
        direction = pattern[(start+steps)%len(pattern)]
        move(map, direction, highest-steps)
        stopped = falling(map, highest-steps)
        steps += 1
    return start + steps

def sol1(pattern):
    i = 0
    map = {}
    highest = 0
    floors = [0 for _ in range(7)]
    for year in range(2022):
        spawn_block(map, year, highest)
        i = evolve(map, pattern, i, highest)
        highest = compute_highest(map)
    return highest

def cleanup(map, floor):
    for k in list(map.keys()):
        if k[1] < floor:
            map.pop(k)

def sol2(pattern):
    i = 0
    map = {}
    highest = 0
    concordances = set()
    loop_concordance = ()
    loop_finished = False
    start_highest = 0
    heights = []
    year_start, year_end = 0, 0
    for year in range(1_000_000_000_000):
        spawn_block(map, year, highest)
        i = evolve(map, pattern, i, highest)
        a, b = i%len(pattern), year%len(blocks)
        if (a, b) not in concordances and not loop_concordance:
            concordances.add((a, b))
        elif (a, b) in concordances and not loop_concordance:
            start_highest = highest
            loop_concordance = (a, b)
            year_start = year
        elif (a, b) == loop_concordance and not loop_finished:
            year_end = year
            loop_finished = True
            break
        new_highest = compute_highest(map)
        if loop_concordance:
            heights.append(new_highest-highest)
        highest = new_highest

    diff = 1_000_000_000_000-year_start
    return start_highest+sum(heights)*(diff//len(heights))+sum(heights[:diff%len(heights)])

test = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
asserts_sol1 = {
        test: 3068
        }

asserts_sol2 = {
        test: 1514285714288
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
