with open('data.txt', 'r') as puzzle:
    modules = [int(e) for e in puzzle.read().split('\n') if e]

def fuel(mass: int) -> int:
    return max(mass // 3 - 2, 0)

def fuel_rec(module: int, acc: int = 0) -> int:
    f = fuel(module)
    if f:
        return fuel_rec(f, acc+f)
    else:
        return acc


print("part 1: ", sum([fuel(e) for e in modules]))
print("part 2: ", sum([fuel_rec(e) for e in modules]))
