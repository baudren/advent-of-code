import strutils
import sequtils
import sugar

let test = "forward 5,down 5,forward 8,up 3,down 8,forward 2".split(",")
let commands = readFile("day02.txt").splitLines()

proc sol1(commands: seq[string]): int =
    var (d, h) = (0, 0)
    for command in commands:
        let action = command.split(" ")[0]
        let value = parseInt(command.split(" ")[1])
        if action == "forward":
            h += value
        elif action == "down":
            d += value
        elif action == "up":
            d -= value
    result = d*h
    

proc sol2(commands: seq[string]): int =
    var (a, d, h) = (0, 0, 0)
    for command in commands:
        let action = command.split(" ")[0]
        let value = parseInt(command.split(" ")[1])
        if action == "forward":
            h += value
            d += a*value
        elif action == "down":
            a += value
        elif action == "up":
            a -= value
    result = d*h


assert sol1(test) == 150
assert sol2(test) == 900
dump sol1(commands)
dump sol2(commands)