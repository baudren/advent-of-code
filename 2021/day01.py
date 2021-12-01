def sol1(data):
    sol = 0
    cur = data[0]
    for e in data[1:]:
        if e > cur:
            sol += 1
        cur = e
    return sol

def sol2(data):
    sol = 0
    cur = sum(data[0:3])
    tmp = 0
    for i in range(1, len(data)-2):
        s = sum(data[i:i+3])
        if s > cur:
            sol += 1
        cur = s
    return sol



if __name__ == "__main__":
    data = [int(e.strip()) for e in open('day01.txt', 'r').readlines()]
    print(sol1(data))
    print(sol2(data))
