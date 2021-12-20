import numpy as np

def sol1(algo, image):
    back = '0'
    image, back = iterate(algo, image, back)
    image, back = iterate(algo, image, back)
    return np.count_nonzero(image == True)

    
def sol2(algo, image):
    back = '0'
    for i in range(50):
        image, back = iterate(algo, image, back)
    return np.count_nonzero(image == True)

def iterate(algo, image, back):
    new_image = np.zeros((image.shape[0]+2, image.shape[1]+2), dtype=bool)
    for x in range(new_image.shape[0]):
        for y in range(new_image.shape[1]):
            bin_number = ''
            for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    if i-1 >= 0 and i-1 < image.shape[0]:
                        if j-1 >= 0 and j-1 < image.shape[1]:
                            bin_number += '1' if image[i-1][j-1] else '0'
                        else:
                            bin_number += back
                    else:
                        bin_number += back
            n = int(bin_number, 2)
            new_image[x][y] = algo[n] == '#'
    if algo[0] == '#':
        if back == '0':
            back = '1'
        else:
            back = '0'
    return new_image, back

def parse(raw):
    algo = raw[0]
    image = np.array([e == '#' for f in raw[2:] for e in f.strip()], dtype=bool).reshape(len(raw[2:]),len(raw[2:]))
    return algo, image

if __name__ == "__main__":
    data = [e.strip() for e in open('day20.txt', 'r').readlines()]
    test = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".split("\n")
    assert sol1(*parse(test)) == 35
    print(sol1(*parse(data)))
    assert sol2(*parse(test)) == 3351
    print(sol2(*parse(data)))
