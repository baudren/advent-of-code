from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    data = file_to_lines(a)
    register = 1
    cycle = 1
    total = 0
    for line in data:
        value = 0
        if line == 'noop':
            incr = 1
        else:
            value = int(line.split()[1])
            incr = 2
        for i in range(incr):
            cycle += 1
            if value and i == 1:
                register += value
            if cycle in (20, 60, 100, 140, 180, 220):
                total += cycle*register
    return total


def sol2(a):
    data = file_to_lines(a)
    screen = []
    crt_line = ""
    cycle = 1
    register = 1
    for line in data:
        value = 0
        if line == 'noop':
            incr = 1
        else:
            value = int(line.split()[1])
            incr = 2
        for i in range(incr):
            if cycle in (41, 81, 121, 161, 201):
                screen.append(crt_line)
                crt_line = ""
            if (cycle-1) % 40 in (register-1, register, register+1):
                crt_line += "#"
            else:
                crt_line += "."
            if value and i == 1:
                register += value
            cycle += 1
    screen.append(crt_line)
    return "\n".join(screen)

test = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

asserts_sol1 = {
        test: 13140
        }

asserts_sol2 = {
        test: """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
    print(sol2(data))
