import strutils
import sugar
import tables
import sequtils
import sets

let test = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".split("\n")
let test2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".split("\n")

let data = readFile("data.txt").split("\n")

proc traverse(reverse: Table[string, seq[string]], containing: var seq[string] , bag: string): void =
    if not reverse.contains(bag):
        if not containing.contains(bag):
            containing.add(bag)
    else:
        for bag in reverse[bag]:
            if not containing.contains(bag):
                containing.add(bag)
            traverse(reverse, containing, bag)


proc sol1(rules: seq[string]): int =
    var 
        reverse = initTable[string, seq[string]]()
        containing: seq[string] = @[]
    for rule in rules:
        let 
            outer = rule.split(" bags contain ")[0]
            inners = rule.split(" bags contain ")[1]
        if inners != "no other bags.":
            let elements = inners.split(", ").mapIt(it.replace(" bags", "").replace(" bag", "").replace(".", "").split(" ")[1..^1].join(" "))
            for element in elements:
                if element in reverse:
                    reverse[element].add(outer)
                else:
                    reverse[element] = @[outer]
    traverse(reverse, containing, "shiny gold")
    result = len(containing)

proc dig(containing: Table[string, Table[string, int]], bag: string): int =
    if bag notin containing:
        return 0
    for key, value in containing[bag]:
        result += value*(1 + dig(containing, key))


proc sol2(rules: seq[string]): int =
    var 
        containing = initTable[string, Table[string, int]]()
    for rule in rules:
        let 
            outer = rule.split(" bags contain ")[0]
            inners = rule.split(" bags contain ")[1]
        if inners != "no other bags.":
            let elements = inners.split(", ").mapIt(it.replace(" bags", "").replace(" bag", "").replace(".", ""))
            containing[outer] = initTable[string, int]()
            for element in elements:
                let
                    amount = element.split(" ")[0].parseInt()
                    bag = element.split(" ")[1..^1].join(" ")
                containing[outer][bag] = amount
    result = dig(containing, "shiny gold")

assert sol1(test) == 4
dump sol1(data)

assert sol2(test) == 32
assert sol2(test2) == 126
dump sol2(data)
