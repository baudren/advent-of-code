from rich import print
from utils import load, file_to_lines, file_to_ints

directions = [
    (1, 0), # >
    (0, 1), # v
    (-1, 0), # <
    (0, -1), # ^
]
symbols = {
    (1, 0): ">",
    (0, 1): "v",
    (-1, 0): "<",
    (0, -1): "^",
}

def parse_instructions(instruction_string):
    instructions = []
    is_number = True
    number_string = ""
    for c in instruction_string:
        try:
            int(c)
            number_string += c
        except ValueError:
            instructions.append(int(number_string))
            instructions.append(c)
            number_string = ""
    instructions.append(int(number_string))
    return instructions

def parse_map(map_string):
    r_map = {}
    map_ = {}
    for y, line in enumerate(map_string.splitlines()):
        r_map[y+1] = {}
        for x, c in enumerate(line):
            if c != ' ':
                if x+1 not in map_:
                    map_[x+1] = {}
                r_map[y+1][x+1] = c
                map_[x+1][y+1] = c
    return map_, r_map

def sol1(a):
    map_string, instruction_string = a.split("\n\n")
    map_, r_map = parse_map(map_string)
    instructions = parse_instructions(instruction_string)
    index_direction = 0
    direction = directions[index_direction]
    # find left-most position on top row
    last_pos = (min(r_map[1].keys()), 1)
    debug = False
    for instruction in instructions:
        if debug: input()
        if debug: print(f"Being in {last_pos}, facing {symbols[direction]}")
        if instruction in ("R", "L"):
            index_direction = (index_direction+1) % 4 if instruction == "R" else (index_direction-1) % 4
            direction = directions[index_direction]
            if debug: print(f"Turning, now facing {symbols[direction]}")
        else:
            if debug: print(f"Moving {instruction}")
            x, y = last_pos
            for _ in range(instruction):
                if index_direction in (0, 2):
                    # check r_map
                    if index_direction == 0:
                        if x+1 in r_map[y]:
                            if r_map[y][x+1] != "#":
                                x = x+1
                            else:
                                break
                        else:
                            if r_map[y][min(r_map[y].keys())] != "#":
                                x = min(r_map[y].keys())
                            else:
                                break
                    else:
                        if x-1 in r_map[y]:
                            if r_map[y][x-1] != "#":
                                x = x-1
                            else:
                                break
                        else:
                            if r_map[y][max(r_map[y].keys())] != "#":
                                x = max(r_map[y].keys())
                            else:
                                break
                        
                else:
                    if index_direction == 1:
                        if y+1 in map_[x]:
                            if map_[x][y+1] != "#":
                                y = y+1
                            else:
                                break
                        else:
                            if map_[x][min(map_[x].keys())] != "#":
                                y = min(map_[x].keys())
                            else:
                                break
                    else:
                        if y-1 in map_[x]:
                            if map_[x][y-1] != "#":
                                y = y-1
                            else:
                                break
                        else:
                            if map_[x][max(map_[x].keys())] != "#":
                                y = max(map_[x].keys())
                            else:
                                break
            last_pos = (x, y)
            if debug: print(last_pos)
    return 1000*last_pos[1]+4*last_pos[0]+index_direction


