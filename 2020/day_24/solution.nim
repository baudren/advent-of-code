import strutils, sugar

let test = readFile("test.txt").splitLines
let data = readFile("data.txt").splitLines

proc sol1(data: seq[string]): seq[(int, int)] =
    var flipped: seq[(int, int)] = @[]
    var head: (int, int)
    var skipping: bool = false
    for line in data:
        head  = (0, 0)
        for i, c in line:
            if skipping:
                skipping = false
                continue
            if c == 'w':
                head = (head[0]-1, head[1])
            elif c == 'e':
                head = (head[0]+1, head[1])
            else:
                case line[i..i+1].join(""):
                    of "se":
                        head = (head[0], head[1]+1)
                    of "ne":
                        head = (head[0]+1, head[1]-1)
                    of "nw":
                        head = (head[0], head[1]-1)
                    of "sw":
                        head = (head[0]-1, head[1]+1)
                skipping = true
        if head in flipped:
            flipped.del(flipped.find(head))
        else:
            flipped.add(head)
    return flipped


proc sol2(data: seq[(int, int)], moves: int): int =
    var data = data
    # determine boundaries
    var (q_min, r_min, q_max, r_max) = (0, 0, 0, 0)
    for black in data:
        if black[0] < q_min:
            q_min = black[0]
        elif black[0] > q_max:
            q_max = black[0]
        if black[1] < r_min:
            r_min = black[1]
        elif black[1] > r_max:
            r_max = black[1]
    for i in 1..moves:
        var to_add: seq[(int, int)] = @[]
        var to_remove: seq[(int, int)] = @[]
        for r in r_min-1..r_max+1:
            for q in q_min-1..q_max+1:
                var neighbours: int = 0
                if (q+1, r) in data:
                    neighbours += 1
                if (q+1, r-1) in data:
                    neighbours += 1
                if (q, r-1) in data:
                    neighbours += 1
                if (q-1, r) in data:
                    neighbours += 1
                if (q-1, r+1) in data:
                    neighbours += 1
                if (q, r+1) in data:
                    neighbours += 1
                if (q, r) in data:
                    if neighbours == 0 or neighbours > 2:
                        to_remove.add((q, r))
                else:
                    if neighbours == 2:
                        to_add.add((q, r))
        for remove in to_remove:
            data.del(data.find(remove))
        for add in to_add:
            data.add(add)
        for black in data:
            if black[0] < q_min:
                q_min = black[0]
            elif black[0] > q_max:
                q_max = black[0]
            if black[1] < r_min:
                r_min = black[1]
            elif black[1] > r_max:
                r_max = black[1]

    return data.len

let testBlack = test.sol1
assert testBlack.len == 10
let black = data.sol1
dump black.len

assert testBlack.sol2(100) == 2208
dump black.sol2(100)

