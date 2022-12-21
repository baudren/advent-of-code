from rich import print
from utils import load, file_to_lines, file_to_ints
import heapq

from collections import namedtuple
State = namedtuple("State", "m r i")

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


def parse_costs(cost_line):
    costs = {}
    for item in cost_line.split(" and "):
        quantity, type = int(item.split(" ")[0]), item.split(" ")[1]
        costs[type] = quantity
    return costs

ores = ["ore", "clay", "obsidian", "geode"]
higher = ["geode", "obsidian", "clay"]

class Blueprint:

    def __init__(self, line):
        self.index = int(line.split(":")[0].split(" ")[1])
        self.costs = {
            "ore": parse_costs(line.split(".")[0].split(" costs ")[1]),
            "clay": parse_costs(line.split(".")[1].split(" costs ")[1]),
            "obsidian": parse_costs(line.split(".")[2].split(" costs ")[1]),
            "geode": parse_costs(line.split(".")[3].split(" costs ")[1]),
        }
        print(self.costs)

    def quality(self, minutes):
        return self.index*self.get_max_geodes(minutes)

    def get_max_geodes(self, minutes):
        max_geodes = 0
        robots = (1, 0, 0, 0)
        items = (0, 0, 0, 0)
        max_costs = {o: max([self.costs[t].get(o, 0) for t in ores]) for o in ores}
        max_costs["geode"] = 1000
        frontier = PriorityQueue()
        score = get_score(minutes, robots, items, max_costs)
        frontier.put((minutes, robots, items), -score)
        debug = True # self.costs["geode"]["obsidian"] == 12
        while not frontier.empty():
            minutes_left, robots, items = frontier.get()
            print(minutes_left)
            if debug: print(f"{minutes_left=}, {robots=}, {items=}")
            # Decide which robots could be built, and add this one if we can
            can_build_one_more_robot = False
            for index, ore in enumerate(ores):
                if index == 0 and robots[index] < max_costs[ore]:
                    time = get_time_to_wait(ore, robots, items, self.costs)
                    if minutes_left > time:
                        can_build_one_more_robot = True
                        r, i = list(robots), list(items)
                        r[index] += 1
                        for ii, oo in enumerate(ores):
                            i[ii] += time * robots[ii] - self.costs[ore].get(oo, 0)
                        score = get_score(minutes_left-time, r, i, max_costs)
                        if debug: print(f"Adding: {minutes_left-time},{tuple(r)}, {tuple(i)} with score {-score}")
                        if debug: input()
                        frontier.put((minutes_left-time, tuple(r), tuple(i)), -score)
                elif index >= 0 and robots[index-1] > 0:  # Can only build what we have robots for, for higher level robots
                    if robots[index] < max_costs[ore]: # stop building robots if we have enough of all to build one per turn
                        time = get_time_to_wait(ore, robots, items, self.costs)
                        if minutes_left > time:
                            can_build_one_more_robot = True
                            r, i = list(robots), list(items)
                            r[index] += 1
                            for ii, oo in enumerate(ores):
                                i[ii] += time * robots[ii] - self.costs[ore].get(oo, 0)
                            score = get_score(minutes_left-time, r, i, max_costs)
                            if debug: print(f"Adding: {minutes_left-time},{tuple(r)}, {tuple(i)} with score {-score}")
                            if debug: input()
                            frontier.put((minutes_left-time, tuple(r), tuple(i)), -score)
            if not can_build_one_more_robot:
                #print("Dropping state, can't build more robots")
                #input()
                final_geodes = items[-1]+robots[-1]*minutes_left
                if debug: print(f"geodes: {final_geodes}")
                if final_geodes > max_geodes:
                    max_geodes = final_geodes
        if max_geodes == 0:
            pass #exit()
        return max_geodes

def get_score(minutes_left, robots, items, max_costs):
    weights = [1, 10, 100, 1000]
    score = 0
    for index, ore in enumerate(ores):
        if robots[index] > 0:
            #score += sign(items[index]+robots[index]*minutes_left-max_costs[ore])*weights[index]
            score += (items[index]+robots[index]*minutes_left)*weights[index]
    return score

def get_time_to_wait(ore, robots, items, costs):
    index = ores.index(ore)
    start = list(items)
    time = 1
    while True:
        can_build = True
        for i, o in enumerate(ores):
            if costs[ore].get(o, 0) > start[i]:
                can_build = False
        if can_build:
            break
        time += 1
        for i, o in enumerate(ores):
            start[i] += robots[i]
    return time

# It's useless to have more than max_costs
def sign(x):
    return (x > 0) - (x < 0)

def sol1(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        blueprint = Blueprint(line)
        total += blueprint.quality(24)
    return total


def sol2(a):
    data = file_to_lines(a)
    total = 1
    for line in data[:3]:
        blueprint = Blueprint(line)
        maxg = blueprint.get_max_geodes(32)
        print(maxg)
        total *= maxg
    return total

test = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""
asserts_sol1 = {
        test: 33
        }
# answer not 1136, not 1382, too low, not 1426

asserts_sol2 = {
        test: 0
        }

if __name__ == "__main__":
    data = load()
    #for d,expected in asserts_sol1.items():
    #    assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    #print(f"\n{sol1(data)=}\n")
    #for d,expected in asserts_sol2.items():
    #    assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
