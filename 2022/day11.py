from rich import print
from utils import load, file_to_lines, file_to_ints


class Monkey:

    def __init__(self, text):
        self.index = text.splitlines()[0].split()[1][0]
        self.objects = [int(e) for e in text.splitlines()[1].split(": ")[1].split(", ")]
        self.operation = text.splitlines()[2].split(" = ")[1]
        self.test = int(text.splitlines()[3].split(" by ")[1])
        self.if_true = text.splitlines()[4].split(" monkey ")[1]
        self.if_false = text.splitlines()[5].split(" monkey ")[1]
        self.activity = 0

    def add_item(self, item):
        self.objects.append(item)

    def take_turn(self):
        if self.objects:
            self.activity += 1
            item = self.objects.pop(0)
            item = eval(self.operation.replace("old", str(item)))
            item = int(item/3)
            if item % self.test == 0:
                return self.if_true, item
            else:
                return self.if_false, item
        else:
            return (-1, -1)

    def take_turn_2(self, gcm):
        if self.objects:
            self.activity += 1
            item = self.objects.pop(0)
            item = eval(self.operation.replace("old", str(item)))
            item = item % gcm
            if item % self.test == 0:
                return self.if_true, item
            else:
                return self.if_false, item
        else:
            return (-1, -1)

    def __repr__(self):
        return f"{self.index}, {self.objects}, {self.operation}, {self.test}, {self.if_true}, {self.if_false}"

def sol1(a):
    monkeys = {}
    for text in a.split("\n\n"):
        monkey = Monkey(text)
        monkeys[monkey.index] = monkey
    for round in range(20):
        for k in monkeys:
            while True:
                target, item = monkeys[k].take_turn()
                if target == -1:
                    break
                else:
                    monkeys[target].add_item(item)
    activity = []
    for k in monkeys:
        activity.append(monkeys[k].activity)
    activity.sort()
    return activity[-2]*activity[-1]


def sol2(a):
    monkeys = {}
    gcm = 1
    for text in a.split("\n\n"):
        monkey = Monkey(text)
        monkeys[monkey.index] = monkey
        gcm *= monkey.test

    for round in range(10000):
        activity = []
        for k in monkeys:
            while True:
                target, item = monkeys[k].take_turn_2(gcm)
                if target == -1:
                    break
                else:
                    monkeys[target].add_item(item)
            activity.append(monkeys[k].activity)
    activity.sort()
    return activity[-2]*activity[-1]

test = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""
asserts_sol1 = {
    test: 10605
    }

asserts_sol2 = {
    test: 2713310158
    }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
