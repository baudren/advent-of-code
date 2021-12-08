from aocd import get_data, submit

numbers = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}

def sol1(data):
    result = 0
    for line in data:
        signals, digits = [e.strip() for e in line.split("|")]
        for digit in digits.split(" "):
            if len(digit) in [2, 3, 4, 7]:
                result += 1
    return result

def sol2(data):
    result = 0
    for line in data:
        signals, digits = [e.strip() for e in line.split("|")]
        mapping = extract_mapping(signals.split(" "))
        number = ''
        for digit in digits.split(" "):
            
            key = [k for k in mapping if all(l in k for l in digit) and all(l in digit for l in k)][0]
            number += str(mapping[key])
        result += int(number)
    return result

def extract_mapping(signals):
    mapping = {}
    one = [e for e in signals if len(e) == 2][0]
    seven = [e for e in signals if len(e) == 3][0]
    four = [e for e in signals if len(e) == 4][0]
    eight = [e for e in signals if len(e) == 7][0]
    mapping[one] = 1
    # Three is the length 5 where the 1 is fully in
    three = [e for e in signals if len(e) == 5 and all(i in e for i in one)][0]
    # The six is the only length 6 where if you remove the 1, you have 5 digits
    sixies = [e for e in signals if len(e) == 6]
    fives = [e for e in signals if len(e) == 5]
    six = [e for e in sixies if len(set(e)-set(one)) == 5][0]
    
    middles = "".join(list(set(fives[0])&set(fives[1])&set(fives[2])))
    zero = [e for e in sixies if len(set(e)-set(middles)) == 4][0]
    nine = [e for e in sixies if e not in [six, zero]][0]
    two = [e for e in signals if len(e)==5 and e != three and len(set(e).union(set(six)))==7][0]
    five = [e for e in signals if len(e)==5 and e not in [three, two]][0]
    
    mapping[two] = 2
    mapping[five] = 5
    mapping[three] = 3
    mapping[six] = 6
    mapping[zero] = 0
    mapping[nine] = 9
    mapping[seven] = 7
    mapping[four] = 4
    mapping[eight] = 8

    
    print(mapping)
    return mapping

if __name__ == "__main__":
    data = open('day08.txt').readlines()
    test = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".split("\n")
    assert sol1(test) == 26
    print(sol1(data))
    assert sol2(test) == 61229
    print(sol2(data))