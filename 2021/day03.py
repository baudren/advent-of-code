def sol1(data):
    g = {k: '0' for k in range(len(data[0]))}
    e = {k: '1' for k in range(len(data[0]))}
    sol = {k: 0 for k in range(len(data[0]))}
    for item in data:
        for index, bit in enumerate(item):
            sol[index] += int(bit)
    for i, v in sol.items():
        if v > len(data)/2:
            g[i] = '1'
            e[i] = '0'
    return int(''.join(g.values()), 2)*int(''.join(e.values()), 2)


def sol2(data):
    sol = {k: 0 for k in range(len(data[0]))}
    g = {k: '0' for k in range(len(data[0]))}
    for i, v in sol.items():
        if v >= len(data)/2:
            g[i] = '1'
    index = 0
    bag = {item: True for item in data}
    while True:
        new_bag = {}
        sol = {k: 0 for k in range(len(data[0]))}
        for item in bag:
            for i, bit in enumerate(item):
                sol[i] += int(bit)
                if i == index:
                    break
        mfb = '1' if sol[index] >= len(bag)/2 else '0'
        lsb = '0' if mfb == '1' else '1'
        for item in bag:
            if item[index] == mfb:
                new_bag[item] = True
        bag = new_bag
        if len(bag) == 1:
            ogr = list(bag.keys())[0]
            break
        index += 1

    index = 0
    bag = {item: True for item in data}
    while True:
        new_bag = {}
        sol = {k: 0 for k in range(len(data[0]))}
        for item in bag:
            for i, bit in enumerate(item):
                sol[i] += int(bit)
                if i == index:
                    break
        mfb = '0' if sol[index] >= len(bag)/2 else '1'
        for item in bag:
            if item[index] == mfb:
                new_bag[item] = True
        bag = new_bag
        if len(bag) == 1:
            csr = list(bag.keys())[0]
            break
        index += 1
    return int(ogr, 2)*int(csr, 2)
        

if __name__ == "__main__":
    data = [e.strip() for e in open('day03.txt', 'r').readlines()]
    test = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split("\n")
    assert sol1(test) == 198
    print(sol1(data))
    assert sol2(test) == 230
    print(sol2(data))