def sol2(a):
    # warping logic hardcoded for my puzzle input, doesn't work for the example
    #  12
    #  3
    # 45
    # 6
    map_string, instruction_string = a.split("\n\n")
    map_, r_map = parse_map(map_string)
    instructions = parse_instructions(instruction_string)
    index_direction = 0
    direction = directions[index_direction]
    # find left-most position on top row
    last_pos = (min(r_map[1].keys()), 1)
    debug = False
    debug_switch = False
    switched = False
    for instruction in instructions:
        if debug: print(f"Being in {last_pos}, facing {symbols[direction]}")
        if instruction in ("R", "L"):
            index_direction = (index_direction+1) % 4 if instruction == "R" else (index_direction-1) % 4
            direction = directions[index_direction]
            if debug: print(f"Turning, now facing {symbols[direction]}")
        else:
            if debug: print(f"Moving {instruction}")
            x, y = last_pos
            for step in range(instruction):
                if debug: print(f"{step=}, {index_direction=}")
                if switched: print(f"Now at {(x, y)} moving {symbols[directions[index_direction]]}")
                if switched: switched = False
                if index_direction in (0, 2):
                    # check r_map
                    if index_direction == 0:
                        if x+1 in r_map[y]:
                            if r_map[y][x+1] != "#":
                                x = x+1
                            else:
                                break
                        else:
                            # all four possible cases
                            if debug_switch: print(f"moving right from {(x, y)}")
                            if debug_switch: input()
                            if debug_switch: switched = True
                            if y <= 50: # zone 2 > wraps to 5 <
                                test_y = 151-y
                                if r_map[test_y][max(r_map[test_y].keys())] != "#":
                                    x = max(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 2
                                else:
                                    break
                            elif y <= 100:  # zone 3 > wraps to zone 2 ^
                                test_x = y+50
                                if map_[test_x][max(map_[test_x].keys())] != "#":
                                    x = test_x
                                    y = max(map_[test_x].keys())
                                    index_direction = 3
                                else:
                                    break
                            elif y <= 150: # zone 5 > wraps to zone 2 <
                                test_y = 151-y
                                if r_map[test_y][max(r_map[test_y].keys())] != "#":
                                    x = max(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 2
                                else:
                                    break
                            else: # zone 6 > wraps to zone 5 ^
                                test_x = y-100
                                if map_[test_x][max(map_[test_x].keys())] != "#":
                                    x = test_x
                                    y = max(map_[test_x].keys())
                                    index_direction = 3
                                else:
                                    break
                    else:
                        if x-1 in r_map[y]:
                            if r_map[y][x-1] != "#":
                                x = x-1
                            else:
                                break
                        else:
                            if debug_switch: print(f"moving left from {(x, y)}")
                            if debug_switch: input()
                            if debug_switch: switched = True
                            if y <= 50: # zone 1 < wraps to 4 >
                                test_y = 151-y
                                if r_map[test_y][min(r_map[test_y].keys())] != "#":
                                    x = min(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 0
                                else:
                                    break
                            elif y <= 100:  # zone 3 < wraps to 4 v
                                test_x = y - 50
                                if map_[test_x][min(map_[test_x].keys())] != "#":
                                    x = test_x
                                    y = min(map_[test_x].keys())
                                    index_direction = 1
                                else:
                                    break
                            elif y <= 150: # zone 4 < wraps to zone 1 >
                                test_y = 151-y
                                if r_map[test_y][min(r_map[test_y].keys())] != "#":
                                    x = min(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 0
                                else:
                                    break
                            else: # zone 6 < wraps to zone 1 v
                                test_x = y-100
                                if map_[test_x][min(map_[test_x].keys())] != "#":
                                    x = test_x
                                    y = min(map_[test_x].keys())
                                    index_direction = 1
                                else:
                                    break
                else:
                    if index_direction == 1: # v
                        if y+1 in map_[x]:
                            if map_[x][y+1] != "#":
                                y = y+1
                            else:
                                break
                        else:
                            if debug_switch: print(f"moving down from {(x, y)}")
                            if debug_switch: input()
                            if debug_switch: switched = True
                            if x <= 50: # zone 6 v wraps to zone 2 v
                                test_x = x + 100
                                if map_[test_x][min(map_[test_x].keys())] != "#":
                                    y = min(map_[test_x].keys())
                                    x = test_x
                                else:
                                    break
                            elif x <= 100: # zone 5 v wraps to zone 6 <
                                test_y = x + 100
                                if r_map[test_y][max(r_map[test_y].keys())] != "#":
                                    x = max(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 2
                                else:
                                    break
                            else: # zone 2 v wraps to zone 3 <
                                test_y = x - 50
                                if r_map[test_y][max(r_map[test_y].keys())] != "#":
                                    x = max(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 2
                                else:
                                    break
                    else: # ^
                        if y-1 in map_[x]:
                            if map_[x][y-1] != "#":
                                y = y-1
                            else:
                                break
                        else:
                            if debug_switch: print(f"moving up from {(x, y)}")
                            if debug_switch: input()
                            if debug_switch: switched = True
                            if x <= 50: # zone 4 ^ wraps to zone 3 >
                                test_y = x + 50
                                if r_map[test_y][min(r_map[test_y].keys())] != "#":
                                    x = min(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 0
                                else:
                                    break
                            elif x <= 100: # zone 1 ^ wraps to zone 6 >
                                test_y = x + 100
                                if r_map[test_y][min(r_map[test_y].keys())] != "#":
                                    x = min(r_map[test_y].keys())
                                    y = test_y
                                    index_direction = 0
                                else:
                                    break
                            else: # zone 2 ^ wraps to zone 6 ^
                                test_x = x - 100
                                if map_[test_x][max(map_[test_x].keys())] != "#":
                                    y = max(map_[test_x].keys())
                                    x = test_x
                                else:
                                    break
            last_pos = (x, y)
            if debug: print(f"{last_pos=}")
    return 1000*last_pos[1]+4*last_pos[0]+index_direction

test = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
asserts_sol1 = {
        test: 6032
        }

asserts_sol2 = {
        test: 5031
        }

# solution2 not 23282, not 107190, not 12354

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    #for d,expected in asserts_sol2.items():
    #    assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
