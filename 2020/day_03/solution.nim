import strutils
import sugar

let test = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".split("\n")
let data = readFile("data.txt").splitLines()

proc sol1(data: seq[string], right: int, down: int): int =
    for index in 0..<data.len():
        if index mod down == 0:
            if data[index][index*right div down mod data[index].len()] == '#':
                result += 1

proc sol2(data: seq[string]): int =
    return sol1(data, 1, 1)*sol1(data, 3, 1)*sol1(data, 5, 1)*sol1(data, 7, 1)*sol1(data, 1, 2)

assert sol1(test, 1, 1) == 2
assert sol1(test, 3, 1) == 7
assert sol1(test, 5, 1) == 3
assert sol1(test, 7, 1) == 4
assert sol1(test, 1, 2) == 2
dump sol2(test)
assert sol2(test) == 336
dump sol2(data)