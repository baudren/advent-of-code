import math
from rich import print
from utils import *
import re
import sys
sys.setrecursionlimit(100000)

basic_transform = file_to_lines

from itertools import permutations
from collections import deque
from collections import defaultdict
from functools import reduce
from operator import mul

cache = {}

data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
data = load()
data = basic_transform(data)
patterns = list([e for e in data[0].split(", ")])
patterns.sort(key=lambda s: len(s), reverse=False)


def count_match(line):
    if line not in cache:
        if line == "":
            cache[line] = 1
        else:
            valids = list(filter(lambda s: line.startswith(s), patterns))
            if not valids:
                cache[line] = 0
            else:
                cache[line] = sum([1*count_match(line[len(e):]) for e in valids])
    return cache[line]


def sol1(data):
    total = 0
    for i, line in enumerate(data[2:]):
        n = line
        skip = defaultdict(int)
        previous = []
        for i in range(len(line)-1, 0, -1):
            t = count_match(line[i:])
        total += 1 if count_match(line) else 0
    return total

def sol2(data):
    total = 0
    for i, line in enumerate(data[2:]):
        n = line
        skip = defaultdict(int)
        previous = []
        for i in range(len(line)-1, 0, -1):
            t = count_match(line[i:])
        total += count_match(line)
    return total


print(sol1(data))
print(sol2(data))