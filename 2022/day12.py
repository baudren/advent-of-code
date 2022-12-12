from rich import print
from utils import load, file_to_lines, file_to_ints
from collections import namedtuple
import heapq
Location = namedtuple("Location", "x y z")

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, Location]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: Location, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> Location:
        return heapq.heappop(self.elements)[1]

class Graph:
    def __init__(self, grid):
        self.size = len(grid)
        self.grid = grid
    
    def in_bounds(self, id: Location):
        return id.x >= 0 and id.x <= self.size and id.y >= 0 and id.y <= self.size

    def neighbors(self, id: Location):
        print(f"neighbors of {id}")
        (x, y, z) = id
        neighbors = [Location(x+1, y, 0), Location(x-1, y, 0), Location(x, y-1, 0), Location(x, y+1, 0)]
        results = filter(self.in_bounds, neighbors)
        locs = []
        for r in results:
            if self.grid[r.x][r.y].z - z < 2:
                locs.append(self.grid[r.x][r.y])
        print(locs)
        return locs


def parse(a):
    grid = []
    for j,line in enumerate(a.splitlines()):
        l = []
        for i,elem in enumerate(line):
            if elem == 'S':
                location = Location(x=i, y=j, z=0)
                start = location
            elif elem == 'E':
                location = Location(x=i, y=j, z=ord('z')-ord('a'))
                goal = location
            else:
                location = Location(x=i, y=j, z=ord(elem)-ord('a'))
            l.append(location)
        grid.append(l)
    return grid, start, goal

def heuristic(a: Location, b: Location) -> float:
    return abs(a.z-b.z)

def a_star_search(graph , start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()
        print(f"{current=}")
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
        print(frontier.elements)
    return came_from, cost_so_far

def sol1(a):
    grid, start, goal = parse(a)
    graph = Graph(grid)
    came_from, cost_so_far = a_star_search(graph, start, goal)
    print(grid)
    print(cost_so_far)
    print(cost_so_far[goal])

    return 0


def sol2(a):
    data = file_to_lines(a)
    return 0

test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
asserts_sol1 = {
        test: 31
        }

asserts_sol2 = {
        test: 0
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
