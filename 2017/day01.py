from rich import print
from utils import load_string, load_lines


def sol1(a):
    total = 0
    previous = int(a[0])
    for i in a[1:]:
        value = int(i)
        if value == previous:
            total += value
        previous = value
    if a[-1] == a[0]:
        total += int(a[0])

    return total


def sol2(a):
    total = 0
    next_index = len(a)//2
    for i in range(len(a)):
        value = int(a[i])
        other = int(a[next_index])
        if value == other:
            total += value
        next_index = (next_index + 1) % len(a)
    return total


asserts_sol1 = {
        "1122": 3,
        "1111": 4,
        "1234": 0,
        "91212129": 9
        }

asserts_sol2 = {
        "1212": 6,
        "1221": 0,
        "123425": 4,
        "123123": 12,
        "12131415": 4
        }

if __name__ == "__main__":
    data = load_string()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
