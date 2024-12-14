from rich import print
from utils import *

basic_transform = file_to_lines

class Robot:

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
    
    def take_turns(self, limits, n):
        x = (self.pos[0]+n*self.vel[0]) % limits[1]
        y = (self.pos[1]+n*self.vel[1]) % limits[0]
        return (x, y)
    
    def __repr__(self):
        return f"{self.pos=}, {self.vel=}"

import numpy as np

def sol1(data):
    robots = []
    for line in data:
        pos = tuple(int(e) for e in line.split(" ")[0][2:].split(","))
        vel = tuple(int(e) for e in line.split(" ")[1][2:].split(","))
        robots.append(Robot(pos, vel))
    limits = (7, 11)
    limits = (103, 101)
    grid = np.zeros(limits)
    for r in robots:
        p = r.take_turns(limits, 100)
        x, y = p
        grid[y][x] += 1
    total = 1
    tl, tr, bl, br = 0,0,0,0
    for x in range(limits[1]//2):
        for y in range(limits[0]//2):
            tl += grid[y][x]
    for x in range(limits[1]//2+1, limits[1]):
        for y in range(limits[0]//2):
            tr += grid[y][x]
    for x in range(limits[1]//2):
        for y in range(limits[0]//2+1, limits[0]):
            bl += grid[y][x]
    for x in range(limits[1]//2+1, limits[1]):
        for y in range(limits[0]//2+1, limits[0]):
            br += grid[y][x]
    return int(tl*tr*bl*br)

from matplotlib import pyplot as plt

def sol2(data):
    robots = []
    for line in data:
        pos = tuple(int(e) for e in line.split(" ")[0][2:].split(","))
        vel = tuple(int(e) for e in line.split(" ")[1][2:].split(","))
        robots.append(Robot(pos, vel))
    #limits = (7, 11)
    limits = (103, 101)
    answer = 0
    for i in range(10000):
        if (i % limits[0]) == 28 and (i % limits[1]) == 77:
            answer = i
            grid = np.zeros(limits)
            for r in robots:
                p = r.take_turns(limits, i)
                x, y = p
                grid[y][x] = 1
            plt.imshow(grid)
            plt.savefig(f'{i:04}.png')
    return answer

data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))