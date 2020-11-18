import itertools
import matplotlib.pyplot as plt
import re
import mpld3
import numpy as np
data = """<x=-10, y=-10, z=-13>
<x=5, y=5, z=-9>
<x=3, y=8, z=-16>
<x=1, y=3, z=-3>"""

class JupiterOrbits:
    init = []

    def __init__(self, moons):
        self.moons = moons
        for moon in self.moons:
            self.init.append(tuple(e for e in moon.position))
    
    def step_once(self):
        for m, n in itertools.combinations(self.moons, 2):
            m.apply_gravity(n)
        for m in self.moons:
            m.move()

    def step_n(self, n):
        for _ in range(n):
            self.step_once()
            for moon in self.moons:
                print(moon)
            print()
    
    def run_part1(self):
        self.step_n(1000)
        return sum([m.energy() for m in self.moons])
    
    def run_part2(self):
        index = 1
        energies = []
        while True:
            self.step_once()
            index += 1
            curr = []
            for moon in self.moons:
                curr.append(tuple(e for e in moon.position))
            energies.append(sum([m.energy() for m in self.moons]))
            if curr == self.init:
                break
            if index % 10000 == 0:
                print(index)
        return index, energies

class NPOrbits:
    pos = np.zeros((4, 3), dtype=int)
    vel = np.zeros((4, 3), dtype=int)
    period = [0, 0, 0]
    def __init__(self, moons):
        for i, m in enumerate(moons):
            self.pos[i] = m.position
        self.init = self.pos.copy()

    def step_once(self):
        for m, n in itertools.combinations(range(4), 2):
            value = (self.pos[m] < self.pos[n])*1 - (self.pos[m] > self.pos[n])*1
            self.vel[m] += value
            self.vel[n] -= value
        self.pos += self.vel

    def step_n(self, n):
        for _ in range(n):
            self.step_once()
    
    def run_part1(self):
        self.step_n(10)
        return np.dot(np.sum(abs(self.pos), axis=1), np.sum(abs(self.vel), axis=1))

    def run_part2(self):
        index = 1
        while True:
            self.step_once()
            index += 1
            for i, v in enumerate(self.init.T):
                if all(v == self.pos.T[i]) and self.period[i] == 0:
                    print(i, v, self.pos)
                    self.period[i] = index
            if all([e!=0 for e in self.period]):
                break
        return self.period


class Moon:

    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]
    
    def __str__(self):
        return f"pos: {self.position}, vel: {self.velocity}"

    def __repr__(self):
        return self.__str__()
    
    def apply_gravity(self, other):
        for i, v in enumerate(self.position):
            if v > other.position[i]:
                self.velocity[i] -= 1
                other.velocity[i] += 1
            elif v < other.position[i]:
                self.velocity[i] += 1
                other.velocity[i] -= 1
    
    def move(self):
        for i, v in enumerate(self.velocity):
            self.position[i] += v

    def energy(self):
        return sum([abs(e) for e in self.position]) * sum([abs(e) for e in self.velocity])

moons = []
# data = """<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>"""
# data = """<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>"""
for line in data.split("\n"):
    x, y, z = [int(e) for e in re.search("x=(-?\d+).*y=(-?\d+).*z=(-?\d+)", line).groups()]
    moons.append(Moon([x, y, z]))

from time import time
orbits = JupiterOrbits(moons)
t0 = time()
print(orbits.run_part1())
t1 = time()
moons = []
for line in data.split("\n"):
    x, y, z = [int(e) for e in re.search("x=(-?\d+).*y=(-?\d+).*z=(-?\d+)", line).groups()]
    moons.append(Moon([x, y, z]))
t2 = time()
orbits = NPOrbits(moons)
periods = orbits.run_part2()
t3 = time()
print(t3-t2, t1-t0)

from functools import reduce
from math import gcd

def lcm(a, b):
    return int(a * b / gcd(a, b))

def lcms(*numbers):
    return reduce(lcm, numbers)

print(periods)
print(lcms(*periods))
#print(orbits.run_part1())
#index, energies = orbits.run_part2()
#print(energies)
#print(energies.count(energies[0]))
#print([i for i, v in enumerate(energies) if v == energies[0]])
#plt.plot(range(len(energies))[:100], energies[:100])
#plt.show()
#
#from collections import Counter
#print(Counter(energies))
#print(energies[0])
