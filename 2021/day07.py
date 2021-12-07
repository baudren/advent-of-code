from aocd import get_data, submit
import numpy as np
from time import time

def sol1(data):
    sol = {}
    best = float('inf')
    for pos in range(max(data)):
        sol[pos] = np.sum(np.abs(data-pos))
        if sol[pos] < best:
            best = sol[pos]
    return int(best)

def sol2(data):
    sol = {}
    best = float('inf')
    for pos in range(max(data)):
        sol[pos] = np.sum(np.abs(data-pos)*(np.abs(data-pos) +1)/2)
        if sol[pos] < best:
            best = sol[pos]
    return int(best)

if __name__ == "__main__":
    #data = np.array([int(e) for e in get_data(day=7, year=2021).split(",")])
    data = np.array(open('day07.txt').readlines()[0].split(","), dtype = np.uint32)
    test = np.array([int(e) for e in "16,1,2,0,4,2,7,1,2,14""".split(",")])
    assert sol1(test) == 37
    print(sol1(data))
    #submit(sol1(data), part="a", day=7, year=2021)
    assert sol2(test) == 168
    print(sol2(data))
    #submit(sol2(data), part="b", day=7, year=2021)