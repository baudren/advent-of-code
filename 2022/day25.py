from rich import print
from utils import load, file_to_lines, file_to_ints


custom_int = {
    '0' : 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}

def snafu_to_int(snafu):
    number = 0
    l = len(snafu)
    for i, c in enumerate(snafu):
        number += custom_int[c]*5**(l-i-1)
    return number

def max_p(p):
    number = 0
    for l in range(p+1):
        number += 2*5**(p-l)
    return number


def recurse(rest, p, number, test):
    ident = " "*(4*(p+1))
    debug = False #p > 10 #"1-0---" in number
    if debug: print(f"{ident}{rest=}, {p=}, {number=}")
    if p == -1:
        if snafu_to_int(number) == test:
            return number
        else:
            raise ValueError
    elif rest == 0:
        if debug: print("Rest is 0")
        number += "".join(["0" for _ in range(p+1)])
        if snafu_to_int(number) == test:
            return number
        else:
            raise ValueError
    elif rest > max_p(p):
        raise ValueError
    elif rest < -max_p(p):
        raise ValueError
    if rest == 5**p:
        number += "1" + "".join(["0" for _ in range(p)])
        return number
    elif rest == 2*5**p:
        number += "2" + "".join(["0" for _ in range(p)])
        return number
    elif rest == -5**p:
        number += "-" + "".join(["0" for _ in range(p)])
        return number
    elif rest == -2*5**p:
        number += "=" + "".join(["0" for _ in range(p)])
        return number
    # Try to add the moves in order that make sense
    if rest > 2*5**p:
        moves = ["2", "1", "0", "-", "="]
    elif rest > 5**p:
        moves = ["1", "0", "-", "=", "2"]
    elif rest > 0:
        moves = ["0", "-", "=", "2", "1"]
    elif rest > -5**p:
        moves = ["-", "=", "2", "1", "0"]
    else:
        moves = ["=", "2", "1", "0", "-"]
    for move in moves:
        try:
            return recurse(rest-custom_int[move]*5**p, p-1, number+move, test)
        except:
            pass
    raise ValueError


def int_to_snafu(int_):
    number = ""
    p = 0
    total = 0
    while True:
        total += 2*5**p
        if total >= int_:
            break
        else:
            p += 1
    try:
        return recurse(int_, p, "", int_)
    except:
        return recurse(int_, p+1, "", int_)

def sol1(a):
    data = file_to_lines(a)
    total = 0
    for line in data:
        snafu = snafu_to_int(line)
        total += snafu_to_int(line)
    return int_to_snafu(total)


test = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
asserts_sol1 = {
        test: "2=-1=0"
        }


if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    print(f"Go play Dwarf Fortress now")
