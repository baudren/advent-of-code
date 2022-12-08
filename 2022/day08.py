from rich import print
from utils import load, file_to_lines, file_to_ints
import numpy as np


def sol1(a):
    size = len(file_to_lines(a)[0])
    data = np.array([[int(j) for j in e] for e in file_to_lines(a)])
    visible = set()
    total = 0
    # exterior trees
    total += 2*size + 2*(size-2)
    # Interior trees
    # treat rows for left/right
    for i in range(1,size-1):
        # for each height from left to right
        for h in range(data[i][0], 10):
            # advance from left to right, if we encounter a value higher than the height, we add it
            for k in range(1, size-1):
                if data[i][k] > h:
                    visible.add((i,k))
                    break
        for h in range(data[i][size-1], 10):
            for k in range(size-2, 0, -1):
                if data[i][k] > h:
                    visible.add((i, k))
                    break
    # columns
    for j in range(1, size-1):
        for h in range(data[0][j], 10):
            for i in range(1, size-1):
                if data[i][j] > h:
                    visible.add((i,j))
                    break
        for h in range(data[size-1][j], 10):
            for i in range(size-2, 0, -1):
                if data[i][j] > h:
                    visible.add((i,j))
                    break
    return total+len(visible)


def sol2(a):
    size = len(file_to_lines(a)[0])
    data = np.array([[int(j) for j in e] for e in file_to_lines(a)])
    scores = []

    for i in range(1,size-1):
        for j in range(1,size-1):
            height = data[i][j]
            # to left
            up = 0
            for k in range(i-1,-1,-1):
                up += 1
                if data[k][j] >= height:
                    break
            down = 0
            for k in range(i+1,size):
                down += 1
                if data[k][j] >= height:
                    break
            left = 0
            for k in range(j-1,-1,-1):
                left += 1
                if data[i][k] >= height:
                    break
            right = 0
            for k in range(j+1, size):
                right += 1
                if data[i][k] >= height:
                    break
            score = left*right*up*down
            scores.append(left*right*up*down)
    return max(scores)


asserts_sol1 = {
        """30373
25512
65332
33549
35390""": 21
        }

asserts_sol2 = {
        """30373
25512
65332
33549
35390""": 8
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
