def sol1(dots, folds):
    axis, value = folds[0][0], int(folds[0][1])
    new_dots = {}
    for x, y in dots:
        if axis == 'x':
            if x > value:
                new_dots[(x-(x-value)*2, y)] = True
            else:
                new_dots[(x, y)] = True
        else:
            if y > value:
                new_dots[(x, y-(y-value)*2)] = True
            else:
                new_dots[(x, y)] = True
    return len(new_dots)

def visualize(dots, y_size, x_size):
    for y in range(y_size):
        print(''.join(['#' if (x,y) in dots else '.' for x in range(x_size)]))

def sol2(dots, folds):
    for fold in folds:
        axis, value = fold[0], int(fold[1])
        new_dots = {}
        for x, y in dots:
            if axis == 'x':
                if x > value:
                    new_dots[(x-(x-value)*2, y)] = True
                else:
                    new_dots[(x, y)] = True
            else:
                if y > value:
                    new_dots[(x, y-(y-value)*2)] = True
                else:
                    new_dots[(x, y)] = True
        dots = new_dots
    visualize(new_dots, 6, 40)

def parse(raw):
    dots = {}
    folds = []
    for line in raw:
        if ',' in line:
            dots[tuple(int(e) for e in line.split(','))] = True
        elif '=' in line:
            folds.append(line.split(" ")[2].split("="))
    return dots, folds

if __name__ == "__main__":
    data = [e.strip() for e in open('day13.txt', 'r').readlines()]
    test = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".split("\n")
    assert sol1(*parse(test)) == 17
    print(sol1(*parse(data)))
    sol2(*parse(data))
