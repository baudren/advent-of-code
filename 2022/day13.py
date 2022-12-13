from rich import print
from utils import load, file_to_lines, file_to_ints
from functools import cmp_to_key


def is_right_order(pair):
    left, right = pair.splitlines()
    left = eval(left)
    right = eval(right)
    value = compare_rec(left, right)
    return value == 1


# return -1 if wrong order, 0 if no answer, 1 if right order
def compare_rec(a, b):
    if type(a) == type(b):
        if (type(a) == type(1)):
            if a == b:
                return 0
            elif a < b:
                return 1
            else:
                return -1
        else:
            # both are lists
            for i in range(len(a)):
                if len(b) < i+1:
                    return -1
                else:
                    value = compare_rec(a[i], b[i])
                    if value != 0:
                        return value
            # ran out of values to compare
            # if a is empty and b is not, right order, if both are empty, wrong order
            if len(a) == 0 and len(b) != 0:
                return 1
            elif len(a) == 0 and len(b) == 0:
                return -1
            elif len(a) < len(b):
                return 1
            else:
                return 0
    elif type(a) == type(1):
        new_a = [a]
        return compare_rec(new_a, b)
    else:
        new_b = [b]
        return compare_rec(a, new_b)


def sol1(a):
    pairs = a.split("\n\n")
    total = 0
    for index, pair in enumerate(pairs):
        if is_right_order(pair):
            total += index+1
    return total


def sol2(a):
    pairs = [eval(e) for e in a.splitlines() if e]
    pairs.extend([[[2]], [[6]]])
    sorted_pairs = sorted(pairs, key=cmp_to_key(compare_rec), reverse=True)
    return (sorted_pairs.index([[2]])+1)*(sorted_pairs.index([[6]])+1)


test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
asserts_sol1 = {
        test: 13
        }

asserts_sol2 = {
        test: 140
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
