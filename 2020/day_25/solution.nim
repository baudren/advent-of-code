import sugar, sequtils, strutils

let test = """5764801
17807724""".splitLines.map(parseInt)
let data = """16616892
14505727""".splitLines.map(parseInt)


proc transform(subject_number: int, loop_size: int, start: int): int =
    result = start
    for i in 1..loop_size:
        result *= subject_number
        result = result mod 20201227

proc sol1(data: seq[int]): int =
    let 
        card_pub = data[0]
        door_pub = data[1]
    var card_loop = 1
    var card_value = 1
    while true:
        card_value = transform(7, 1, card_value)
        if card_value == card_pub:
            break
        else:
            card_loop += 1
    return transform(door_pub, card_loop, 1)

assert test.sol1 == 14897079
dump data.sol1