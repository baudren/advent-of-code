import strutils
import sugar
import sequtils

let test = """FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL""".split("\n")
let data = readFile("data.txt").split("\n")

proc sol(data: seq[string]): (int, int) =
    var (min, max, seat) = (-1, 0, 0)
    var found: seq[int] = @[]
    for boarding_pass in data:
        let
            row_input = boarding_pass[0..^4]
            col_input = boarding_pass[^3..^1]
        var 
            rows = [0, 127]
            cols = [0, 7]
        for partition in row_input:
            if partition == 'F':
                rows[1] = rows[0]+int((rows[1]-rows[0]+1)/2)-1
            else:
                rows[0] = rows[0]+int((rows[1]-rows[0]+1)/2)
        for partition in col_input:
            if partition == 'L':
                cols[1] = cols[0]+int((cols[1]-cols[0]+1)/2)-1
            else:
                cols[0] = cols[0]+int((cols[1]-cols[0]+1)/2)
        assert rows[0] == rows[1]
        assert cols[0] == cols[1]
        let id = rows[0] * 8 + cols[0]
        if id > max:
            max = id
        if min == -1 or id < min:
            min = id
        found.add(id)
    let ids: seq[int] = toSeq(min..max)
    for id in ids:
        if not found.contains(id):
            seat = id
            break
    return (max, seat)


assert sol(test)[0] == 820
dump sol(data)