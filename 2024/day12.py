from rich import print
from utils import *


basic_transform = file_to_lines


def is_in(data, n):
    x, y = n
    return 0 <= x < len(data) and 0 <= y < len(data[0])

def explore(data, pos):
    
    x, y = pos
    local = set()
    frontier = [pos, ]
    a = 0
    p = 0
    while True:
        new = []
        for f in frontier:
            if f in local:
                continue
            x, y = f
            local.add(f)
            a += 1
            ns = [
                (x+1, y),
                (x-1, y),
                (x, y+1),
                (x, y-1),
            ]
            s = 4
            for n in ns:
                if is_in(data, n) and data[n[0]][n[1]] == data[x][y]:
                    s -= 1
                    if n not in local:
                        new.append(n)
            p += s
        if not new:
            break
        frontier = new
    return a*p, local

def sol1(data):
    explored = set()
    total = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if (i, j) not in explored:
                f, s = explore(data, (i, j))
                total += f
                explored.update(s)
    return total


def explore2(data, pos):
    local = set()
    frontier = [pos, ]
    c = data[pos[0]][pos[1]]
    a = 0
    while True:
        new = []
        for f in frontier:
            if f in local:
                continue
            x, y = f
            local.add(f)
            a += 1
            ns = [
                (x+1, y),
                (x-1, y),
                (x, y+1),
                (x, y-1),
            ]
            for n in ns:
                if is_in(data, n) and data[n[0]][n[1]] == c:
                    if n not in local:
                        new.append(n)
        if not new:
            break
        frontier = new
    sides = 0
    for i in range(len(data)):
        u, d = False, False
        for j in range(len(data[0])):
            if (i, j) in local:
                if not is_in(data, (i-1, j)) or data[i-1][j] != c:
                    if not u:
                        u = True
                else:
                    if u:
                        sides += 1
                    u = False
                if not is_in(data, (i+1, j)) or data[i+1][j] != c:
                    if not d:
                        d = True
                else:
                    if d:
                        sides += 1
                    d = False
            else:
                if u:
                    sides += 1
                    u = False
                if d:
                    sides += 1
                    d = False
        if u:
            sides += 1
        if d:
            sides += 1
    for j in range(len(data[0])):
        l, r = False, False
        for i in range(len(data)):
            debug = j == 4
            debug = False
            if debug: print(f"{(i, j)=}")
            if (i, j) in local:
                if not is_in(data, (i, j-1)) or data[i][j-1] != c:
                    if not l:
                        l = True
                else:
                    if l:
                        sides += 1
                    l = False
                if not is_in(data, (i, j+1)) or data[i][j+1] != c:
                    if not r:
                        r = True
                else:
                    if r:
                        sides += 1
                    r = False
            else:
                if l:
                    sides += 1
                    l = False
                if r:
                    sides += 1
                    r = False
        if l:
            sides += 1
        if r:
            sides += 1
    return a*sides, local
    

def sol2(data):
    explored = set()
    total = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if (i, j) not in explored:
                f, s = explore2(data, (i, j))
                total += f
                explored.update(s)
    return total

data = load()
data = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
data = load()
data = basic_transform(data)
print(sol1(data))
print(sol2(data))