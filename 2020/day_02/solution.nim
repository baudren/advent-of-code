import strutils
import sugar
import re

let regex = re"(\d+)-(\d+) (\D): (\D+).*"

let test = "1-3 a: abcde,1-3 b: cdefg,2-9 c: ccccccccc".split(",")
let data = readFile("data.txt").splitLines()

# why are regex so slow??
proc sol1(data: seq[string]): int =
    for line in data:
        if line =~ regex:
            let
                (min_n, max_n, letter, password) = (parseInt(matches[0]), parseInt(matches[1]), matches[2], matches[3])
                count = password.count(letter)
            if count >= min_n and count <= max_n:
                result += 1

proc sol2(data: seq[string]): int =
    for line in data:
        if line =~ regex:
            let
                (index_1, index_2, letter, password) = (parseInt(matches[0]), parseInt(matches[1]), matches[2][0], matches[3])
            if (password[index_1-1] == letter) != (password[index_2-1] == letter):
                result += 1

assert sol1(test) == 2
dump sol1(data)
assert sol2(test) == 1
dump sol2(data)