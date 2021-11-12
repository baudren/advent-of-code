import strutils
import sequtils

let program = readFile("data.txt").split(",").mapIt(parseInt(it))

type
    IntCodeComputer = object
        program: seq[int]
        input: seq[int]
        output: seq[int]
        head: int

proc apply(int_code: var IntCodeComputer): bool =
    let
        opcode = $int_code.program[int_code.head]
        instruction = opcode[^2..^1].parseInt
        mode = opcode[0..^2].parseInt
    if instruction == 99:
        return false
    case instruction:
        of 1, 2:
            let
                b = int_code.program[int_code.head+1]
                c = int_code.program[int_code.head+2]
                d = int_code.program[int_code.head+3]
            int_code.head += 4
            int_code.program[d] = int_code.program[b] + (if instruction == 2: -1 else: 1) * int_code.program[c]
        of 3, 4:
            let b = int_code.program[int_code.head+1]
            int_code.head += 2
            if instruction == 3:
        else:
            discard
    int_code.head += 4
    return true

proc execute(int_code: var IntCodeComputer): int =
    while int_code.apply():
        continue
    return int_code.program[0]

proc newIntCode(prog: seq[int]): IntCodeComputer =
    IntCodeComputer(program: prog, head: 0)