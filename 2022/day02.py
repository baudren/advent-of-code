from rich import print
from utils import load, file_to_lines, file_to_ints

# Value of each shape
score = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

# Outcome if X, Y, Z stands for Rock, Paper, Scissors
result = {
    'A': {
        'X': 3,
        'Y': 6,
        'Z': 0,
    },
    'B': {
        'X': 0,
        'Y': 3,
        'Z': 6,
    },
    'C': {
        'X': 6,
        'Y': 0,
        'Z': 3,
    }
}

# which shape to select if X, Y, Z stands for Lose, Draw, Win
result_2 = {
    'A': {
        'X': 'Z',
        'Y': 'X',
        'Z': 'Y',
    },
    'B': {
        'X': 'X',
        'Y': 'Y',
        'Z': 'Z',
    },
    'C': {
        'X': 'Y',
        'Y': 'Z',
        'Z': 'X',
    }
}

# outcome if X, Y, Z stands for Lose, Draw, Win
outcome = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}


def sol1(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        elf, me = line.split()
        total += score[me]+result[elf][me]
    return total


def sol2(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        elf, me = line.split()
        total += score[result_2[elf][me]] + outcome[me]
    return total


asserts_sol1 = {
        }

asserts_sol2 = {
        }

if __name__ == "__main__":
    data = load()
    for d, expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d, expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
