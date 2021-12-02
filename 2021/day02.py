def sol1(data):
    h, d = 0, 0
    for e in data:
        command, value = e.split(" ")
        value = int(value)
        if command == "forward":
            h += value
        elif command == "down":
            d += value
        elif command == "up":
            d -= value
    return d*h

def sol2(data):
    a, h, d = 0, 0, 0
    for e in data:
        command, value = e.split(" ")
        value = int(value)
        if command == "forward":
            h += value
            d += a*value
        elif command == "down":
            a += value
        elif command == "up":
            a -= value
    return d*h


if __name__ == "__main__":
    data = [e.strip() for e in open('day02.txt', 'r').readlines()]
    test = """forward 5,down 5,forward 8,up 3,down 8,forward 2""".split(",")
    assert sol1(test) == 150
    print(sol1(data))
    assert sol2(test) == 900
    print(sol2(data))
