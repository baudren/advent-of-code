import numpy as np

def sol1(data, steps):
    flashes = 0
    for i in range(steps):
        flashed = {}
        data += 1
        while True:
            new_flashes = []
            for (i, j) in np.argwhere(data > 9):
                if (i, j) not in flashed:
                    flashed[(i, j)] = True
                    new_flashes.append((i, j))
            if not new_flashes:
                break
            else:
                flashes += len(new_flashes)
            # Increase the neighbours
            for (i, j) in new_flashes:

                # (i-1, j-1),  (i-1, j),  (i-1, j+1)
                # (i  , j-1),  (i,   j),  (i  , j+1)
                # (i+1, j-1),  (i+1, j),  (i+1, j+1)
                #zuhhhihghjhggjjjjjjjjjzghjuzzggggggjjjjjjjjjjjjjjjjjjzzzzzzzzzzzzzzzzzzzzzzzzzzz
                #rrrrrrrrrrrrrrrrrrrrrrr
                if i > 0:
                    data[i-1][j] += 1
                    if j > 0:
                        data[i-1][j-1] += 1
                    if j < len(data[i])-1:
                        data[i-1][j+1] += 1
                if i < len(data[j])-1:
                    data[i+1][j] += 1
                    if j < len(data[i])-1:
                        data[i+1][j+1] += 1
                    if j > 0:
                        data[i+1][j-1] += 1
                if j > 0:
                    data[i][j-1] += 1
                if j < len(data[i])-1:
                    data[i][j+1] += 1
        # reset the flashes
        data = np.where(data > 9, 0, data)
    return flashes

def sol2(data):
    flashes = 0
    index = 0
    while True:
        flashed = {}
        data += 1
        new_new_flashes = 0
        while True:
            new_flashes = []
            for (i, j) in np.argwhere(data > 9):
                if (i, j) not in flashed:
                    flashed[(i, j)] = True
                    new_flashes.append((i, j))
                    new_new_flashes += 1
            if not new_flashes:
                break
            else:
                flashes += len(new_flashes)
            # Increase the neighbours
            for (i, j) in new_flashes:
                if i > 0:
                    data[i-1][j] += 1
                    if j > 0:
                        data[i-1][j-1] += 1
                    if j < len(data[i])-1:
                        data[i-1][j+1] += 1
                if i < len(data[j])-1:
                    data[i+1][j] += 1
                    if j < len(data[i])-1:
                        data[i+1][j+1] += 1
                    if j > 0:
                        data[i+1][j-1] += 1
                if j > 0:
                    data[i][j-1] += 1
                if j < len(data[i])-1:
                    data[i][j+1] += 1
        # reset the flashes
        data = np.where(data > 9, 0, data)
        index += 1
        if new_new_flashes == len(data)**2:
            break
    return index+1


if __name__ == "__main__":
    data = np.array([int(e) for f in open('day11.txt').readlines() for e in f.strip()]).reshape(10,10)
    test = np.array([int(e) for f in """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n") for e in f]).reshape(10,10)
    assert sol1(test, 10) == 204
    # wrong number?? assert sol1(test, 100) == 1656
    print(sol1(data, 100))
    assert sol2(test) == 195
    print(sol2(data))