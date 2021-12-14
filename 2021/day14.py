from collections import Counter

def parse(raw):
    template = ""
    rules = {}
    for line in raw:
        if '->' in line:
            start, add = line.split(" -> ")
            rules[start] = add
        elif line:
            template = line
    return template, rules

def sol(template, rules, steps):
    polymer = template
    pairs = {}
    for i in range(len(polymer)-1):
        if polymer[i:i+2] in pairs:
            pairs[polymer[i:i+2]] += 1
        else:
            pairs[polymer[i:i+2]] = 1
    counter = Counter(polymer)
    for step in range(steps):
        new_pairs = {}
        for key, value in pairs.items():
            if key in rules:
                if rules[key] in counter:
                    counter[rules[key]] += value
                else:
                    counter[rules[key]] = value
                a, b = key[0]+rules[key], rules[key]+key[1]
                if a in new_pairs:
                    new_pairs[a] += value
                else:
                    new_pairs[a] = value
                if b in new_pairs:
                    new_pairs[b] += value
                else:
                    new_pairs[b] = value
            else:
                new_pairs[key] = value
        pairs = new_pairs
    min_, max_ = min(counter.values()), max(counter.values())
    return max_-min_

if __name__ == "__main__":
    data = [e.strip() for e in open('day14.txt', 'r').readlines()]
    test = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split("\n")
    assert sol(*parse(test), 10) == 1588
    print(sol(*parse(data), 10))
    assert sol(*parse(test), 40) == 2188189693529
    print(sol(*parse(data), 40))