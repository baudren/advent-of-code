import math
from rich import print
from utils import *
from collections import defaultdict


basic_transform = file_to_lines

def generate_manhattan_points(x, y, rr):
    points = set()
    for r in range(rr+1):
        for offset in range(r):
            invOffset = r - offset # Inverse offset
            points.add((x + offset, y + invOffset))
            points.add((x + invOffset, y - offset))
            points.add((x - offset, y - invOffset))
            points.add((x - invOffset, y + offset))
    return points

class Graph(BaseGraph):

    def __init__(self, walls, size):
        self.walls = walls
        self.size = size

    def in_bounds(self, node):
        x, y = node
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return node not in self.walls
        return False

    def not_in_bounds(self, node):
        return not self.in_bounds(node)
    
    def neighbors(self, node):
        x, y = node
        neighbors = [
            (x+1, y), (x-1, y), (x, y-1), (x, y+1)
        ]
        return filter(self.in_bounds, neighbors)

    def neighbors_2(self, node):
        x, y = node
        first_neighbors = [
            (x+1, y), (x-1, y), (x, y-1), (x, y+1)
        ]
        # Keep only the ones in the walls
        in_walls = filter(self.not_in_bounds, first_neighbors)
        plus2 = set()
        for in_wall in in_walls:
            plus2.update(self.neighbors(in_wall))
        if node in plus2: plus2.remove(node)
        return plus2

    def neighbors_20(self, node):
        x, y = node
        valids = filter(self.in_bounds, generate_manhattan_points(x, y, 20))
        valids_with_time = {}
        for valid in valids:
            xx, yy = valid
            valids_with_time[valid] = abs(xx-x)+abs(yy-y)
        return valids_with_time

def heuristic(node, goal):
    x, y = node
    xx, yy = goal
    return abs(x-xx)+abs(y-yy)

def sol1(data):
    walls = set()
    for j, line in enumerate(data):
        for i, char in enumerate(line):
            if char == "#": walls.add((i, j))
            elif char == "S": start = (i, j)
            elif char == "E": goal = (i, j)
    g = Graph(walls, (len(data[0]), len(data)))
    came_from, cost_so_far = a_star_search(g, start, goal, heuristic)
    current = goal
    dist = 0
    race_track = {}
    while current:
        race_track[current] = dist
        current = came_from[current]
        dist += 1

    total = 0
    cheats = {}
    for point, normal_score in race_track.items():
        for neighbor in g.neighbors_2(point):
            diff = normal_score - race_track.get(neighbor, normal_score) - 2 # duration of the cheat
            cheats[(point, neighbor)] = diff
            if diff >= 100:
                total += 1
    return total


def sol2(data):
    total = 0
    walls = set()
    for j, line in enumerate(data):
        for i, char in enumerate(line):
            if char == "#": walls.add((i, j))
            elif char == "S": start = (i, j)
            elif char == "E": goal = (i, j)
    g = Graph(walls, (len(data[0]), len(data)))
    came_from, cost_so_far = a_star_search(g, start, goal, heuristic)
    current = goal
    dist = 0
    race_track = {}
    while current:
        race_track[current] = dist
        current = came_from[current]
        dist += 1

    total = 0
    cheats = {}
    for point, normal_score in race_track.items():
        for neighbor, cheat_time in g.neighbors_20(point).items():
            diff = normal_score - race_track.get(neighbor, normal_score) - cheat_time # duration of the cheat
            cheats[(point, neighbor)] = diff
            if diff >= 100:
                total += 1
    return total


data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))