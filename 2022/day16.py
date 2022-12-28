from rich import print
from utils import load, file_to_lines, file_to_ints
from collections import namedtuple
import heapq
from functools import cmp_to_key


class Valve:

    def __init__(self, key, neighbours, pressure):
        self.key = key
        self.neighbours = neighbours
        self.pressure = pressure

    def __repr__(self):
        return f"{self.key}: {self.pressure} (go to {self.neighbours})"

def get_distance(valves, source, target):
    frontier = set((source, ))
    distance = 0
    while True:
        distance += 1
        new_frontier = set()
        for elem in frontier:
            for neighbour in valves[elem].neighbours:
                new_frontier.add(neighbour)
        if target in new_frontier:
            break
        else:
            frontier = new_frontier
    return distance

def create_distances(valves, non_zero):
    distances = {}
    for elem in non_zero+["AA"]:
        distances[elem] = {}
        for target in non_zero:
            if target != elem:
                distances[elem][target] = get_distance(valves, elem, target)
    return distances


def explore(valves, non_zero, start):
    distances = create_distances(valves, non_zero)
    paths = [(("AA", ), 0, 1)]
    finished_paths = []
    while paths:
        current_path, current_cost, current_time = paths.pop()
        current = current_path[-1]
        found = False
        for next in distances[current].keys():
            if next not in current_path:
                found = True
                new_cost = current_cost + (31-current_time-distances[current][next]-1)*valves[next].pressure
                new_time = current_time + distances[current][next]+1
                new_path = current_path + (next, )
                if new_time > 30:
                    finished_paths.append((current_path, current_cost, current_time))
                else:
                    paths.append((new_path, new_cost, new_time))
        if not found:
            finished_paths.append((current_path, current_cost, current_time))
    sorted_paths = sorted(finished_paths, key=lambda x: x[2])
    max = 0
    for r in sorted_paths:
        if r[1] > max:
            max = r[1]
    return max


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


def get_rest_score(valves, visited, minutes):
    score = 0
    for k, v in valves.items():
        if k not in visited[0] and k not in visited[1] and v.pressure != 0:
            score += v.pressure * (26-min(minutes))
    return score


