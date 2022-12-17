from rich import print
from utils import load, file_to_lines, file_to_ints

def show_map(map, highest):
    print()
    for y in range(highest, -1, -1):
        l = "|"
        for x in range(0, 7):
            l += map.get((x, y), '.')
        print(l+"|")
    print("+-------+")
    print()

def show_map_l(map, highest, low):
    print()
    for y in range(highest, low-1, -1):
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

def falling(map, highest, floor=0):
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
    if bottom == floor:
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

# TODO can't move if a shape is blocking, but so maxx < 6
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

def get_new_floor(map, highest, floor):
    min_ = [floor-1 for _ in range(7)]
    for y in range(highest, floor-1, -1):
        for x in range(7):        
            if map.get((x, y), " ") == "#" and y > min_[x]:
                min_[x] = y
    return min(min_)+1

def evolve(map, pattern, start, highest, floor=0):
    steps = 0
    stopped = False
    while not stopped:
        direction = pattern[(start+steps)%len(pattern)]
        move(map, direction, highest-steps)
        stopped = falling(map, highest-steps, floor)
        steps += 1
    floor = get_new_floor(map, highest-steps+6, floor)
    return start + steps, floor

def sol1(pattern):
    i = 0
    map = {}
    highest = 0
    for year in range(2022):
        spawn_block(map, year, highest)
        i, _ = evolve(map, pattern, i, highest)
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
    floor = 0
    for year in range(1_000_000_000_000):
        if year % 100_000 == 0:
            print(year)
        spawn_block(map, year, highest)
        i, new_floor = evolve(map, pattern, i, highest, floor)
        highest = compute_highest(map)
        if new_floor != floor:
            floor = new_floor
            cleanup(map, floor)
            #print(len(map))
        #show_map(map, highest+6)
            #print(floor)
        #input()
    return highest

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
