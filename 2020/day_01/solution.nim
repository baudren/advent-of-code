import strutils
import sequtils
import sugar

let test = "1721,979,366,299,675,1456".split(",").mapIt(parseInt(it))
let integers = readFile("data.txt").splitLines().mapIt(parseInt(it))

proc sol1(integers: seq[int]): int =
    for i in integers:
        if integers.contains(2020-i):
            return i*(2020-i)

proc sol2(integers: seq[int]): int =
    for i in 0..<integers.len():
        for j in i..<integers.len():
            if integers[i] + integers[j] < 2020:
                let dk = 2020 - integers[i] - integers[j]
                if integers.contains(dk):
                    return dk * integers[i] * integers[j]

assert sol1(test) == 514579
assert sol2(test) == 241861950
dump sol1(integers)
dump sol2(integers)