import strutils
import sugar
import sequtils

let test = "1-3 a: abcde,1-3 b: cdefg,2-9 c: ccccccccc".split(",")
let data = readFile("data.txt").splitLines()

# TODO Use regex for parsing, but which module???
proc sol1(data: seq[string]): int =
    for line in data:
        let
            policy = line.split(":")[0]
            password = line.split(":")[1].strip()
            letter = policy.split(" ")[1]
            min_n = parseInt(policy.split(" ")[0].split("-")[0])
            max_n = parseInt(policy.split(" ")[0].split("-")[1])
            count = password.count(letter)
        if count >= min_n and count <= max_n:
            result += 1

proc sol2(data: seq[string]): int =
    for line in data:
        let
            policy = line.split(":")[0]
            password = line.split(":")[1].strip()
            letter = policy.split(" ")[1][0]
            index_1 = parseInt(policy.split(" ")[0].split("-")[0])
            index_2 = parseInt(policy.split(" ")[0].split("-")[1])
        var count: int = 0
        if password[index_1-1] == letter:
            count = count + 1
        if password[index_2-1] == letter:
            count += 1
        if count == 1:
            result += 1

assert sol1(test) == 2
dump sol1(data)
assert sol2(test) == 1
dump sol2(data)