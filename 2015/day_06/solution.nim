import sequtils,strutils,re,sugar

let lineRe = re"(turn off|turn on|toggle) (\d+,\d+) through (\d+,\d+)"

let data = readFile("data.txt").splitLines

proc sol1(data: seq[string]): int =
    var lights: array[1_000_000, bool]
    for line in data:
        if line =~ lineRe:
            let start: seq[int] = matches[1].split(",").map(parseInt)
            let stop: seq[int] = matches[2].split(",").map(parseInt)
            case matches[0]:
                of "turn off":
                    for x in start[0]..stop[0]:
                        for y in start[1]..stop[1]:
                            lights[x*1000+y] = false
                of "turn on":
                    for x in start[0]..stop[0]:
                        for y in start[1]..stop[1]:
                            lights[x*1000+y] = true
                of "toggle":
                    for x in start[0]..stop[0]:
                        for y in start[1]..stop[1]:
                            lights[x*1000+y] = not lights[x*1000+y]
                else:
                    echo "oups"
    return lights.count(true)

proc sol2(data: seq[string]): int64 =
    var lights: array[1_000_000, int]
    for line in data:
        if line =~ lineRe:
            let start: seq[int] = matches[1].split(",").map(parseInt)
            let stop: seq[int] = matches[2].split(",").map(parseInt)
            case matches[0]:
                of "turn on":
                    for x in start[0]..stop[0]:
                        for y in start[1]..stop[1]:
                            lights[x*1000+y] += 1
                of "turn off":
                    for x in start[0]..stop[0]:
                        for y in start[1]..stop[1]:
                            if lights[x*1000+y] > 0:
                                lights[x*1000+y] -= 1
                of "toggle":
                    for x in start[0]..stop[0]:
                        for y in start[1]..stop[1]:
                            lights[x*1000+y] += 2
                else:
                    echo "oups"
    for light in lights:
        result += light

dump sol1(data)
dump sol2(data)
