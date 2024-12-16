from rich import print
from utils import *

basic_transform = file_to_lines



dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def heuristic(current, target):
    x, y, _ = current
    return abs(target[0]-x)+abs(target[1]-y)

class Graph(BaseGraph):

    def __init__(self, walls):
        self.walls = walls

    def in_bounds(self, node):
        x, y, _ = node
        return (x, y) not in self.walls
        #return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def neighbors(self, node):
        x, y, dir_index = node
        neighbors = [
            (x+dirs[dir_index][0], y+dirs[dir_index][1], dir_index),
            (x, y, (dir_index + 1)%4), 
            (x, y, (dir_index -1 )%4),
            ]
        return filter(self.in_bounds, neighbors)

    def is_fork(self, node):
        x, y, _ = node
        t = 0
        o = [
            (x-1, y),
            (x, y-1),
            (x+1, y),
            (x, y+1),
        ]
        t = sum([1 if self.in_bounds((*e, 0)) else 0 for e in o ])
        return t >= 3

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
        x, y, o = current
        if (x, y) == goal:
            break
        
        for next in graph.neighbors(current):
            if next[0] == current[0] and next[1] == current[1]:
                new_cost = cost_so_far[current] + 1000
            else:
                new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    return came_from, cost_so_far


def sol1(data):
    total = 0
    dir_index = 0
    walls = set()
    goal, start = None, None
    for j, line in enumerate(data):
        for i, char in enumerate(line):
            if char == '#':
                walls.add((i, j))
            elif char == 'S':
                start = (i, j)
            elif char == 'E':
                goal = (i, j)
    start = (*start, 0)
    g = Graph(walls)
    came_from, cost_so_far = a_star_search(g, start, goal, heuristic)
    for i in range(len(dirs)):
        if (*goal, i) in cost_so_far:
            return(cost_so_far[(*goal, i)])


class Path:
    def __init__(self, start, start_cost, max_cost):
        self.visited = set()
        x, y, o = start
        self.current = (x, y, o)
        self.visited.add((x, y))
        self.cost_so_far = start_cost
        self.max_cost = max_cost
        self.forks = set()
    
    def add_next(self, next, cost):
        x, y, o = next
        if (x, y) not in self.visited or (x, y) == (self.current[0], self.current[1]):
            self.visited.add((x, y))
            self.cost_so_far = cost
            self.current = next
            return self.cost_so_far <= self.max_cost
        else:
            return False
    
    def copy_with_next(self, next, cost):
        other = Path(self.current, 0, self.max_cost)
        other.current = self.current
        other.cost_so_far = self.cost_so_far
        other.visited = self.visited.copy()
        other.forks = self.forks.copy()
        if other.add_next(next, cost):
            return other
        return None
    
    def __repr__(self):
        return f"{self.current=} {self.cost_so_far=}"

    def __lt__(self, other):
        return id(self) < id(other)

def mod_a_star_search(graph , start, goal, heuristic, max_cost):
    frontier = PriorityQueue()
    frontier.put((*start, 0), 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = set()
    came_from[start].add(None)
    cost_so_far[start] = set()
    cost_so_far[start].add(0)
    stops = set()

    while not frontier.empty():
        current = frontier.get()
        x, y, o, c = current
        if (x, y) == goal:
            if c == max_cost:
                stops.add((x, y, o))
        for next in graph.neighbors((x, y, o)):
            if next[0] == current[0] and next[1] == current[1]:
                new_cost = min(cost_so_far[(x,y,o)]) + 1000
            else:
                new_cost = min(cost_so_far[(x,y,o)]) + 1
            if next not in cost_so_far or new_cost <= min(cost_so_far[next])+1000:
                if new_cost > max_cost:
                    continue
                if next not in cost_so_far:
                    cost_so_far[next] = set()
                if next in came_from:
                    if (new_cost == min(cost_so_far[next])): 
                        came_from[next].add((x,y,o))
                    elif new_cost < min(cost_so_far[next]):
                        came_from[next] = set()
                        came_from[next].add((x,y,o))
                else:
                    came_from[next] = set()
                    came_from[next].add((x,y,o))
                cost_so_far[next].add(new_cost)
                priority = new_cost + heuristic(next, goal)
                frontier.put((*next, new_cost), priority)
                
    return came_from, stops

def get_parents(came_from, point):
    all_parents = set()
    for parent in came_from[point]:
        if parent:
            all_parents.add(parent)
            all_parents.update(get_parents(came_from, parent))
    return all_parents

def display_parents(parents, g, size):
    points = set([(x, y) for x,y,o in parents])
    for y in range(size[1]):
        l = ""
        for x in range(size[0]):
            if (x, y) in points:
                l += "O"
            elif (x, y) in g.walls:
                l += "#"
            else:
                l += "."
        print(l)


def sol2(data, prev):
    total = 0
    dir_index = 0
    walls = set()
    goal, start = None, None
    for j, line in enumerate(data):
        for i, char in enumerate(line):
            if char == '#':
                walls.add((i, j))
            elif char == 'S':
                start = (i, j)
            elif char == 'E':
                goal = (i, j)
    size = (len(data[0]), len(data))
    start = (*start, 0)
    g = Graph(walls)
    came_from, stops = mod_a_star_search(g, start, goal, heuristic, prev)
    all_parents = set()
    for stop in stops:
        all_parents.add(stop)
        all_parents.update(get_parents(came_from, stop))
    display_parents(all_parents, g, size)
    points = set([(x, y) for x,y,o in all_parents])
    return len(points)


data = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
data = load()

data = basic_transform(data)
max_cost = sol1(data)
# 522 < answer < 561
print(max_cost)
print(sol2(data, max_cost))