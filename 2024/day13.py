from rich import print
from utils import *

basic_transform = file_to_lines


def blocks(data):
    a, ap = (int(e[2:]) for e in data[0].split(": ")[1].split(", "))
    b, bp = (int(e[2:]) for e in data[1].split(": ")[1].split(", "))
    c, cp = (int(e[2:]) for e in data[2].split(": ")[1].split(", "))
    d = bp*a-ap*b
    if d != 0:
        e = cp*a-c*ap
        m = e/d
        if m == int(m) and m > 0:
            n = (c-b*m)/a
            if n == int(n) and n > 0:
                return 3*n+m
    return 0

def blocks2(data):
    more = 10000000000000
    a, ap = (int(e[2:]) for e in data[0].split(": ")[1].split(", "))
    b, bp = (int(e[2:]) for e in data[1].split(": ")[1].split(", "))
    c, cp = (more+int(e[2:]) for e in data[2].split(": ")[1].split(", "))
    d = bp*a-ap*b
    if d != 0:
        e = cp*a-c*ap
        m = e/d
        if m == int(m) and m > 0:
            n = (c-b*m)/a
            if n == int(n) and n > 0:
                return 3*n+m
    return 0

def sol1(data):
    total = 0
    for i, line in enumerate(data):
        if line == "":
            total += blocks(data[i-3:i])
    total += blocks(data[len(data)-3:])
    return int(total)


def sol2(data):
    total = 0
    for i, line in enumerate(data):
        if line == "":
            total += blocks2(data[i-3:i])
    total += blocks2(data[len(data)-3:])
    return int(total)

data = load()
data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))