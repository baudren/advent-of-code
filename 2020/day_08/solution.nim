import strutils
import sugar

let test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".split("\n")

let data = readFile("data.txt").split("\n")

proc parse(data: seq[string]): seq[(string, int)] =
    for line in data:
        result.add((line.split(" ")[0], parseInt(line.split(" ")[1])))

proc sol1(instructions: seq[(string, int)]): (int, bool) =
    var
        acc = 0
        terminates = false
        head = 0
        visited: seq[int] = @[]
    while true:
        if head notin visited:
            if head < len(instructions):
                visited.add(head)
            else:
                terminates = true
                break
        else:
            break
        case instructions[head][0]:
            of "acc":
                acc += instructions[head][1]
                head += 1
            of "jmp":
                head += instructions[head][1]
            else:
                head += 1
    return (acc, terminates)

proc sol2(instructions: seq[(string, int)]): int =
    var modified_instructions = instructions
    for index in 0..instructions.len():
        let
            orig = instructions[index][0]
            replaced = (if orig == "jmp": "noop" elif orig == "noop": "jmp" else: orig)
        modified_instructions[index] = (replaced, instructions[index][1])
        let (acc, terminates) = sol1(modified_instructions)
        if terminates:
            return acc
        else:
            modified_instructions[index] = (orig, instructions[index][1])


assert sol1(parse(test))[0] == 5
let instructions = parse(data)
dump sol1(instructions)[0]

assert sol2(parse(test)) == 8
dump sol2(instructions)