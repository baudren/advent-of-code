import math
from rich import print
from utils import *

basic_transform = file_to_lines

class Graph(BaseGraph):

    def __init__(self, size):
        self.size = size
        self.walls = set()

    def in_bounds(self, node):
        x, y = node
        if node not in self.walls:
            return 0 <= x < self.size and 0 <= y < self.size

    def neighbors(self, node):
        x, y = node
        neighbors = [
            (x+1, y), (x-1, y), (x, y-1), (x, y+1)
        ]
        return filter(self.in_bounds, neighbors)

def heuristic(node, goal):
    x, y = node
    xx, yy = goal
    return abs(x-xx)+abs(y-yy)

def sol1(data):
    if len(data) < 100:
        size = 7
    else:
        size = 71
    g = Graph(size)
    limit = 12 if size == 7 else 1024
    for i, block in enumerate(data):
        if i == limit:
            break
        g.walls.add(tuple([int(e) for e in block.split(",")]))
    goal = (6, 6) if size == 7 else (70, 70)
    came_from, cost_so_far = a_star_search(g, (0, 0), goal, heuristic)
    return cost_so_far[goal]


def sol2(data):
    if len(data) < 100:
        size = 7
    else:
        size = 71
    g = Graph(size)
    goal = (6, 6) if size == 7 else (70, 70)
    for i, block in enumerate(data):
        g.walls.add(tuple([int(e) for e in block.split(",")]))
        came_from, cost_so_far = a_star_search(g, (0, 0), goal, heuristic)
        if not goal in cost_so_far:
            return block


data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))