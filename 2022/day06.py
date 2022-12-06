from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    for i in range(len(a)-4):
        if len(set(a[i:i+4])) == 4:
            break
    return i+4


def sol2(a):
    for i in range(len(a)-14):
        if len(set(a[i:i+14])) == 14:
            break
    return i+14


asserts_sol1 = {
        """mjqjpqmgbljsphdztnvjfqwrcgsmlb""": 7,
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
        "nppdvjthqldpwncqszvftbrmjlhg": 6,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11
        }

asserts_sol2 = {
        """mjqjpqmgbljsphdztnvjfqwrcgsmlb""": 19
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
