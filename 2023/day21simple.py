from rich import print
import sys
import streamlit as st
import os
import functools

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

@functools.lru_cache(maxsize=None)
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

@functools.lru_cache(maxsize=None)
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
    inactive = set([])
    generate = {(0, 0): []}
    lengths = {(0, 0): []}
    known = {(0, 0): set([original, ])}
    for step in range(int(sys.argv[-1])):
        debug = False
        # loop over start quadrant to generate their points
        pos_from_inactive = set()
        for inactive_quadrant in inactive:
            print(f"{inactive_quadrant} is inactive")
            all_new_pos = generate[inactive_quadrant]
            #print(f"{all_new_pos=}")
            new_pos = all_new_pos[-2] if (step-len(all_new_pos))%2 else all_new_pos[-1]
            for pos in new_pos:
                x, y = pos
                quadrant = (x//bounds[0], y//bounds[1])
                if quadrant == inactive_quadrant:
                    print("bug")
                if quadrant not in inactive:
                    pos_from_inactive.add(pos)
        positions.update(pos_from_inactive)
        #print(positions)
        new_positions = {}
        for quadrant in known:
            new_positions[quadrant] = set()
        new_generate = {}
        for pos in positions:
            x, y = pos
            start_quadrant = (x//bounds[0], y//bounds[1])
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
                if quadrant not in new_positions:
                    new_positions[quadrant] = set()
                if quadrant not in lengths:
                    lengths[quadrant] = []
                if start_quadrant not in new_generate:
                    new_generate[start_quadrant] = []
                new_generate[start_quadrant].append(new_pos)
                new_positions[quadrant].add(new_pos)
        for k, v in new_generate.items():
            if k not in generate:
                generate[k] = []
            items = []
            for item in v:
                x, y = item
                q = (x//bounds[0], y//bounds[1])
                if q != k:
                    items.append(item)
            generate[k].append(tuple(items))
        positions = set()
        for quadrant, new_position_set in new_positions.items():
            frozen = frozenset(new_position_set)
            if len(frozen) != 0:
                lengths[quadrant].append(len(frozen))
                if frozen in known[quadrant]:
                    inactive.add(quadrant)
                    print(f"quadrant {quadrant} is looping at step {step}")
                else:
                    known[quadrant].add(frozen)
                    positions.update(frozen)
        #print((step, len(positions)))
    total = len(positions)
    for quadrant in inactive:
        value = lengths[quadrant]
        #print((quadrant, value, step, value[-1] if (step-len(value)) % 2 else value[-2]))
        total += value[-1] if (step-len(value)) % 2 else value[-2]
    return total

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
