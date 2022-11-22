from rich import print
from utils import load_string, load_lines
import re


def sol1(a):
    b = get_ints(a)
    total = 0
    for line in b:
        diff = max(line) - min(line)
        total += diff
    return total


def sol2(a):
    b = get_ints(a)
    total = 0
    for line in b:
        for i in range(len(line)):
            for j in range(i+1, len(line)):
                if line[i] >= line[j]:
                    if line[i] // line[j] == line[i]*1.0/line[j]:
                        total += line[i] / line[j]
                        break
                else:
                    if line[j] // line[i] == line[j]*1.0/line[i]:
                        total += line[j] / line[i]
                        break
    return int(total)


asserts_sol1 = {
        """5 1 9 5
7 5 3
2 4 6 8""": 18
        }

asserts_sol2 = {
        """5 9 2 8
9 4 7 3
3 8 6 5""": 9
        }

def get_ints(data):
    return [[int(a) for a in re.split("\s+", t.strip())] for t in data]

if __name__ == "__main__":
    data = load_lines()
    for d,expected in asserts_sol1.items():
        assert sol1(d.split("\n")) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d.split("\n")) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
