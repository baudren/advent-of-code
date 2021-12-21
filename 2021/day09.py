import numpy as np

def sol1(data):
    lows = []
    for i, line in enumerate(data):
        for j, item in enumerate(line):
            low = True
            if j > 0:
                if line[j-1] <= item:
                    low = False
            if j < len(line)-1:
                if line[j+1] <= item:
                    low = False
            if i > 0:
                if data[i-1][j] <= item:
                    low = False
            if i < len(data)-1:
                if data[i+1][j] <= item:
                    low = False
            if low:
                lows.append(item)
    return np.sum(np.array(lows)+1)

def sol2(data):
    basins = []
    for i, line in enumerate(data):
        for j, item in enumerate(line):
            low = True
            if j > 0:
                if line[j-1] <= item:
                    low = False
            if j < len(line)-1:
                if line[j+1] <= item:
                    low = False
            if i > 0:
                if data[i-1][j] <= item:
                    low = False
            if i < len(data)-1:
                if data[i+1][j] <= item:
                    low = False
            if low:
                basin = explore_basin(data, i, j)
                basins.append(len(basin))

    basins = np.array(basins)
    args = basins.argsort()[-3:]
    return np.product(basins[args])


def explore_basin(data, i, j):
    basin = {}
    explore_basin_rec(basin, data, i, j)
    return basin

def explore_basin_rec(basin, data, i, j):
    basin[(i, j)] = True
    item = data[i][j]
    if j > 0:
        if data[i][j-1] >= item and data[i][j-1] != 9 and (i, j-1) not in basin:
            explore_basin_rec(basin, data, i, j-1)
    if j < len(data[0])-1:
        if data[i][j+1] >= item and data[i][j+1] != 9 and (i, j+1) not in basin:
            explore_basin_rec(basin, data, i, j+1)
    if i > 0:
        if data[i-1][j] >= item and data[i-1][j] != 9 and (i-1, j) not in basin:
            explore_basin_rec(basin, data, i-1, j)
    if i < len(data)-1:
        if data[i+1][j] >= item and data[i+1][j] != 9 and (i+1, j) not in basin:
            explore_basin_rec(basin, data, i+1, j)


if __name__ == "__main__":
    data = np.array([int(e) for f in open('day09.txt').readlines() for e in f.strip()]).reshape(100,100)
    test = np.array([int(e) for f in """2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n") for e in f]).reshape(5,10)
    assert sol1(test) == 15
    print(sol1(data))
    assert sol2(test) == 1134
    print(sol2(data))