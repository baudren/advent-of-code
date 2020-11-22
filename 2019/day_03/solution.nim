# To improve, this is only 3 times as fast as Python...
import strutils
import sequtils
import sugar
import tables

type
    Wire = seq[string]
    Position = tuple[x: int, y: int]

proc `+`(a: Position, b: Position): Position =
    return (a.x + b.x, a.y + b.y)

proc `*`(a: int, b: Position): Position =
    return (a*b.x, a*b.y)

proc `+=`(a: var Position, b: Position): void =
    a = a + b

proc abs(a: Position): int =
    return abs(a.x) + abs(a.y)

let
    data: seq[Wire] = readFile("data.txt").splitLines().mapIt(it.split(","))
    w1: Wire = data[0]
    w2: Wire = data[1]

const
    dirs = {'U': (0, 1), 'R': (1, 0), 'D': (0, -1), 'L': (-1, 0)}.toTable

# output all covered tuples by a wire
proc covered(wire: Wire): Table[Position, int] =
    var covered: Table[Position, int] = initTable[Position, int]()
    var head: Position = (0, 0)
    var current_length = 0
    for elem in wire:
        let 
            dir = elem[0]
            length: int = parseInt(elem[1..^1])
        for i in 1..length:
            discard covered.hasKeyOrPut(head + i*dirs[dir], i+current_length)
        head += length*dirs[dir]
        current_length += length       
    return covered

proc sol(w1: Wire, w2: Wire): (int, int) =
    let
        c1 = covered(w1)
        c2 = covered(w2)
    var intersects: seq[Position] = @[]
    for key in c1.keys:
        if c2.hasKey(key):
            intersects.add(key)
    let
        sol1 = intersects.mapIt(abs(it)).min
        sol2 = intersects.mapIt(c1[it] + c2[it]).min
    return (sol1, sol2)

dump sol(w1, w2)