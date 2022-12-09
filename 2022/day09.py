from rich import print
from utils import load, file_to_lines, file_to_ints

moves = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}

def sol1(a):
    data = file_to_lines(a)
    h = (0, 0)
    t = (0, 0)
    visited = set([t])
    for move in data:
        direction, dist = move.split()
        dist = int(dist)
        for i in range(dist):
            h = (h[0]+moves[direction][0], h[1]+moves[direction][1])
            if t[0] == h[0]:
                if t[1]-h[1] > 1:
                    t = (t[0], t[1]-1)
                if h[1]-t[1] > 1:
                    t = (t[0], t[1]+1)
            if t[1] == h[1]:
                if t[0]-h[0] > 1:
                    t = (t[0]-1,t[1])
                if h[0]-t[0] > 1:
                    t = (t[0]+1, t[1])
            if t[0] != h[0] and t[1] != h[1]:
                if t[0]-h[0] > 1:
                    t = (t[0]-1, t[1])
                    if t[1]-h[1] > 0:
                        t = (t[0], t[1]-1)
                    elif h[1]-t[1] > 0:
                        t = (t[0], t[1]+1)
                elif h[0]-t[0] > 1:
                    t = (t[0]+1, t[1])
                    if t[1]-h[1] > 0:
                        t = (t[0], t[1]-1)
                    elif h[1]-t[1] > 0:
                        t = (t[0], t[1]+1)
                if t[1]-h[1] > 1:
                    t = (t[0], t[1]-1)
                    if t[0]-h[0] > 0:
                        t = (t[0]-1, t[1])
                    elif h[0]-t[0] > 0:
                        t = (t[0]+1, t[1])
                elif h[1]-t[1] > 1:
                    t = (t[0], t[1]+1)
                    if t[0]-h[0] > 0:
                        t = (t[0]-1, t[1])
                    elif h[0]-t[0] > 0:
                        t = (t[0]+1, t[1])
            visited.add(t)
    return len(visited)

def sol2(a):
    data = file_to_lines(a)
    snake = [(0, 0) for _ in range(10)]
    visited = set([snake[-1]])
    for move in data:
        direction, dist = move.split()
        dist = int(dist)
        for i in range(dist):
            snake[0] = (snake[0][0]+moves[direction][0], snake[0][1]+moves[direction][1])
            for i in range(1, 10):
                h = snake[i-1]
                t = snake[i]
                if t[0] == h[0]:
                    if t[1]-h[1] > 1:
                        t = (t[0], t[1]-1)
                    if h[1]-t[1] > 1:
                        t = (t[0], t[1]+1)
                if t[1] == h[1]:
                    if t[0]-h[0] > 1:
                        t = (t[0]-1,t[1])
                    if h[0]-t[0] > 1:
                        t = (t[0]+1, t[1])
                if t[0] != h[0] and t[1] != h[1]:
                    if t[0]-h[0] > 1:
                        t = (t[0]-1, t[1])
                        if t[1]-h[1] > 0:
                            t = (t[0], t[1]-1)
                        elif h[1]-t[1] > 0:
                            t = (t[0], t[1]+1)
                    elif h[0]-t[0] > 1:
                        t = (t[0]+1, t[1])
                        if t[1]-h[1] > 0:
                            t = (t[0], t[1]-1)
                        elif h[1]-t[1] > 0:
                            t = (t[0], t[1]+1)
                    if t[1]-h[1] > 1:
                        t = (t[0], t[1]-1)
                        if t[0]-h[0] > 0:
                            t = (t[0]-1, t[1])
                        elif h[0]-t[0] > 0:
                            t = (t[0]+1, t[1])
                    elif h[1]-t[1] > 1:
                        t = (t[0], t[1]+1)
                        if t[0]-h[0] > 0:
                            t = (t[0]-1, t[1])
                        elif h[0]-t[0] > 0:
                            t = (t[0]+1, t[1])
                snake[i] = t
            visited.add(t) ## the real tail
    return len(visited)


asserts_sol1 = {
        """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""": 13
        }

asserts_sol2 = {
        """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""": 36
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
