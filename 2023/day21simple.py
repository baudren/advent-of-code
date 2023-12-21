from rich import print
import streamlit as st
import os
import functools

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

@functools.cache
def get_neighbors(pos, walls, bounds):
    neighbors = []
    x, y = pos
    if (x-1, y) not in walls and x-1 >= 0:
        neighbors.append((x-1, y))
    if (x+1, y) not in walls and x+1 < bounds[0]:
        neighbors.append((x+1, y))
    if (x, y-1) not in walls and y-1 >= 0:
        neighbors.append((x, y-1))
    if (x, y+1) not in walls and y+1 < bounds[1]:
        neighbors.append((x, y+1))
    return tuple(neighbors)

@functools.cache
def get_neighbors_2(pos, walls, bounds):
    neighbors = []
    x, y = pos
    if x > 0:
        if (x-1, y) not in walls:
            neighbors.append((x-1, y))
    else:
        if (bounds[0]-1, y) not in walls:
            neighbors.append((x-1, y))
    if x < bounds[0]-2:
        if (x+1, y) not in walls:
            neighbors.append((x+1, y))
    else:
        if (0, y) not in walls:
            neighbors.append((x+1, y))
    if y > 0:
        if (x, y-1) not in walls:
            neighbors.append((x, y-1))
    else:
        if (x, bounds[1]-1) not in walls:
            neighbors.append((x, y-1))
    if y < bounds[0] -2:
        if (x, y+1) not in walls:
            neighbors.append((x, y+1))
    else:
        if (x, 0) not in walls:
            neighbors.append((x, y+1))
    return tuple(neighbors)

def sol1(data):
    positions = set([])
    walls = set([])
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'S':
                positions.add((x, y))
    walls = frozenset(walls)
    bounds = (len(data[0]), len(data))
    for step in range(64):
        new_positions = set()
        for pos in positions:
            for n in get_neighbors(pos, walls, bounds):
                new_positions.add(n)
        positions = new_positions

    total = 0
    return len(positions)


def sol2(data):
    positions = set([])
    walls = set([])
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'S':
                positions.add((x, y))
    walls = frozenset(walls)
    bounds = (len(data[0]), len(data))

    original = frozenset(positions)
    
    # then this loop seeds the neighbor quadrants in a defined way
    # List of active quadrants, starting with the first one, coordinates 0, 0
    inactive = {}
    positions = original.copy()
    known = {(0, 0): set([original, ])}
    print((inactive, positions, known))
    for step in range(100):
        debug = False
        new_positions = {}
        for pos in positions:
            x, y = pos
            # map to first quadrant
            for n in get_neighbors_2((x % bounds[0], y % bounds[1]), walls, bounds):
                xx, yy = n
                xxx, yyy = x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy
                new_pos = xxx, yyy
                quadrant = (xxx//bounds[0], yyy//bounds[1])
                if quadrant in inactive:
                    continue
                if quadrant not in known:
                    known[quadrant] = set()
                new_positions[quadrant].add((xxx, yyy))

                #if debug: print(("neighbors", n))
                #if debug: print((x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy))
                new_positions.add((x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy))
        positions = new_positions

    total = 0
    return len(positions)

data = load()
data = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
#data = load()

data = basic_transform(data)
print(sol2(data))
