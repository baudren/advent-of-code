from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    data = file_to_lines(a)
    cur = 0
    max_ = 0
    for e in data:
        if e.strip():
            cur += int(e.strip())
        else:
            if cur > max_:
                max_ = cur
            cur = 0
    return max_


def sol2(a):
    data = file_to_lines(a)
    foods = []
    cur = 0
    for e in data:
        if e.strip():
            cur += int(e.strip())
        else:
            foods.append(cur)
            cur = 0
    if cur != 0:
        foods.append(cur)
    foods.sort()
    return sum(foods[-3:])


asserts_sol1 = {
        """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""": 24000
        }

asserts_sol2 = {
        """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""": 45000
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
