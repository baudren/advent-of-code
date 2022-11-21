class Program:

    def __init__(self, data):
        self.steps = []
        cur = []
        for line in data:
            if line[0] == "inp" and cur:
                self.steps.append(cur)
                cur = [line]
            else:
                cur.append(line)
        self.steps.append(cur)

    # Find the target z for a given pos, starting by the end
    def execute(self, pos, target):
        pass

def sol(data):
    program = Program(data)
    # First find the target z for each pos, starting by the end
    target = [[(0, "0")]]
    for pos in range(0, 14):
        possibilities = []
        for w in range(9, 0, -1):
            for value in range(100000):
                #print(w, value)
                vars = {"x": 0, "y":0, "z":value, "w":w}
                for line in program.steps[13-pos]:
                    command = line[0]
                    if command == 'add':
                        try:
                            vars[line[1]] += int(line[2])
                        except:
                            vars[line[1]] += vars[line[2]]
                    elif command == 'mul':
                        try:
                            vars[line[1]] *= int(line[2])
                        except:
                            vars[line[1]] *= vars[line[2]]
                    elif command == 'div':
                        try:
                            vars[line[1]] //= int(line[2])
                        except:
                            vars[line[1]] //= vars[line[2]]
                    elif command == 'mod':
                        try:
                            vars[line[1]] %= int(line[2])
                        except:
                            vars[line[1]] %= vars[line[2]]
                    elif command == 'eql':
                        try:
                            if vars[line[1]] == vars[line[2]]:
                                vars[line[1]] = 1
                            else:
                                vars[line[1]] = 0
                        except:
                            if vars[line[1]] == int(line[2]):
                                vars[line[1]] = 1
                            else:
                                vars[line[1]] = 0
                    #exit()
                to_delete = None
                for i, poss in enumerate(target):
                    if vars["z"] == poss[-1][0]:
                        new_ = list(poss)
                        new_.append((value, str(w)))
                        possibilities.append(new_)
                        to_delete = i
        if not possibilities:
            print(f"{pos} woopsie")
            exit()
        target = possibilities
    max_ = int("1"*14)
    min_ = int("9"*14)
    for possibility in target:
        n = []
        for step in possibility[1:]:
            n.append(step[1])
        n = int("".join(n[::-1]))
        if n > max_:
            max_ = n
        if n < min_:
            min_ = n
    return max_, min_

def sol2(data):
    program = Program(data)
    # First find the target z for each pos, starting by the end
    target = [[(0, "0")]]
    for pos in range(0, 14):
        print(pos)
        print(len(target))
        possibilities = []
        for w in range(1, 10):
            for value in range(100000):
                vars = {"x": 0, "y":0, "z":value, "w":w}
                for line in program.steps[13-pos]:
                    command = line[0]
                    if command == 'add':
                        try:
                            vars[line[1]] += int(line[2])
                        except:
                            vars[line[1]] += vars[line[2]]
                    elif command == 'mul':
                        try:
                            vars[line[1]] *= int(line[2])
                        except:
                            vars[line[1]] *= vars[line[2]]
                    elif command == 'div':
                        try:
                            vars[line[1]] //= int(line[2])
                        except:
                            vars[line[1]] //= vars[line[2]]
                    elif command == 'mod':
                        try:
                            vars[line[1]] %= int(line[2])
                        except:
                            vars[line[1]] %= vars[line[2]]
                    elif command == 'eql':
                        try:
                            if vars[line[1]] == vars[line[2]]:
                                vars[line[1]] = 1
                            else:
                                vars[line[1]] = 0
                        except:
                            if vars[line[1]] == int(line[2]):
                                vars[line[1]] = 1
                            else:
                                vars[line[1]] = 0
                to_delete = None
                for i, poss in enumerate(target):
                    if vars["z"] == poss[-1][0]:
                        new_ = list(poss)
                        new_.append((value, str(w)))
                        possibilities.append(new_)
                        to_delete = i
                        break
        if not possibilities:
            print(f"{pos} woopsie")
            exit()
        target = possibilities
    max_ = int("1"*14)
    min_ = int("9"*14)
    for possibility in target:
        n = []
        for step in possibility[1:]:
            n.append(step[1])
        n = int("".join(n[::-1]))
        if n > max_:
            max_ = n
        if n < min_:
            min_ = n
    return max_, min_


if __name__ == "__main__":
    program = [e.split() for e in open("day24.txt", 'r').read().splitlines()]
    max_, min_ = sol2(program)
    print(f"max: {max_}")
    print(f"min: {min_}")
