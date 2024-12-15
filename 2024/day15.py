from rich import print
from utils import *

basic_transform = file_to_lines

def display(size, walls, boxes, robot):
    for y in range(size[1]):
        l = ""
        for x in range(size[0]):
            if (x, y) in walls:
                l += "#"
            elif (x, y) in boxes:
                l += "O"
            elif (x, y) == robot:
                l += "@"
            else:
                l += '.'
        print(l)
    print()


def attempt_move(size, walls, boxes, robot, move):
    x, y = robot
    to_move = []
    destination = None
    if move == '^':
        for y in range(robot[1]-1, -1, -1):
            if (x, y) in walls:
                break
            elif (x, y) in boxes:
                to_move.append(y)
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0], robot[1]-1)
                boxes.remove((x, max(to_move)))
                boxes.add((x, destination[1]))
    elif move == 'v':
        for y in range(robot[1]+1, size[1]):
            if (x, y) in walls:
                break
            elif (x, y) in boxes:
                to_move.append(y)
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0], robot[1]+1)
                boxes.remove((x, min(to_move)))
                boxes.add((x, destination[1]))
    elif move == '<':
        for x in range(robot[0]-1, -1, -1):
            if (x, y) in walls:
                break
            elif (x, y) in boxes:
                to_move.append(x)
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0]-1, robot[1])
                boxes.remove((max(to_move), y))
                boxes.add((destination[0], y))
    elif move == '>':
        for x in range(robot[0]+1, size[0]):
            if (x, y) in walls:
                break
            elif (x, y) in boxes:
                to_move.append(x)
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0]+1, robot[1])
                boxes.remove((min(to_move), y))
                boxes.add((destination[0], y))
    return boxes, robot

def sol1(data):
    walls = set()
    boxes = set()
    robot = (0, 0)
    size = (len(data[0]), 0)
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'O':
                boxes.add((x, y))
            elif char == '@':
                robot = (x, y)
        if line == "":
            size = (size[0], y)
    display(size, walls, boxes, robot)
    for movements in data[size[1]:]:
        for move in movements:
            boxes, robot = attempt_move(size, walls, boxes, robot, move)
    display(size, walls, boxes, robot)
    return sum([b[0]+100*b[1] for b in boxes])


def display2(size, walls, boxes, robot):
    for y in range(size[1]):
        l = ""
        after = False
        for x in range(size[0]):
            if (x, y) in walls:
                l += "#"
            elif (x, y) in boxes:
                l += "["
                after = True
            elif (x, y) == robot:
                l += "@"
            else:
                if after: 
                    l += "]"
                    after = False
                else: l += '.'
        print(l)
    print()

def attempt_move2(size, walls, boxes, robot, move):
    x, y = robot
    to_move = set()
    destination = None
    if move == '^':
        pushing = set()
        pushing.add(x)
        for y in range(robot[1]-1, -1, -1):
            if any([(e, y) in walls for e in pushing]):
                break
            elif any([(e, y) in boxes or (e-1, y) in boxes for e in pushing]):
                new_pushing = set()
                for e in pushing:
                    if (e, y) in boxes:
                        to_move.add((e, y))
                        new_pushing.update({e, e+1})
                    elif (e-1, y) in boxes:
                        to_move.add((e-1, y))
                        new_pushing.update({e, e-1})
                pushing = new_pushing
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0], robot[1]-1)
                new_b = set()
                for b in to_move:
                    new_b.add((b[0], b[1]-1))
                    boxes.remove(b)
                boxes.update(new_b)
    elif move == 'v':
        pushing = set()
        pushing.add(x)
        for y in range(robot[1]+1, size[1]):
            if any([(e, y) in walls for e in pushing]):
                break
            elif any([(e, y) in boxes or (e-1, y) in boxes for e in pushing]):
                new_pushing = set()
                for e in pushing:
                    if (e, y) in boxes:
                        to_move.add((e, y))
                        new_pushing.update({e, e+1})
                    elif (e-1, y) in boxes:
                        to_move.add((e-1, y))
                        new_pushing.update({e, e-1})
                pushing = new_pushing
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0], robot[1]+1)
                new_b = set()
                for b in to_move:
                    new_b.add((b[0], b[1]+1))
                    boxes.remove(b)
                boxes.update(new_b)
    elif move == '<':
        skip = False
        for x in range(robot[0]-1, -1, -1):
            if skip:
                skip = False
                continue
            if (x, y) in walls:
                break
            elif (x-1, y) in boxes:
                to_move.add((x-1, y))
                skip = True
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0]-1, robot[1])
                new_b = set()
                for b in to_move:
                    new_b.add((b[0]-1, b[1]))
                    boxes.remove(b)
                boxes.update(new_b)
    elif move == '>':
        skip = False
        for x in range(robot[0]+1, size[0]):
            if skip:
                skip = False
                continue
            if (x, y) in walls:
                break
            elif (x, y) in boxes:
                skip = True
                to_move.add((x, y))
            else:
                destination = (x, y)
                break
        if destination:
            if not to_move:
                robot = destination
            else:
                robot = (robot[0]+1, robot[1])
                new_b = set()
                for b in to_move:
                    new_b.add((b[0]+1, b[1]))
                    boxes.remove(b)
                boxes.update(new_b)
    return boxes, robot

def sol2(data):
    walls = set()
    boxes = set()
    robot = (0, 0)
    grid = set()
    size = (len(data[0])*2, 0)
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((2*x, y))
                walls.add((2*x+1, y))
            elif char == 'O':
                boxes.add((2*x, y))
            elif char == '@':
                robot = (2*x, y)
        if line == "":
            size = (size[0], y)
    display2(size, walls, boxes, robot)
    for movements in data[size[1]:]:
        for move in movements:
            boxes, robot = attempt_move2(size, walls, boxes, robot, move)
    display2(size, walls, boxes, robot)
    return sum([b[0]+100*b[1] for b in boxes])

data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))