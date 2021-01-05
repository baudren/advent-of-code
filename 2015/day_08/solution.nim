import strutils, sugar

let test = """
""
"abc"
"aaa\"aaa"
"\x27"""".splitLines
let data = readFile("data.txt").splitLines

proc sol1(data: seq[string]): int =
    var (total_char, char_in_str) = (0, 0)
    for line in data:
        #echo len(line)
        total_char += len(line)
        var char_count = len(line)-2
        var workLine = line
        let double_back = line.count("\\\\")
        char_count -= (double_back)
        workLine = line.replace("\\\\", "A")
        let hexa = workLine.count("\\x")
        char_count -= hexa*3
        let back = workLine.count("\\")
        char_count -= (back-hexa)
        char_in_str += char_count
    return total_char - char_in_str

proc sol2(data: seq[string]): int =
    var (total_char, char_encoded) = (0, 0)
    for line in data:
        #echo len(line)
        total_char += len(line)
        var char_count = len(line)+4
        var workLine = line
        let double_back = line.count("\\\\")
        char_count += 2*double_back
        workLine = line.replace("\\\\", "A")
        let hexa = workLine.count("\\x")
        char_count += hexa
        let back = workLine.count("\\")
        char_count += 2*(back-hexa)
        char_encoded += char_count
        dump len(line)
        dump char_count
    return char_encoded - total_char

dump data.sol1
dump data.sol2