import strutils
import sugar
import tables
import sequtils
import re

let test2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""".split("\n")
let data = readFile("data.txt").split("\n")

let rule = re"^(\d+): (.*)$"


type
    Messages = object
        rules: Table[int, seq[string]]
        possibilities: Table[int, seq[string]]
        messages: seq[string]

proc toMessages(data: seq[string]): Messages =
    var rules = initTable[int, seq[string]]()
    var possibilities = initTable[int, seq[string]]()
    var messages: seq[string]

    for i, line in data:
        if line =~ rule:
            let index = matches[0].parseInt
            if matches[1].contains("\""):
                rules[index] = @[matches[1].replace("\"", "")]
                possibilities[index] = @[matches[1].replace("\"", "")]
            elif matches[1].contains("|"):
                rules[index] = @[matches[1].split("|")[0].strip, matches[1].split("|")[1].strip]
            else:
                rules[index] = @[matches[1]]
        elif line != "":
            messages.add(line)
    return Messages(rules: rules, messages: messages, possibilities: possibilities)

proc fillPossibilities(mess: var Messages): void =
    while mess.possibilities.len != mess.rules.len:
        for index, rule in mess.rules:
            if index notin mess.possibilities:
                var found: bool = true
                for part in rule:
                    if part.split(" ").anyIt(it.parseInt notin mess.possibilities):
                        found = false
                        break
                if found:
                    var full: seq[string] = @[]
                    for part in rule:
                        var list: seq[string] = @[]
                        for i in part.split(" "):
                            if list.len == 0:
                                list.add(mess.possibilities[i.parseInt])
                            else:
                                var newList: seq[string] = @[]
                                for e in list:
                                    for p in mess.possibilities[i.parseInt]:
                                        newList.add(e & p)
                                list = newList
                        full.add(list)
                    mess.possibilities[index] = full

proc sol1(mess: Messages): int =
    let (l_42, l_31) = (mess.possibilities[42][0].len, mess.possibilities[31][0].len)
    for message in mess.messages:
        var (n_42, n_31, index, count, found) = (0, 0, 0, 1, false)
        while true:
            if n_31 == 0 and message[index..count*l_42-1] in mess.possibilities[42]:
                n_42 += 1
                index += l_42
                count += 1
                if index == len(message):
                    break
            elif message[index..count*l_31-1] in mess.possibilities[31]:
                n_31 += 1
                index += l_31
                count += 1
                if index == len(message):
                    found = true
                    break
            else:
                break
        if found and n_42 == 2 and n_31 == 1:
            result += 1

# Fitting against poss[42] and poss[31], if n times poss[42], only n-1 max times poss[31]
proc sol2(mess: Messages): int =
    let (l_42, l_31) = (mess.possibilities[42][0].len, mess.possibilities[31][0].len)
    for message in mess.messages:
        var (n_42, n_31, index, count, found) = (0, 0, 0, 1, false)
        while true:
            if n_31 == 0 and message[index..count*l_42-1] in mess.possibilities[42]:
                n_42 += 1
                index += l_42
                count += 1
                if index == len(message):
                    break
            elif message[index..count*l_31-1] in mess.possibilities[31]:
                n_31 += 1
                index += l_31
                count += 1
                if index == len(message):
                    found = true
                    break
            else:
                break
        if found and n_42 >= 2 and n_31 > 0 and n_42 > n_31:
            result += 1

var mess = data.toMessages
mess.fillPossibilities
dump mess.sol1

var testMess2 = test2.toMessages
testMess2.fillPossibilities
assert testMess2.sol2 == 12

dump mess.sol2