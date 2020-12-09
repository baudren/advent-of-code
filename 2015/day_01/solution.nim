import strutils
import sequtils
import sugar

let test = ""
let data = readFile("data.txt")

proc sol1(data: string): int =
    for character in data:
        case character:
            of '(':
                result += 1
            of ')':
                result -= 1
            else:
                discard

proc sol2(data: string): int =
    for index in 0..<data.len:
        case data[index]:
            of '(':
                result += 1
            of ')':
                result -= 1
            else:
                discard
        if result == -1:
            return index + 1

assert sol1("(())") == 0
dump sol1(data)
assert sol2(")") == 1
assert sol2("()())") == 5
dump sol2(data)
