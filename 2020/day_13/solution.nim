import strutils
import sugar
import sequtils
import tables
import math

let test = """939
7,13,x,x,59,x,31,19""".split("\n")
var data = readFile("data.txt").splitLines()

proc sol1(data: seq[string]): int =
    let timestamp = data[0].parseInt
    let buses = data[1].split(",").filterIt(it != "x").map(parseInt)
    var earliest: seq[int] = @[]
    for bus in buses:
        earliest.add(bus * (timestamp div bus + 1))
    dump earliest
    dump earliest.minIndex
    (earliest[earliest.minIndex] - timestamp) * buses[earliest.minIndex]


assert sol1(test) == 295
dump sol1(data)

proc sol2(data: string): int64 =
    var delays: seq[(int64, int)] = @[]
    let raw_buses: seq[string] = data.split(",")
    let first: int64 = raw_buses[0].parseInt
    var second: int = 0
    for i, bus in raw_buses:
        if bus != "x" and bus.parseInt != first:
            delays.add((bus.parseBiggestInt, i))
            if second == 0:
                second = bus.parseInt
    var curr_fit = 0
    var fit = 0
    var locked: seq[int] = @[]
    #dump second
    var count = 1
    #result = 1_000_000_000_000*29
    var incr = first
    dump delays
    while true:
        # if count mod 10_000_000 == 0:
        #     echo result div 29, " -> ", result
        count += 1
        #dump result
        result += incr
        dump result
        fit = 0
        var to_multiply: seq[int64] = @[]
        for i, (bus, delay) in delays:
            #echo i, " ", bus
            if delay <= bus:
                if bus*(result div bus + 1) - result == delay:
                    fit += 1
                    echo "pin ", i+1, " is fitting"
                    if i notin locked and fit > curr_fit:
                        curr_fit += 1
                        locked.add(i)
                        to_multiply.add(bus)
                        echo "locking pin ", i+1, " incr: ", bus
            else:
                if delay mod 2 == abs((result-bus) mod 2):
                    fit += 1
                    echo "pin ", i+1, " is fitting"
                    if i notin locked and fit > curr_fit:
                        locked.add(i)
                        curr_fit += 1
                        to_multiply.add(bus)
                        echo "locking pin ", i+1, " incr: ", bus
        if to_multiply != @[]:
            echo "was ", incr
            if len(to_multiply) > 1:
                for i in 0..<len(to_multiply)-1:
                    if to_multiply[^(1+i)] >= to_multiply[^(1+i+1)]:
                        echo "here"
                        incr *= to_multiply[^(1+i)]
                    else:
                        echo "there"
                        incr *= foldl(to_multiply, a*b)
            else:
                incr *= to_multiply[0]
        dump fit
        if fit == len(delays):
            break

proc sol3(data: string): int64 =
    var delays: seq[(int, int)] = @[]
    let raw_buses: seq[string] = data.split(",")
    for i, bus in raw_buses:
        if bus != "x":
            let bus_int = bus.parseInt
            delays.add((bus_int, i mod bus_int))
    let n = foldl(delays.mapIt(it[0]), a*b)
    for i, (bus, delay) in delays:
        let n_hat = foldl(delays.mapIt(it[0]).filterIt(it != bus), a*b)
        var j = 1
        while true:
            if j*n_hat mod bus == 1:
                break
            else:
                j += 1
        result += -delay*j*n_hat
    return result mod n + n

#assert sol3("5,2") == 5
#assert sol3("5,x,2") == 0
assert sol3("17,x,13,19") == 3417
assert sol3("67,7,59,61") == 754018
dump sol3(data[1])