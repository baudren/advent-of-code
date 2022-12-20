from rich import print
from utils import load, file_to_lines, file_to_ints

def parse_costs(cost_line):
    costs = {}
    for item in cost_line.split(" and "):
        quantity, type = int(item.split(" ")[0]), item.split(" ")[1]
        costs[type] = quantity
    return costs

ores = ["geode", "obsidian", "clay", "ore"]
higher = ["geode", "obsidian", "clay"]

class Blueprint:

    def __init__(self, line):
        self.index = int(line.split(":")[0].split(" ")[1])
        self.robot_costs = {
            "ore": parse_costs(line.split(".")[0].split(" costs ")[1]),
            "clay": parse_costs(line.split(".")[1].split(" costs ")[1]),
            "obsidian": parse_costs(line.split(".")[2].split(" costs ")[1]),
            "geode": parse_costs(line.split(".")[3].split(" costs ")[1]),
        }
        self.robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        self.items = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        print(self.robot_costs)

    def quality(self, minutes):
        max_ore_cost = max([self.robot_costs[ore]["ore"] for ore in ores])
        print(max_ore_cost)
        # Each active robots collects one item
        self.robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        self.items = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        for minute in range(1, minutes+1):
            # Do we have max_ore_cost ore-collecting robots?
            new_robots = {}
            if self.robot_costs["ore"]["ore"] < max_ore_cost and self.robots["ore"] < max_ore_cost:
                if self.items["ore"] >= self.robot_costs["ore"]["ore"]:
                    new_robots["ore"] = 1
                    self.items["ore"] -= self.robot_costs["ore"]["ore"]
            else:
                for ore in ores:
                    can_build = True
                    for type, cost in self.robot_costs[ore].items():
                        if self.items[type] < cost:
                            can_build = False
                    if can_build:
                        new_robots[ore] = 1
                        for type, cost in self.robot_costs[ore].items():
                            self.items[type] -= cost
                        break

            for robot in self.robots:
                self.items[robot] += self.robots[robot]
            # Robots are ready
            for k, v in new_robots.items():
                self.robots[k] += v
            print(minute)
            print(f"{self.items=}")
            print(f"{self.robots=}")
            print()
            input()
        return self.index*self.items["geode"]

def sol1(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        blueprint = Blueprint(line)
        total += blueprint.quality(24)
    return total


def sol2(a):
    data = file_to_lines(a)
    return 0

test = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""
asserts_sol1 = {
        test: 33
        }
# answer not 1136

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
