import strutils, sugar

var data = "1113122113"

proc next(str: string): string =
    var cur = -1
    for i, c in str[0..^1]:
        if i <= cur:
            continue
        cur = i
        var count = 1
        while cur+1 < str.len and str[cur+1] == c:
            count += 1
            cur += 1
        result = result & count.intToStr & $c

assert "1".next == "11"
assert "11".next == "21"
assert "21".next == "1211"
assert "1211".next == "111221"
assert "111221".next == "312211"

for i in 1..50:
    dump i
    dump data[0..9]
    data = data.next
    if i == 40:
        dump data.len
dump data.len