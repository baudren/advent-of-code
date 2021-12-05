import re

def sol1(data):
    floor = {}
    result = 0
    for line in data:
        x1, y1, x2, y2 = parse(line)
        if x1 == x2 or y1 == y2:
            if y1 != y2:
                for y in range(y1, y2+1 if y2 > y1 else y2-1, 1 if y2 > y1 else -1):
                    if (x1, y) in floor:
                        floor[(x1, y)] += 1
                        if floor[(x1, y)] == 2:
                            result += 1
                    else:
                        floor[(x1, y)] = 1
            else:
                for x in range(x1, x2+1 if x2 > x1 else x2-1, 1 if x2 > x1 else -1):
                    if (x, y1) in floor:
                        floor[(x, y1)] += 1
                        if floor[(x, y1)] == 2:
                            result += 1
                    else:
                        floor[(x, y1)] = 1
    return result


def sol2(data):
    floor = {}
    result = 0
    for line in data:
        x1, y1, x2, y2 = parse(line)
        if y1 != y2 and x1 == x2:
            for y in range(y1, y2+1 if y2 > y1 else y2-1, 1 if y2>y1 else -1):
                if (x1, y) in floor:
                    floor[(x1, y)] += 1
                    if floor[(x1, y)] == 2:
                        result += 1
                else:
                    floor[(x1, y)] = 1
        elif y1 == y2 and x1 != x2:
            for x in range(x1, x2+1 if x2 > x1 else x2-1, 1 if x2 > x1 else -1):
                if (x, y1) in floor:
                    floor[(x, y1)] += 1
                    if floor[(x, y1)] == 2:
                        result += 1
                else:
                    floor[(x, y1)] = 1
        else:
            # diagonal
            for x, y in zip(range(x1, x2+1 if x2 > x1 else x2-1, 1 if x2 > x1 else -1), range(y1, y2+1 if y2 > y1 else y2-1, 1 if y2>y1 else -1)):
                if (x, y) in floor:
                    floor[(x, y)] += 1
                    if floor[(x, y)] == 2:
                        result += 1
                else:
                    floor[(x, y)] = 1
    return result

def parse(line):
    start, end = line.split(" -> ")
    x1, y1 = [int(e) for e in start.split(",")]
    x2, y2 = [int(e) for e in end.split(",")]
    return x1, y1, x2, y2

if __name__ == "__main__":
    data = [e.strip() for e in open('day05.txt', 'r').readlines()]
    test = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split("\n")
    assert sol1(test) == 5
    print(sol1(data))
    assert sol2(test) == 12
    print(sol2(data))
