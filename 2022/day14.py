from rich import print
from utils import load, file_to_lines, file_to_ints
import numpy as np


def show_stack(stack):
    print(stack)

def evolve(stack, min_x):
    pos = (500-min_x, 0)
    while True:
        stack[pos[0], pos[1]] = '.'
        if stack[pos[0], pos[1]+1] == '.':
            pos = (pos[0], pos[1]+1)
        elif pos[0]-1 < 0:
            return False
        elif stack[pos[0]-1, pos[1]+1] == '.':
            pos = (pos[0]-1, pos[1]+1)
        elif pos[0]+1 > np.shape(stack)[0]-1:
            return False
        elif stack[pos[0]+1, pos[1]+1] == '.':
            pos = (pos[0]+1, pos[1]+1)
        else:
            # on floor
            stack[pos[0], pos[1]] = 'o'
            return True
        stack[pos[0], pos[1]] = '+'
    return True

def evolve2(stack, min_x):
    pos = (500-min_x, 0)
    while True:
        stack[pos[0], pos[1]] = '.'
        if stack[pos[0], pos[1]+1] == '.':
            pos = (pos[0], pos[1]+1)
        elif pos[0]-1 < 0:
            return pos, False
        elif stack[pos[0]-1, pos[1]+1] == '.':
            pos = (pos[0]-1, pos[1]+1)
        elif pos[0]+1 > np.shape(stack)[0]-1:
            return pos, False
        elif stack[pos[0]+1, pos[1]+1] == '.':
            pos = (pos[0]+1, pos[1]+1)
        else:
            # on floor
            stack[pos[0], pos[1]] = 'o'
            return pos, True
        stack[pos[0], pos[1]] = '+'
    return pos, True

def sol1(a):
    data = file_to_lines(a)
    # extract bounds
    min_x = 1000
    max_x = 0
    max_y = 0
    for path in data:
        for pair in path.split(" -> "):
            x, y = tuple([int(e) for e in pair.split(",")])
            if x < min_x: 
                min_x = x
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
    stack = np.full((max_x-min_x+1, max_y+1), '.')
    for path in data:
        current = tuple([int(e) for e in path.split(" -> ")[0].split(",")])
        current = (current[0]-min_x, current[1])
        for pair in path.split(" -> ")[1:]:
            target = tuple([int(e) for e in pair.split(",")])
            target = (target[0]-min_x, target[1])
            if target[0] == current[0]:
                for y in range(min(current[1], target[1]), max(current[1], target[1])+1):
                    stack[target[0], y] = "#"
            elif target[1] == current[1]:
                for x in range(min(current[0], target[0]), max(current[0], target[0])+1):
                    stack[x, target[1]] = "#"
            else:
                print("Should not happen")
                print(pair, current)
                exit()
            current = target
    
    grains = 0
    while True:
        grains += 1
        stack[500-min_x, 0] = '+'
        result = evolve(stack, min_x)
        if not result:
            break
    return grains-1


def sol2(a):
    data = file_to_lines(a)
    # extract bounds
    min_x = 1000
    max_x = 0
    max_y = 0
    for path in data:
        for pair in path.split(" -> "):
            x, y = tuple([int(e) for e in pair.split(",")])
            if x < min_x: 
                min_x = x
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
    min_x, max_x, max_y = -1000, 2000, max_y + 2
    stack = np.full((max_x-min_x+1, max_y+1), '.')
    for x in range(0, max_x-min_x+1):
        stack[x, max_y] = '#'
    for path in data:
        current = tuple([int(e) for e in path.split(" -> ")[0].split(",")])
        current = (current[0]-min_x, current[1])
        for pair in path.split(" -> ")[1:]:
            target = tuple([int(e) for e in pair.split(",")])
            target = (target[0]-min_x, target[1])
            if target[0] == current[0]:
                for y in range(min(current[1], target[1]), max(current[1], target[1])+1):
                    stack[target[0], y] = "#"
            elif target[1] == current[1]:
                for x in range(min(current[0], target[0]), max(current[0], target[0])+1):
                    stack[x, target[1]] = "#"
            else:
                print("Should not happen")
                print(pair, current)
                exit()
            current = target
    
    grains = 0
    while True:
        grains += 1
        stack[500-min_x, 0] = '+'
        pos, result = evolve2(stack, min_x)
        if pos[0] == 500-min_x and pos[1] == 0:
            break
    return grains

test = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
asserts_sol1 = {
        test: 24
        }

asserts_sol2 = {
        test: 93
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
