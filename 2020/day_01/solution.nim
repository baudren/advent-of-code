import strutils
import sequtils
import sugar

let integers = readFile("data.txt").splitLines().mapIt(parseInt(it))

proc sol1(integers: seq[int]): int =
    for i in integers:
        for j in integers:
            if i + j == 2020:
                return i*j

proc sol2(integers: seq[int]): int =
    for i in integers:
        for j in integers:
            for k in integers:
                if i + j + k == 2020:
                    return i*j*k

dump sol1(integers)
dump sol2(integers)