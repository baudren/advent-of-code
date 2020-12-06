import strutils
import sugar
import sets
import tables
import sequtils

let test = """abc

a
b
c

ab
ac

a
a
a
a

b
""".split("\n\n").mapIt(it.replace("\n", ""))
let test2 = """abc

a
b
c

ab
ac

a
a
a
a

b""".split("\n\n").mapIt(it.replace("\n", ","))
let data = readFile("data.txt").split("\n\n").mapIt(it.replace("\n", ""))
let data2 = readFile("data.txt").split("\n\n").mapIt(it.replace("\n", ","))

proc sol1(data: seq[string]): int =
    for group in data:
        result += toHashSet(group).len()

proc sol2(data: seq[string]): int =
    for group in data:
        var answers = initTable[char, int]()
        let length = group.count(",") + 1
        for answer in group.split(","):
            for ch in toHashSet(answer):
                if ch in answers:
                    answers[ch] += 1
                else:
                    answers[ch] = 1
        for key, val in answers:
            if val == length:
                result += 1

assert sol1(test) == 11
dump sol1(data)

assert sol2(test2) == 6
dump sol2(data2)