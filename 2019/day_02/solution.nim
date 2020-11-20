import strutils
import sequtils

let program = readFile("data.txt").split(",").mapIt(parseInt(it))

type
    IntCode = object
        program: seq[int]
        head: int

proc apply(int_code: var IntCode): bool =
    let
        a = int_code.program[int_code.head]
    if a == 99:
        return false
    let
        b = int_code.program[int_code.head+1]
        c = int_code.program[int_code.head+2]
        d = int_code.program[int_code.head+3]
    case a:
        of 1:
            int_code.program[d] = int_code.program[b] + int_code.program[c]
        of 2:
            int_code.program[d] = int_code.program[b] * int_code.program[c]
        else:
            discard
    int_code.head += 4
    return true

proc execute(int_code: var IntCode): int =
    while int_code.apply():
        continue
    return int_code.program[0]

proc newIntCode(prog: seq[int]): IntCode =
    IntCode(program: prog, head: 0)

proc verify(prog: seq[int], output: seq[int]) =
    var
        int_code = newIntCode(prog)
    discard int_code.execute()
    assert int_code.program == output, "wrong"

verify(@[1, 0, 0, 0, 99], @[2, 0, 0, 0, 99])
verify(@[2, 3, 0, 3, 99], @[2, 3, 0, 6, 99])
verify(@[2,4,4,5,99,0], @[2,4,4,5,99,9801])
verify(@[1,1,1,4,99,5,6,0,99], @[30,1,1,4,2,5,6,0,99])

var
    int_code = newIntCode(program)

# warmup
int_code.program[1] = 12
int_code.program[2] = 2
echo int_code.execute()

proc sol2(program: seq[int], output: int): int =
    for verb in 0..99:
        for noun in 0..99:
            var int_code = newIntCode(program)
            int_code.program[1] = noun
            int_code.program[2] = verb
            if int_code.execute() == output:
                return noun*100 + verb

echo sol2(program, 19690720)
