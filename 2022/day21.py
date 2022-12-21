from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    data = file_to_lines(a)
    monkeys = {}
    numbers = {}
    for line in data:
        monkey = line.split(":")[0]
        try:
            number = int(line.split(": ")[1])
            numbers[monkey] = number
        except:
            operation = line.split(": ")[1]
            first = line.split(": ")[1].split(" ")[0]
            second = line.split(": ")[1].split(" ")[2]
            monkeys[monkey] = (operation, first, second)
    while monkeys:
        for monkey in list(monkeys.keys()):
            op, first, second = monkeys[monkey]
            if first in numbers and second in numbers:
                monkeys.pop(monkey)
                numbers[monkey] = eval(op.replace(first, f"numbers['{first}']").replace(second, f"numbers['{second}']"))
    return int(numbers["root"])


def sol2(a):
    data = file_to_lines(a)
    monkeys = {}
    numbers = {}
    for line in data:
        monkey = line.split(":")[0]
        try:
            number = int(line.split(": ")[1])
            numbers[monkey] = number
            monkeys[monkey] = (number, )
        except:
            operation = line.split(": ")[1]
            first = line.split(": ")[1].split(" ")[0]
            second = line.split(": ")[1].split(" ")[2]
            monkeys[monkey] = (operation, first, second)
    monkeys["root"] = (monkeys["root"][0].replace("+", "=="), monkeys["root"][1], monkeys["root"][2])
    numbers["humn"] = "XXXX"
    #exit()
    # Construct the equation in a first pass
    equations = {}
    while "root" not in equations:
        for monkey in list(monkeys.keys()):
            if len(monkeys[monkey]) == 1:
                equations[monkey] = numbers[monkey]
                continue
            op, first, second = monkeys[monkey]
            if first in equations and second in equations:
                monkeys.pop(monkey)
                equations[monkey] = op.replace(first, "("+str(eval(f"equations['{first}']"))+")").replace(second, "("+str(eval(f"equations['{second}']"))+")")
        #print(f"{equations=}")
    print(equations["root"])
    first, second = equations["root"].split(" == ")
    if "XXXX" in second:
        fixed = int(eval(first))
        variable = second
    else:
        fixed = int(eval(second))
        variable = first
    print(variable)
    g = eval(variable, {"XXXX": 1})
    h = eval(variable, {"XXXX": 2})
    print(g, h)
    b = h
    a = h-g
    print(a, b)
    print((fixed-b)/a)
    return (fixed-b)/a


test = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
asserts_sol1 = {
        test: 152
        }

asserts_sol2 = {
        test: 301
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
