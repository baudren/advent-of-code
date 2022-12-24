from rich import print
from utils import load, file_to_lines, file_to_ints
import heapq

from collections import namedtuple
State = namedtuple("State", "x y m")

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

directions = {
    "<": (-1, 0),
    ">": (1, 0),
    "v": (0, 1),
    "^": (0, -1),
}

def show_winds(winds, size, pos):
    print("".join(["#" for _ in range(size[0])]))
    for y in range(1, size[1]-1):
        line = "#"
        for x in range(1, size[0]-1):
            if (x, y) == pos:
                line += "E"
                if (x, y) in winds:
                    print("ERROR")
                    exit()
            elif (x, y) in winds:
                if len(winds[(x, y)]) == 1:
                    line += winds[(x, y)]
                else:
                    line += str(len(winds[(x, y)]))
            else:
                line += "."
        print(line + "#")
    print("".join(["#" for _ in range(size[0])]))

def evolve_winds(winds, size):
    new_winds = {}
    for pos, wind_string in winds.items():
        for wind in wind_string:
            x, y = (pos[0]+directions[wind][0], pos[1]+directions[wind][1])
            if x == 0:
                x = size[0]-2
            elif x == size[0]-1:
                x = 1
            if y == 0:
                y = size[1]-2
            elif y == size[1]-1:
                y = 1
            if (x, y) in new_winds:
                new_winds[(x, y)] = new_winds[(x, y)] + wind
            else:
                new_winds[(x, y)] = wind
    return new_winds

def decide_move(winds, pos, goal, size):
    # if pos in winds, means we have to move, otherwise we could stay
    # Every step, try to move right if possible, then down if possible, wait if possible, up, left
    can_wait = pos not in winds
    if pos[1] != 0 and pos[0] < goal[0]:
        new = (pos[0]+1, pos[1])
        if new not in winds: # and (new not in old_winds or "<" not in old_winds[new]):
            return new
    if pos[1] < size[1]-1 or pos[0] == goal[0]:
        new = (pos[0], pos[1]+1)
        if new not in winds: # and (new not in old_winds or "^" not in old_winds[new]):
            return new
    if can_wait:
        return pos
    if pos[1] > 1 or pos[0] == 1:
        new = (pos[0], pos[1]-1)
        if new not in winds: # and (new not in old_winds or "v" not in old_winds[new]):
            return new
    if pos[0] > 1:
        new = (pos[0]-1, pos[1])
        if new not in winds: #  and (new not in old_winds or ">" not in old_winds[new]):
            return new
    print("DAMN")
    exit()

def possible_moves(winds, pos, goal, size):
    moves = []
    can_wait = pos not in winds
    if pos[1] != 0 and pos[0] < size[0]-2:
        new = (pos[0]+1, pos[1])
        if new not in winds: # and (new not in old_winds or "<" not in old_winds[new]):
            moves.append(new)
    if pos[1] < size[1]-2 or pos[0] == goal[0]:
        new = (pos[0], pos[1]+1)
        if new not in winds: # and (new not in old_winds or "^" not in old_winds[new]):
            moves.append(new)
    if can_wait:
        moves.append(pos)
    if pos[1] > 1 or pos[0] == goal[0]:
        new = (pos[0], pos[1]-1)
        if new not in winds: # and (new not in old_winds or "v" not in old_winds[new]):
            moves.append(new)
    if pos[1] != size[1]-1 and pos[0] > 1:
        new = (pos[0]-1, pos[1])
        if new not in winds: #  and (new not in old_winds or ">" not in old_winds[new]):
            moves.append(new)
    return moves

def min_reach_goal(start_pos, goal, size, winds_per_minute, offset=0):
    # One star at a time
    pos = start_pos
    frontier = PriorityQueue()
    frontier.put((*pos, offset if offset != 0 else 0), abs(goal[0]-pos[0])+abs(goal[1]-pos[1]))
    visited = set()
    debug = False#offset != 0
    if debug: print(f"{start_pos=}, {goal=}")
    if debug: input()
    while not frontier.empty():
        x, y, m = frontier.get()
        if ((x, y, m)) in visited:
            continue
        else:
            visited.add((x, y, m))
        pos = (x, y)
        if debug: print(f"{m-offset}")
        if debug: show_winds(winds_per_minute[m], size, pos)
        if False: input()
        if pos == goal:
            return m-offset
        winds = winds_per_minute[m+1]
        moves = possible_moves(winds, pos, goal, size)
        for move in moves:
            #print(move)
            #input()
            dist = abs(goal[0]-move[0])+abs(goal[1]-move[1])
            frontier.put((*move, m+1), dist+m-offset)
        if not moves:
            if debug: print("Stuck")
            if debug: show_winds(winds, size, (0, 0))
            if debug: input()
        
        #show_winds(winds, size, pos)
        #input()

def sol1(a):
    data = file_to_lines(a)
    size = (len(data[0]), len(data))
    start_pos = (1, 0)
    goal = (len(data[0])-2, len(data)-1)
    winds = {}
    for y, line in enumerate(data[1:-1]):
        for x, c in enumerate(line[1: -1]):
            if c in directions:
                winds[(x+1, y+1)] = c
    winds_per_minute = {}
    winds_per_minute[0] = winds
    for m in range(350):
        winds_per_minute[m+1] = evolve_winds(winds_per_minute[m], size)
    steps = min_reach_goal(start_pos, goal, size, winds_per_minute)
    return steps


def sol2(a):
    data = file_to_lines(a)
    size = (len(data[0]), len(data))
    start_pos = (1, 0)
    goal = (len(data[0])-2, len(data)-1)
    winds = {}
    for y, line in enumerate(data[1:-1]):
        for x, c in enumerate(line[1: -1]):
            if c in directions:
                winds[(x+1, y+1)] = c
    winds_per_minute = {}
    winds_per_minute[0] = winds
    for m in range(1200):
        winds_per_minute[m+1] = evolve_winds(winds_per_minute[m], size)
    steps = 0
    steps += min_reach_goal(start_pos, goal, size, winds_per_minute, 0)
    steps += min_reach_goal(goal, start_pos, size, winds_per_minute, steps)
    steps += min_reach_goal(start_pos, goal, size, winds_per_minute, steps)
    return steps

test = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
asserts_sol1 = {
        test: 18
        }

asserts_sol2 = {
        test: 54
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
