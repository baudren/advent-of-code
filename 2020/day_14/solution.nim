import strutils
import sugar
import sequtils
import tables
import re

let test = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".split("\n")
let test2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".split("\n")
var data = readFile("data.txt").splitLines()
let regex = re"mem\[(\d+)\] = (\d+)"


proc sol1(data: seq[string]): int =
    var mask = ""
    var values = initTable[int, int]()
    for line in data:
        if line.startsWith("mask"):
            mask = line.split("=")[1].strip()
        elif line =~ regex:
            let
                (address, value) = (parseInt(matches[0]), parseInt(matches[1]))
            var bin_value = value.toBin(len(mask))
            for i, x in mask:
                if x != 'X':
                    bin_value[i] = mask[i]
            values[address] = parseBinInt(bin_value)
    return foldl(toSeq(values.values), a+b)


proc sol2(data: seq[string]): int =
    var mask = ""
    var values = initTable[int, int]()
    for line in data:
        if line.startsWith("mask"):
            mask = line.split("=")[1].strip()
        elif line =~ regex:
            let
                (orig_address, value) = (parseInt(matches[0]), parseInt(matches[1]))
            var bin_address = orig_address.toBin(len(mask))
            for i, x in mask:
                if x != '0':
                    bin_address[i] = mask[i]
            var addresses: seq[string] = @[bin_address]
            while true:
                for i in countdown(addresses.len-1, 0):
                    if 'X' in addresses[i]:
                        let address = addresses[i]
                        addresses.delete(i)
                        var (a, b) = (address, address)
                        for j, x in address:
                            if x == 'X':
                                a[j] = '0'
                                b[j] = '1'
                                break
                        addresses.add(a)
                        addresses.add(b)
                if 'X' notin addresses[0]:
                    break
            for address in addresses:
                values[parseBinInt(address)] = value
    return foldl(toSeq(values.values), a+b)


assert sol1(test) == 165
dump sol1(data)

assert sol2(test2) == 208
dump sol2(data)