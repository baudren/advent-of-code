import strutils
import sugar
import sequtils

let test = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".split("\n\n").mapIt(it.replace("\n", " "))
let data = readFile("data.txt").split("\n\n").mapIt(it.replace("\n", " "))

proc sol1(data: seq[string]): int =
    const required = @["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for passport in data:
        let fields = passport.split(" ").mapIt(it.split(":")[0])
        if required.allIt(fields.contains(it)):
            result += 1
        

assert sol1(test) == 2
dump sol1(data)

let invalid = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007""".split("\n\n").mapIt(it.replace("\n", " "))
let valid = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""".split("\n\n").mapIt(it.replace("\n", " "))

import tables
import re
let hcl = re"#[0-9a-f]{6}"
const ecl = @["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
let pid = re"^[0-9]{9}$"


proc sol2(data: seq[string]): int =
    const required = @["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for passport in data:
        var fields = initTable[string, string]()
        for entry in passport.split(" "):
            if entry != "":
                fields[entry.split(":")[0]] = entry.split(":")[1]
        if required.allIt(fields.contains(it)):
            var valid_fields = 0
            for k, v in fields.pairs:
                case k:
                    of "byr":
                        if len(v) == 4:
                            let nv = parseInt(v)
                            if nv <= 2002 and nv >= 1920:
                                valid_fields += 1
                    of "iyr":
                        if len(v) == 4:
                            let nv = parseInt(v)
                            if nv <= 2020 and nv >= 2010:
                                valid_fields += 1
                    of "eyr":
                        if len(v) == 4:
                            let nv = parseInt(v)
                            if nv <= 2030 and nv >= 2020:
                                valid_fields += 1
                    of "hgt":
                        if len(v) > 3:
                            if v[^2..^1] == "cm":
                                if len(v) >= 5:
                                    let nv = parseInt(v[0..^3])
                                    if nv <= 203 and nv >= 150:
                                        valid_fields += 1
                            elif v[^2..^1] == "in":
                                if len(v) >= 4:
                                    let nv = parseInt(v[0..^3])
                                    if nv <= 76 and nv >= 59:
                                        valid_fields += 1
                    of "hcl":
                        if v =~ hcl:
                            valid_fields += 1
                    of "ecl":
                        if ecl.contains(v):
                            valid_fields += 1
                    of "pid":
                        if v =~ pid:
                            valid_fields += 1
            if valid_fields == 7:
                #var output = ""
                #for k,v in fields.pairs:
                #    if k != "cid":
                #        output.add(k & ": " & v & "\t")
                #echo output
                #echo fields.filter(it => it.key != "cid")
                result += 1
            

assert sol2(invalid) == 0
assert sol2(valid) == 4
dump sol2(data)