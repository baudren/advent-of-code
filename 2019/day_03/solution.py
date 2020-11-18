import numpy as np
import time

wires = [e.strip().split(",") for e in open('data.txt', 'r').readlines()]
w1, w2 = wires[0], wires[1]

def define_path(wire, path):
    current = path[-1]
    next_segment = wire.pop(0)
    length = int(next_segment[1:])
    for index in range(1, length+1):
        if next_segment[0] == "U":
            path.append((current[0], current[1]+index))
        elif next_segment[0] == "D":
            path.append((current[0], current[1]-index))
        elif next_segment[0] == "R":
            path.append((current[0]+index, current[1]))
        elif next_segment[0] == "L":
            path.append((current[0]-index, current[1]))
    if wire:
        return define_path(wire, path)
    else:
        return path[1:]

path_1 = define_path(w1, [(0, 0)])
path_2 = define_path(w2, [(0, 0)])
path_2_keys = {}
for e in path_2:
    path_2_keys[e] = True

def find_nearest(path1, path2):
    intersections = [e for e in path1 if e in path2]
    distances = [manhattan_distance(e) for e in intersections]
    return manhattan_distance(intersections[distances.index(min(distances))])

def manhattan_distance(pair):
    return abs(pair[0])+abs(pair[1])

print(find_nearest(path_1, path_2_keys))

def part_2(path1, path2_keys, path2):
    intersections = []
    for i, e in enumerate(path1):
        if e in path2_keys:
            intersections.append(i+1+path2.index(e)+1)
    return min(intersections)

print(part_2(path_1, path_2_keys, path_2))