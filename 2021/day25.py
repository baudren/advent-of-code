import numpy as np

def sol1(data):
    steps = 0
    moved = True
    while moved:
        new_data = np.copy(data)
        # East moves
        to_move = []
        for i, j in zip(*np.where(data == ">")):
            if data[i, (j+1)%data.shape[1]] == '.':
                to_move.append((i, j))
        for i, j in to_move:
            data[i, j] = '.'
            data[i,(j+1)%data.shape[1]] = ">"
        moved = len(to_move) != 0
        # South moves
        to_move = []
        for i, j in zip(*np.where(data == "v")):
            if data[(i+1)%data.shape[0], j] == '.':
                to_move.append((i, j))
        for i, j in to_move:
            data[i, j] = '.'
            data[(i+1)%data.shape[0], j] = "v"
        steps += 1
        if not moved:
            moved = len(to_move) != 0
    return steps

if __name__ == "__main__":
    data = np.array([f for e in open("day25.txt", "r").readlines() for f in e.strip()]).reshape((137,139))
    test = np.array([ f for e in """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".split("\n") for f in e]).reshape((9,10))
    assert sol1(test) == 58
    print(sol1(data))