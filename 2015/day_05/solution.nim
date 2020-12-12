import strutils
import sequtils
import sugar

let data = readFile("data.txt").splitLines()

proc is_nice(str: string): bool =
    result = true
    var vowels = 0
    for c in str:
        if c in "aeiou":
            vowels += 1
    if vowels < 3:
        return false
    var has_double = false
    for i, c in str:
        if i > 0:
            if str[i-1] == c:
                has_double = true
                break
    if not has_double:
        return false
    for offender in ["ab", "cd", "pq", "xy"]:
        if offender in str:
            return false

proc is_nice2(str: string): bool =
    result = true
    var has_double = false
    for i, c in str:
        if i < len(str) - 1:
            if str.count([c, str[i+1]].join("")) >= 2:
                has_double = true
                break
    if not has_double:
        return false
    var has_bridge = false
    for i, c in str:
        if i >= 2:
            if str[i-2] == c:
                has_bridge = true
    return has_bridge

assert "ugknbfddgicrmopn".is_nice()
assert "aaa".is_nice()
assert not "jchzalrnumimnmhp".is_nice()
assert not "haegwjzuvuyypxyu".is_nice()
assert not "dvszwmarrgswjxmb".is_nice()
dump data.map(is_nice).count(true)
assert "qjhvhtzxzqqjkmpb".is_nice2()
assert "xxyxx".is_nice2()
assert not "uurcxstgmygtbstg".is_nice2()
dump data.map(is_nice2).count(true)