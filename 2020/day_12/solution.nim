import strutils
import sugar
import sequtils

# turn right is (x, y) -> (-y, x)
# turn left is (x, y) -> (y, -x)

type 
    Instruction = object
        order: char
        value: int
    Pos = object
        x: int
        y: int
    Dir = object
        x: int
        y: int
    Boat = object
        waypoint: Pos
        pos: Pos
        dir: Dir

proc toInstruction(str: string): Instruction =
    let order = str[0]
    let value = parseInt(str[1..^1])
    return Instruction(order: order, value: value)

proc moveDir(pos: Pos, dir: Dir, value: int): Pos =
    return Pos(x: pos.x + dir.x * value, y: pos.y + dir.y * value)

proc advance_to_waypoint(boat: var Boat, value: int): void =
    boat.pos = Pos(x: boat.pos.x + boat.waypoint.x*value, y: boat.pos.y + boat.waypoint.y*value)

proc move(boat: var Boat, instr: Instruction): void =
    case instr.order:
        of 'R':
            var (x, y) = (boat.dir.x, boat.dir.y)
            for i in 0..<(instr.value div 90):
                (x, y) = (-y, x)
            boat.dir = Dir(x: x, y: y)
        of 'L':
            var (x, y) = (boat.dir.x, boat.dir.y)
            for i in 0..<(instr.value div 90):
                (x, y) = (y, -x)
            boat.dir = Dir(x: x, y: y)
        of 'F':
            boat.pos = boat.pos.moveDir(boat.dir, instr.value)
        of 'N':
            boat.pos = boat.pos.moveDir(Dir(x:1, y:0), instr.value)
        of 'S':
            boat.pos = boat.pos.moveDir(Dir(x: -1, y:0), instr.value)
        of 'E':
            boat.pos = boat.pos.moveDir(Dir(x:0, y:1), instr.value)
        of 'W':
            boat.pos = boat.pos.moveDir(Dir(x:0, y: -1), instr.value)
        else:
            echo "ooups"


proc move2(boat: var Boat, instr: Instruction): void =
    case instr.order:
        of 'R':
            var (x, y) = (boat.waypoint.x, boat.waypoint.y)
            for i in 0..<(instr.value div 90):
                (x, y) = (-y, x)
            boat.waypoint = Pos(x: x, y: y)
        of 'L':
            var (x, y) = (boat.waypoint.x, boat.waypoint.y)
            for i in 0..<(instr.value div 90):
                (x, y) = (y, -x)
            boat.waypoint = Pos(x: x, y: y)
        of 'F':
            boat.advance_to_waypoint(instr.value)
        of 'N':
            boat.waypoint = Pos(x: boat.waypoint.x + instr.value, y: boat.waypoint.y)
        of 'S':
            boat.waypoint = Pos(x: boat.waypoint.x - instr.value, y: boat.waypoint.y)
        of 'E':
            boat.waypoint = Pos(x: boat.waypoint.x, y: boat.waypoint.y + instr.value)
        of 'W':
            boat.waypoint = Pos(x: boat.waypoint.x, y: boat.waypoint.y - instr.value)
        else:
            echo "ooups"


proc manhattan(pos: Pos): int =
    abs(pos.x) + abs(pos.y)

let test = """F10
N3
F7
L270
F11""".split("\n").map(toInstruction)
var data = readFile("data.txt").splitLines().map(toInstruction)

dump test

#manhattan from start
proc sol1(instructions: seq[Instruction]): int =
    var boat = Boat(pos: Pos(x: 0, y: 0), dir: Dir(x:0, y:1))
    for instr in instructions:
        boat.move(instr)
    boat.pos.manhattan

assert sol1(test) == 25
dump sol1(data)

proc sol2(instructions: seq[Instruction]): int =
    var boat = Boat(pos: Pos(x: 0, y: 0), dir: Dir(x: 0, y: 0), waypoint: Pos(x: 1, y: 10))
    for instr in instructions:
        boat.move2(instr)
    boat.pos.manhattan

assert sol2(test) == 286
dump sol2(data)