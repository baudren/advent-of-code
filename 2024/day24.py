import math
from rich import print
from utils import *
from collections import defaultdict

basic_transform = file_to_lines

def apply(w1, op, w2):
    if op == 'AND':
        return 1 if w1 == 1 and w2 == 1 else 0
    elif op == 'OR':
        return 1 if w1 == 1 or w2 == 1 else 0
    elif op == 'XOR':
        return 1 if w1 != w2 else 0

def sol1(data):
    wires = {}
    for i, line in enumerate(data):
        if line == "":
            break
        wire, value = line.split(": ")
        value = int(value)
        wires[wire] = value
    
    operators = []
    for line in data[i+1:]:
        w1, op, w2 = line.split(' -> ')[0].split()
        o = line.split(' -> ')[1]
        if w1 in wires and w2 in wires:
            wires[o] = apply(wires[w1], op, wires[w2])
        else:
            operators.append((w1,op,w2,o))
    
    return solve(wires.copy(), operators.copy())

def get_full_value(wires, s):
    all_s = []
    for wire in wires:
        if wire.startswith(s):
            all_s.append(wire)
    all_s.sort(reverse=True)
    all_s_str = "".join([str(wires[e]) for e in all_s])
    all_s_value = int(all_s_str, 2)
    return all_s_value
    

def solve(wires, operators):
    prev_len = len(wires)
    while operators:
        remaining = []
        for pair in operators:
            w1,op,w2,o = pair
            if w1 in wires and w2 in wires:
                wires[o] = apply(wires[w1], op, wires[w2])
            else:
                remaining.append(pair)
        operators = remaining
        if len(wires) == prev_len:
            print("Problem")
            print(remaining)
            break
        else:
            prev_len = len(wires)
    return get_full_value(wires, 'z')


def build_actual_chain(rev_operators, output):
    if output in rev_operators:
        w1, op, w2 = rev_operators[output]
        if not w1.startswith('x') and not w1.startswith('y'):
            a = build_actual_chain(rev_operators, w1)
        else:
            a = w1
        if not w2.startswith('x') and not w2.startswith('y'):
            b = build_actual_chain(rev_operators, w2)
        else:
            b = w2
        if a.startswith('x') or b.startswith('x'):
            num = int(a[1:])
            s = f"{num:2d}{op}"
        else:
            s = f"({a} {rev_operators[output][1]} {b})"
        return s
    else:
        return output

from itertools import combinations

def sol2(data):
    wires = {}
    for index, line in enumerate(data):
        if line == "":
            break
        wire, value = line.split(": ")
        value = int(value)
        wires[wire] = value
    operators = []
    rev_operators = {}
    for line in data[index+1:]:
        w1, op, w2 = line.split(' -> ')[0].split()
        o = line.split(' -> ')[1]
        operators.append((w1,op,w2,o))
        rev_operators[o] = (w1, op, w2)
    x = get_full_value(wires, 'x')
    y = get_full_value(wires, 'y')
    print(x+y, f"{x+y:0b}")
    xyb = f"{x+y:0b}"
    z = solve(wires.copy(), operators.copy())
    print(z, f"{z:0b}")
    zb = f"{z:0b}"

    # By comparing the above with the value by part1, up until y20, all is well
    for i in range(20, 46):
        # check the actual transformations, going up to x and y.
        # Starting at around 20, there are some "errors".
        # for z00 = x00 XOR y00, which is the case
        # for z01 = X01 XOR y01 XOR (x00 AND y00) (carry), which is the case
        # but starting from z02, there are some additional terms that cancel out each other, for me
        # z02 = (x02 XOR y02) XOR ( (x01 AND y01) OR (some stuff))
        # the some stuff usually, thanks to the OR, cancels out and leaves the carry.
        # By looking at the chains printed below, I identified the four swaps needed, in my case
        # the 21, 26, 33 and 39 were wrong, so I constructed manually the swaps to be done
        # I don't know how to program this.....
        chain = build_actual_chain(rev_operators, f"z{i:02d}")
        print(chain)

    swaps = {
        'shh': 'z21',
        'z21': 'shh',
        'vgs': 'dtk',
        'dtk': 'vgs',
        'dqr': 'z33',
        'z33': 'dqr',
        'pfw': 'z39',
        'z39': 'pfw',
    }
    operators = []
    rev_operators = {}
    for line in data[index+1:]:
        w1, op, w2 = line.split(' -> ')[0].split()
        o = line.split(' -> ')[1]
        o = swaps.get(o, o)
        operators.append((w1,op,w2,o))
        rev_operators[o] = (w1, op, w2)
    print('               '+'9876543210'*5)
    print(x+y, f"x+y={x+y:0b}")
    xyb = f"{x+y:0b}"
    z = solve(wires.copy(), operators.copy())
    print(z, f"z=  {z:0b}")
    zb = f"{z:0b}"
    print(f"{x+y=} {z=} {x+y==z = }")
    return ",".join(sorted(swaps.keys()))
    

data = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
data = load()

data = basic_transform(data)


print(sol1(data))
print(sol2(data))