def explore_elephant(valves, non_zero, start):
    distances = create_distances(valves, non_zero)
    frontier = PriorityQueue()
    frontier.put(((("AA", ), ("AA", )), 0, (1, 1)), 0)
    finished_paths = []
    visited_paths = set()
    starts = set()
    max_cost = 0
    while not frontier.empty():
        current_paths, current_cost, current_times = frontier.get()
        if current_cost > max_cost:
            max_cost = current_cost

        # This is really important!
        if current_cost + get_rest_score(valves, current_paths, current_times) < max_cost:
            continue

        if current_paths in visited_paths:
            finished_paths.append((current_paths, current_cost, current_times))
            continue
        else:
            visited_paths.add(current_paths)
        i_move = False
        e_move = False
        if current_times[0] < current_times[1]:
            i_move = True
        elif current_times[0] > current_times[1]:
            e_move = True
        else:
            i_move, e_move = True, True
        i_path, i_current_time, i_cost = current_paths[0], current_times[0], 0
        e_path, e_current_time, e_cost = current_paths[1], current_times[1], 0
        found, found_i, found_e = False, False, False
        if i_move and e_move:
            i_current, e_current = i_path[-1], e_path[-1]
            for next in distances[i_current].keys():
                i_path, i_current_time, i_cost = current_paths[0], current_times[0], 0
                if next not in i_path and next not in e_path:
                    found, found_i = True, True
                    new_cost = (26-i_current_time-distances[i_current][next])*valves[next].pressure
                    new_time = i_current_time + distances[i_current][next]+1
                    new_path = i_path + (next, )
                    if new_time <= 26:
                        i_path, i_current_time, i_cost = new_path, new_time, new_cost
                    for next_e in distances[e_current].keys():
                        e_path, e_current_time, e_cost = current_paths[1], current_times[1], 0
                        if next_e not in i_path and next_e not in e_path:
                            found, found_e = True, True
                            new_cost = (26-e_current_time-distances[e_current][next_e])*valves[next_e].pressure
                            new_time = e_current_time + distances[e_current][next_e]+1
                            new_path = e_path + (next_e, )
                            if new_time <= 26:
                                e_path, e_current_time, e_cost = new_path, new_time, new_cost
                            if (e_path, i_path) not in starts and (i_path, e_path) not in starts:
                                frontier.put(((i_path, e_path), current_cost+i_cost+e_cost, (i_current_time, e_current_time)), -current_cost-i_cost-e_cost)
                                starts.add((i_path, e_path))

        elif i_move:
            i_current = i_path[-1]
            e_path, e_current_time, e_cost = current_paths[1], current_times[1], 0
            for next in distances[i_current].keys():
                i_path, i_current_time, i_cost = current_paths[0], current_times[0], 0
                if next not in i_path and next not in e_path:
                    found, found_i = True, True
                    new_cost = (26-i_current_time-distances[i_current][next])*valves[next].pressure
                    new_time = i_current_time + distances[i_current][next]+1
                    new_path = i_path + (next, )
                    if new_time <= 26:
                        i_path, i_current_time, i_cost = new_path, new_time, new_cost
                    if (e_path, i_path) not in starts and (i_path, e_path) not in starts:
                        frontier.put(((i_path, e_path), current_cost+i_cost+e_cost, (i_current_time, e_current_time)), -current_cost-i_cost-e_cost)
                        starts.add((i_path, e_path))
                    else:
                        finished_paths.append(((i_path, e_path), current_cost+i_cost+e_cost, (i_current_time, e_current_time)))
        elif e_move:
            e_current = e_path[-1]
            i_path, i_current_time, i_cost = current_paths[0], current_times[0], 0
            for next in distances[e_current].keys():
                if next not in i_path and next not in e_path:
                    e_path, e_current_time, e_cost = current_paths[1], current_times[1], 0
                    found, found_e = True, True
                    new_cost = (27-e_current_time-distances[e_current][next]-1)*valves[next].pressure
                    new_time = e_current_time + distances[e_current][next]+1
                    new_path = e_path + (next, )
                    if new_time <= 26:
                        e_path, e_current_time, e_cost = new_path, new_time, new_cost
                    if (e_path, i_path) not in starts and (i_path, e_path) not in starts:
                        frontier.put(((i_path, e_path), current_cost+i_cost+e_cost, (i_current_time, e_current_time)), -current_cost-i_cost-e_cost)
                        starts.add((i_path, e_path))
                    else:
                        finished_paths.append(((i_path, e_path), current_cost+i_cost+e_cost, (i_current_time, e_current_time)))
        if not found:
            finished_paths.append(((i_path, e_path), current_cost, current_times))
    return max_cost

def sol1(a):
    data = file_to_lines(a)
    valves = {}
    non_zero = []
    for line in data:
        key = line.split(" ")[1]
        rate = int(line.split(";")[0].split("=")[1])
        if rate != 0:
            non_zero.append(key)
        neighbours = " ".join(line.split(" ")[9:]).split(", ")
        valves[key] = Valve(key, neighbours, rate)
    return explore(valves, non_zero, "AA")


def sol2(a):
    data = file_to_lines(a)
    valves = {}
    non_zero = []
    for line in data:
        key = line.split(" ")[1]
        rate = int(line.split(";")[0].split("=")[1])
        if rate != 0:
            non_zero.append(key)
        neighbours = " ".join(line.split(" ")[9:]).split(", ")
        valves[key] = Valve(key, neighbours, rate)
    return explore_elephant(valves, non_zero, "AA")

test = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
asserts_sol1 = {
        test: 1651
        }

asserts_sol2 = {
        test: 1707
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
