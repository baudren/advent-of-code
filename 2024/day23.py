import math
from rich import print
from utils import *
from collections import defaultdict

basic_transform = file_to_lines


def sol1(data):
    connections = defaultdict(set)
    lans = set()
    for line in data:
        a, b = line.split('-')
        connections[a].add(b)
        connections[b].add(a)
        for inter in connections[b].intersection(connections[a]):
            string = ",".join([a,b,inter])
            if a.startswith('t') or b.startswith('t') or inter.startswith('t'): 
                lans.add(string)
    return len(lans)


def find_all_links(connections, a, rest):
    # we know that a, and everything in rest are connected
    # we return the largest set of computers all connected to a and the rest
    o = set()
    for other in connections[a]:
        if other not in rest:
            if all([other in connections[e] for e in rest]):
                o.add(other)
    try_rest = [*rest]+list(o)
    c = [a, *rest]+list(o)
    c.sort()
    if o:
        while True:
            new_c = find_all_links(connections, a, try_rest)
            if new_c == c:
                break
            c = new_c
            try_rest = c.copy()
            try_rest.pop(try_rest.find(a))
    return c


def sol2(data):
    connections = defaultdict(set)
    lans = set()
    for line in data:
        a, b = line.split('-')
        connections[a].add(b)
        connections[b].add(a)
        for inter in connections[b].intersection(connections[a]):
            biggest_link = find_all_links(connections, a, [b, inter])
            lans.add(",".join(biggest_link))

    biggest_lan = ''
    for lan in lans:
        computers = lan.split(",")
        valid = True
        # not sure why this is needed.. but oh well
        for i, computer in enumerate(computers):
            for other in computers[:i]:
                if other not in connections[computer]:
                    valid = False
                    break
        if not valid: continue
        if len(lan) > len(biggest_lan):
            biggest_lan = lan

    return biggest_lan


data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))
