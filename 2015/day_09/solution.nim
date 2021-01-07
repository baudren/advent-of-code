import strutils, sequtils, tables, re, sugar, algorithm

let test = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""".splitLines

let data = readFile("data.txt").splitLines
let line_re = re"([A-Za-z]+) to ([A-Za-z]+) = (\d+)"

proc compute(towns: seq[string], distances: Table[string, Table[string, int]]): int =
    for index, town in towns[0..^2]:
        result += distances[town][towns[index+1]]

proc sol1(data: seq[string]): int =
    var distances = initTable[string, Table[string, int]]()
    for line in data:
        if line =~ line_re:
            if matches[0] notin distances:
                distances[matches[0]] = initTable[string, int]()
            distances[matches[0]][matches[1]] = matches[2].parseInt
            if matches[1] notin distances:
                distances[matches[1]] = initTable[string, int]()
            distances[matches[1]][matches[0]] = matches[2].parseInt
    var towns = toSeq(distances.keys).sorted
    result = compute(towns, distances)
    while towns.nextPermutation:
        let value = compute(towns, distances)
        if value < result:
            result = value


proc sol2(data: seq[string]): int =
    var distances = initTable[string, Table[string, int]]()
    for line in data:
        if line =~ line_re:
            if matches[0] notin distances:
                distances[matches[0]] = initTable[string, int]()
            distances[matches[0]][matches[1]] = matches[2].parseInt
            if matches[1] notin distances:
                distances[matches[1]] = initTable[string, int]()
            distances[matches[1]][matches[0]] = matches[2].parseInt
    var towns = toSeq(distances.keys).sorted
    result = compute(towns, distances)
    while towns.nextPermutation:
        let value = compute(towns, distances)
        if value > result:
            result = value

assert test.sol1 == 605
dump data.sol1
assert test.sol2 == 982
dump data.sol2