from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        start, end = line[:len(line)//2],line[len(line)//2:]
        double = [e for e in start if e in end][0]
        if double == double.upper():
            value = ord(double)-ord('A')+27
        else:
            value = ord(double)-ord('a')+1
        total += value
    return total


def sol2(a):
    data = file_to_lines(a)
    total = 0
    all_ = []
    for line in data:
        if len(all_) <= 3:
            all_.append(line)
        if len(all_) == 3:
            double = [e for e in all_[0] if e in all_[1] and e in all_[2]][0]
            if double == double.upper():
                value = ord(double)-ord('A')+27
            else:
                value = ord(double)-ord('a')+1
            total += value
            all_.clear()
    return total


asserts_sol1 = {
        """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""": 157
        }

asserts_sol2 = {
        """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""": 70
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
