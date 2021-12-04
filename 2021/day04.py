import re

def sol1(numbers, boards):
    called = []
    found = {}
    winner = 0
    for number in numbers:
        called.append(number)
        for i, board in enumerate(boards):
            for j, line in enumerate(board):
                if str(number) in line.split(" "):
                    if not i in found:
                        found[i] = {}
                    if not j in found[i]:
                        found[i][j] = []
                    found[i][j].append(True)
                    if len(found[i][j]) == 5:
                        winner = i
                        break
            else:
                continue
            break
        else:
            continue
        break
    sum_ = 0
    for line in boards[winner]:
        for e in line.split():
            if int(e) not in called:
                sum_ += int(e)
    return called[-1] * sum_


def sol2(numbers, boards):
    called = []
    found = {}
    winners = []
    for number in numbers:
        called.append(number)
        for i, board in enumerate(boards):
            for j, line in enumerate(board):
                for k, num in enumerate(re.split("\s+", line.strip())):
                    if str(number) == num:
                        col = "col"+str(k)
                        if not i in found:
                            found[i] = {}
                        if not j in found[i]:
                            found[i][j] = []
                        if not col in found[i]:
                            found[i][col] = []
                        found[i][j].append(True)
                        found[i][col].append(True)
                        if len(found[i][j]) == 5 or len(found[i][col]) == 5:
                            if not i in winners:
                                winners.append(i)
                            if len(winners) == len(boards):
                                break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            continue
        break
    sum_ = 0
    for line in boards[winners[-1]]:
        for e in line.split():
            if int(e) not in called:
                sum_ += int(e)
    return called[-1] * sum_

def parse(raw):
    numbers = [int(e) for e in raw[0].split(',')]
    raw_boards = [e.split("\n") for e in "\n".join(raw[2:]).split("\n\n")]
    return numbers, raw_boards

if __name__ == "__main__":
    data = [e.strip() for e in open('day04.txt', 'r').readlines()]
    test = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".split("\n")
    assert sol1(*parse(test)) == 4512
    print(sol1(*parse(data)))
    assert sol2(*parse(test)) == 1924
    print(sol2(*parse(data)))
