import strutils, sugar, tables, sequtils, re, algorithm

let test = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".splitLines
let data = readFile("data.txt").splitLines
let allergens_re = re"([^(]*)\(contains ([^)]*)\)"

proc sol1(data: seq[string]): (int, string) =
    var number: int = 0
    var count = initTable[string, int]()
    var poss = initTable[string, seq[string]]()
    for line in data:
        var products: seq[string]
        var allergens: seq[string] = @[]
        if line =~ allergens_re:
            products = matches[0].split(" ").filterIt(it != "")
            allergens = matches[1].split(",").mapIt(strip(it))
        else:
            products = line.split(" ").filterIt(it != "")
        for product in products:
            if count.hasKeyOrPut(product, 1):
                count[product] += 1
        for allergen in allergens:
            if poss.hasKeyOrPut(allergen, products):
                var newPoss: seq[string] = @[]
                for product in poss[allergen]:
                    if product in products:
                        newPoss.add(product)
                poss[allergen] = newPoss
    var uncertain: seq[string] = @[]
    for allergen, possibilities in poss:
        uncertain.add(possibilities)
    uncertain = deduplicate(uncertain)
    for product, appearance in count:
        if product notin uncertain:
            number += appearance
    var fixed: Table[string, string] = initTable[string, string]()
    var fixed_ing: seq[string] = @[]
    while fixed.len != uncertain.len:
        for allergen, possibilities in poss:
            if allergen notin fixed:
                if possibilities.len == 1:
                    fixed[allergen] = possibilities[0]
                    fixed_ing.add(possibilities[0])
                else:
                    var trying: seq[string] = @[]
                    for p in possibilities:
                        if p notin fixed_ing:
                            trying.add(p)
                    poss[allergen] = trying
    return (number, toSeq(fixed.keys).sorted().mapIt(fixed[it]).foldl(a & "," & b))

assert test.sol1 == (5, "mxmxvkd,sqjhc,fvjkl")
dump data.sol1