import strutils
import sugar
import tables
import sequtils
import sets
import algorithm


var test = """16
10
15
5
1
11
7
19
6
12
4""".split("\n").map(parseInt)
var test2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".split("\n").map(parseInt)
test.sort()
test2.sort()
var data = readFile("data.txt").split("\n").map(parseInt)
data.sort()

proc sol1(data: seq[int]): int =
    var 
        current_joltage = 0
        joltage_differences: Table[int, int] = {1: 0, 2: 0, 3: 0}.toTable()
    for adaptor in data:
        joltage_differences[adaptor-current_joltage] += 1
        current_joltage = adaptor
    dump joltage_differences
    dump len(data)
    return joltage_differences[1]*(joltage_differences[3]+1)

proc sol2(data: seq[int]): int =
    var 
        current_joltage = 0
        skipped_index = 0
    result = 1
    dump data
    for index, adaptor in data:
        dump adaptor
        dump current_joltage
        echo index, " ", skipped_index
        if index < skipped_index:
            current_joltage = adaptor
            echo index , "  skipping"
            continue
        if index < data.len() - 1 and adaptor - current_joltage == 1:
            var add = 1
            while (index + add < data.len()) and (data[index+add]-data[index+add-1] == 1):
                add += 1
            add -= 1
            if add > 0:
                echo index, " ", adaptor, " ", add
                skipped_index = index+add
                case add:
                    of 1:
                        result *= 2
                    of 2:
                        result *= 4
                    of 3:
                        result *= 7
                    of 4:
                        result *= 13
                    else:
                        echo "oups ", add
        current_joltage = adaptor
    dump result
    

assert sol1(test) == 35
assert sol1(test2) == 220
dump sol1(data)

assert sol2(test) == 8
assert sol2(test2) == 19208
dump sol2(data)