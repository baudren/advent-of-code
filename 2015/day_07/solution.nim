import strutils, sugar, re, tables, bitops

let data = readFile("data.txt").splitLines

proc sol1(data: seq[string], init: uint16): uint16 =
    var wires = initTable[string, uint16]()
    if init != 0:
        wires["b"] = init
    while len(wires) != len(data):
        for line in data:
            if line =~ re"(.*) -> (.*)":
                let wire = matches[1]
                if wire in wires:
                    continue
                if matches[0] =~ re"^(\d+)$":
                    wires[wire] = uint16(matches[0].strip.parseUInt)
                elif matches[0].startsWith("NOT"):
                    let negated = matches[0].split(" ")[1]
                    if negated in wires:
                        wires[wire] = wires[negated].bitnot
                elif matches[0].contains("AND"):
                    let 
                        a = matches[0].split(" ")[0]
                        b = matches[0].split(" ")[2]
                    if a =~ re"(\d+)":
                        let value = uint16(matches[0].parseUInt)
                        if b in wires:
                            wires[wire] = value and wires[b]
                    elif a in wires and b in wires:
                        wires[wire] = wires[a] and wires[b]
                elif matches[0].contains("OR"):
                    let 
                        a = matches[0].split(" ")[0]
                        b = matches[0].split(" ")[2]
                    if a in wires and b in wires:
                        wires[wire] = wires[a] or wires[b]
                elif matches[0].contains("SHIFT"):
                    let
                        a = matches[0].split(" ")[0]
                        action = matches[0].split(" ")[1]
                        value = matches[0].split(" ")[2].parseInt
                    if a in wires:
                        case action:
                            of "LSHIFT":
                                wires[wire] = wires[a] shl value
                            of "RSHIFT":
                                wires[wire] = wires[a] shr value
                            else:
                                discard
                else:
                    let a = matches[0]
                    if a in wires:
                        wires[wire] = wires[a]
    return wires["a"]

let a = data.sol1(0)
dump a
dump data.sol1(a)
