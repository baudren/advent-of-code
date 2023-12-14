import __main__
from collections import namedtuple
import heapq


def get_filename():
    return __main__.__file__.replace(".py", ".txt")

def load():
    return open(get_filename(), 'r').read()

def write_to_file(data):
    with open(get_filename(), 'w') as data_file:
        data_file.write(data.strip())

def file_to_lines(a):
    return a.splitlines()

def file_to_ints(a):
    return [int(l) for l in a.splitlines()]

def line_to_ints(a):
    return [int(l.strip()) for l in a.split(",")]

def line_to_str(a):
    return [l.strip() for l in a.split(",")]


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


class BaseGraph:

    def neighbors(self, node):
        raise NotImplementedError


Location3D = namedtuple('Location3D', 'x y z')

class Graph3d(BaseGraph):
    def __init__(self, grid):
        self.height = len(grid[0])
        self.width = len(grid)
        self.grid = grid
    
    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def neighbors(self, node):
        (x, y, z) = node
        neighbors = [Location3D(x+1, y, 0), Location3D(x-1, y, 0), Location3D(x, y-1, 0), Location3D(x, y+1, 0)]
        results = filter(self.in_bounds, neighbors)
        locs = []
        for r in results:
            if self.grid[r.x][r.y].z - z < 2:
                locs.append(self.grid[r.x][r.y])
        return locs


# heuristic is a function that takes two arguments, returns a value to estimate the distance to the goal
def a_star_search(graph , start, goal, heuristic):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    return came_from, cost_so_far
