import strutils
import sequtils
import sugar

let test1 = "199,200,208,210,200,207,240,269,260,263".split(",").mapIt(parseInt(it))
let integers = readFile("day01.txt").splitLines().mapIt(parseInt(it))

proc sol1(integers: seq[int]): int =
    var cur: int = integers[0]
    for i in 1..<integers.len():
        if integers[i] > cur:
            result += 1
        cur = integers[i]

proc sol2(integers: seq[int]): int =
    var cur: int = foldl(integers[0..2], a+b)
    var s: int = 0
    for i in 1..<integers.len()-2:
        s = foldl(integers[i..i+2], a+b)
        if s > cur:
            result += 1
        cur = s


assert sol1(test1) == 7
assert sol2(test1) == 5
dump sol1(integers)
dump sol2(integers)