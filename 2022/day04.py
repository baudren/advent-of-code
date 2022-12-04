from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        first, second = line.split(",")
        first_r = [int(first.split("-")[0]), int(first.split("-")[1])]
        second_r = [int(second.split("-")[0]), int(second.split("-")[1])]
        if contains(first_r, second_r):
            total += 1
    return total


def contains(a, b):
    if a[0] >= b[0] and a[1] <= b[1]:
        return True
    elif b[0] >= a[0] and b[1] <= a[1]:
        return True
    return False

def sol2(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        first, second = line.split(",")
        first_r = [int(first.split("-")[0]), int(first.split("-")[1])]
        second_r = [int(second.split("-")[0]), int(second.split("-")[1])]
        if overlap(first_r, second_r):
            total += 1
    return total

def overlap(a, b):
    if contains(a, b):
        return True
    elif a[1] == b[0] or b[1] == a[0]:
        return True
    elif a[0] <= b[0] and a[1] >= b[0]:
        return True
    elif b[0] <= a[0] and b[1] >= a[0]:
        return True
    return False


asserts_sol1 = {
        """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""": 2
        }

asserts_sol2 = {
        """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""": 4
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
