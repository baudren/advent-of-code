import strutils
import sugar
import sequtils
import tables

let test = "0,3,6"
var data = "20,0,1,11,6,3"

proc sol1(data: string, stop: int): int =
    var values = newTable[int, seq[int]]()
    for i, v in data.split(",").map(parseInt):
        values[v] = @[i]
    dump values
    var previous = data.split(",").map(parseInt)[^1]
    for index in len(values)..<stop:
        if index mod 100_000 == 0:
            echo index#, " ", values
        var current: int
        if len(values[previous]) == 1:
            current = 0
        else:
            current = values[previous][^1] - values[previous][^2]
        if values.hasKeyOrPut(current, @[index]):
            values[current].add(index)
        previous = current
        #echo index, " ", values
    return previous

proc sol2(data: string, stop: int, length: int): int =
    var values = initTable[int, Table[int, seq[int]]]()
    let splits = (0..stop).mapIt(it*length)
    for split in splits:
        values[split div length] = initTable[int, seq[int]]()
    for i, v in data.split(",").map(parseInt):
        values[0][v] = @[i]

    var previous = data.split(",").map(parseInt)[^1]
    for index in len(data.split(","))..<stop*length:
        var current: int
        var k: int
        for i, split in splits:
            if previous < split:
                k = i-1
                break
        #echo previous, " ", k
        if len(values[k][previous]) == 1:
            current = 0
        else:
            current = values[k][previous][^1] - values[k][previous][^2]
        for i, split in splits:
            if current < split:
                k = i-1
                break
        if values[k].hasKeyOrPut(current, @[index]):
            values[k][current].add(index)
        previous = current
    return previous

assert sol1("0,3,6", 2020) == 436
dump sol1(data, 2020)
#assert sol1("0,3,6", 30000000) == 175594
#dump sol1(data, 1_000_000)
dump sol2(data, 300, 100_000)