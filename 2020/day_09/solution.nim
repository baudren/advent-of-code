import strutils
import sugar
import tables
import sequtils
import sets


let test = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split("\n").map(parseInt)
const data = readFile("data.txt").split("\n").map(parseInt)

# Find first error
proc sol1(data: seq[int], preamble_length: int): int =
    var preamble = data[0..<preamble_length]
    echo preamble
    for number in data[preamble_length..^1]:
        var found = false
        for n in preamble:
            for m in preamble:
                if n != m and n + m == number:
                    found = true
                    break
            if found: break
        if not found:
            return number
        else:
            preamble.delete(0)
            preamble.add(number)

# Find the numbers that sum to wrong, and sum the lowest and highest
proc sol2(data: seq[int], wrong: int): int =
    var range_size = 2
    while true:
        dump range_size
        for n in 0..<data.find(wrong):
            var number = 0
            for i in 0..<range_size:
                number += data[n+i]
            if number == wrong:
                return data[n..<n+range_size].min()+data[n..<n+range_size].max()
            elif number > wrong:
                range_size += 1
                break

assert sol1(test, 5) == 127
let wrong = sol1(data, 25)
dump wrong

assert sol2(test, 127) == 62
dump sol2(data, wrong)