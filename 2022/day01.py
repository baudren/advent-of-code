from rich import print
from utils import load_string, load_lines


def sol1(a):
    return 1


def sol2(a):
    return 0


asserts_sol1 = {
        "3": 1
        }

asserts_sol2 = {
        "3": 3
        }

if __name__ == "__main__":
    data = load_lines()
    print(data)
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
