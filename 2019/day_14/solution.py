from math import ceil

reaction_data = open('data.txt', 'r').readlines()

# reaction_data = """10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL""".split("\n")
# reaction_data = """9 ORE => 2 A
# 8 ORE => 3 B
# 7 ORE => 5 C
# 3 A, 4 B => 1 AB
# 5 B, 7 C => 1 BC
# 4 C, 1 A => 1 CA
# 2 AB, 3 BC, 4 CA => 1 FUEL""".split("\n")
# reaction_data = """157 ORE => 5 NZVS
# 165 ORE => 6 DCFZ
# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
# 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
# 179 ORE => 7 PSHF
# 177 ORE => 5 HKGWZ
# 7 DCFZ, 7 PSHF => 2 XJWVT
# 165 ORE => 2 GPVTF
# 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""".split("\n")
# reaction_data = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
# 17 NVRVD, 3 JNWZP => 8 VPVL
# 53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
# 22 VJHF, 37 MNCFX => 5 FWMGM
# 139 ORE => 4 NVRVD
# 144 ORE => 7 JNWZP
# 5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
# 5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
# 145 ORE => 6 MNCFX
# 1 NVRVD => 8 CXFTF
# 1 VJHF, 6 MNCFX => 4 RFSQX
# 176 ORE => 6 VJHF""".split("\n")

def parse_formula(line, reactions):
    output = line.split("=>")[-1].strip().split()[-1]
    output_quant = int(line.split("=>")[-1].strip().split()[0])
    inputs = line.split("=>")[0]
    input_elements = []
    for elem in inputs.split(","):
        input_elements.append((elem.strip().split()[1], int(elem.strip().split()[0])))
    reactions[output] = (output_quant, input_elements)

reactions = {}
for line in reaction_data:
    parse_formula(line, reactions)

def compute_ore(element, amount, reactions):
    if element == "ORE":
        return amount
    reaction = reactions[element]
    times = ceil(amount/reaction[0])
    return sum([compute_ore(e[0], e[1]*times, reactions) for e in reaction[1]])


def break_element(element, amount, reactions):
    times = ceil(amount/reactions[element][0])
    return [(k, v*times) for k, v in reactions[element][1]]


class Analyser:

    ranks = {}
    def __init__(self, reactions):
        self.reactions = reactions
        self.rank_elements()
    
    def rank_elements(self):
        # rank elements by distance to ORE
        # 1 is created directly by ore, and 2 is created directly by elements of distance at most 1, etc..
        for element, value in self.reactions.items():
            self.ranks[element] = self.distance(element)

    def distance(self, element):
        value = self.reactions[element]
        if len(value[1]) == 1 and value[1][0][0] == "ORE":
            return 1
        else:
            return max([self.distance(e[0]) for e in value[1]])+1
    
    def part_one(self, amount=1):
        # produce 1 FUEL
        ore_needs = {}
        fuel = reactions["FUEL"]
        times = ceil(amount/fuel[0])
        ore_needs["FUEL"] = times
        rank = self.ranks["FUEL"]
        while True:
            if rank == 1:
                break
            to_delete = []
            to_add = []
            for element, value in ore_needs.items():
                if self.ranks[element] == rank:
                    to_add.extend(break_element(element, value, reactions))
                    to_delete.append(element)
            for e in to_add:
                if e[0] in ore_needs:
                    ore_needs[e[0]] += e[1]
                else:
                    ore_needs[e[0]] = e[1]
            for e in to_delete:
                ore_needs.pop(e)
            rank = max([self.ranks[k] for k in ore_needs])
        return sum([compute_ore(k, v, reactions) for k, v in ore_needs.items()])

    def part_two(self):
        fuel = 1000000000000//self.part_one()
        f_min, f_max = fuel, 2*fuel
        while True:
            middle = (f_max+f_min)//2
            f_1 = self.part_one(middle)
            if f_1 > 1000000000000:
                f_max = middle
            else:
                f_min = middle
            if f_min == f_max-1:
                break
        return f_min
        

analyser = Analyser(reactions)
print(analyser.part_one())
print(analyser.part_two())
