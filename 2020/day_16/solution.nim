import strutils
import sugar
import sequtils
import tables
import re

let test = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""".split("\n")
let data = readFile("data.txt").splitLines()

let
    ranges_pattern = re"([^:]*): (\d+)-(\d+) or (\d+)-(\d+)"

type
    Notes = object
        ranges: Table[string, seq[int]]
        own: seq[int]
        nearby: seq[seq[int]]

proc toNotes(data: seq[string]): Notes =
    var ranges = initTable[string, seq[int]]()
    var own: seq[int] = @[]
    var nearby: seq[seq[int]] = @[]

    var next_is_own = false
    for line in data:
        if line =~ ranges_pattern:
            ranges[matches[0]] = matches[1..4].map(parseInt)
        elif line == "your ticket:":
            next_is_own = true
        elif line.contains(","):
            if next_is_own:
                own = line.split(",").map(parseInt)
                next_is_own = false
            else:
                nearby.add(line.split(",").map(parseInt))
    return Notes(ranges: ranges, own: own, nearby: nearby)

proc toNotesWithoutInvalid(data: seq[string]): Notes =
    var ranges = initTable[string, seq[int]]()
    var own: seq[int] = @[]
    var nearby: seq[seq[int]] = @[]

    var next_is_own = false
    for line in data:
        if line =~ ranges_pattern:
            ranges[matches[0]] = matches[1..4].map(parseInt)
        elif line == "your ticket:":
            next_is_own = true
        elif line.contains(","):
            if next_is_own:
                own = line.split(",").map(parseInt)
                next_is_own = false
            else:
                let ticket = line.split(",").map(parseInt)
                # is there any value that is outside of every range?
                var found = true
                for value in ticket:
                    var count = 0
                    for k, r in ranges:
                        if value notin r[0]..r[1] and value notin r[2]..r[3]:
                            if value == 99:
                                echo r
                            count += 1
                    if count == len(ranges):
                        found = false
                        break
                if found:
                    nearby.add(ticket)
    return Notes(ranges: ranges, own: own, nearby: nearby)

# Ticket scanning error rate
proc sol1(data: seq[string]): int =
    var notes = data.toNotes()
    for ticket in notes.nearby:
        for value in ticket:
            var found = false
            for key, ranges in notes.ranges:
                if value in ranges[0]..ranges[1] or value in ranges[2]..ranges[3]:
                    found = true
                    break
            if not found:
                result += value

proc sol2(data: seq[string]): int =
    var notes = data.toNotesWithoutInvalid()
    # storing the field name: index in the ticket
    var positions: Table[string, int] = initTable[string, int]()
    while true:
        for position in 0..<len(notes.own):
            var valid: seq[string] = toSeq(notes.ranges.keys()).filterIt(it notin positions)
            for ticket in notes.nearby:
                #dump ticket
                for i in countDown(len(valid)-1, 0):
                    let r = notes.ranges[valid[i]]
                    if ticket[position] notin r[0]..r[1] and ticket[position] notin r[2]..r[3]:
                        valid.delete(i)
            if len(valid) == 1:
                positions[valid[0]] = position
        if len(positions) == len(notes.ranges):
            break
    result = 1
    for k, v in positions:
        if k.contains("departure"):
            result *= notes.own[v]

assert sol1(test) == 71
dump sol1(data)

dump sol2(data)