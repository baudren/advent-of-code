import strutils
import sugar
import tables
import sequtils
import sets
import algorithm


let test = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n").mapIt(toSeq(it.items))
var data = readFile("data.txt").split("\n").mapIt(toSeq(it.items))

type
    Game = object
        data: seq[seq[char]]

var testGame = Game(data: test)

proc should_change(i: int, j: int, data: seq[seq[char]]): bool =
    if data[i][j] == '.':
        return false
    # if all seats around are empty, fill it
    var seats_around: seq[char] = @[]
    if i-1 >= 0:
        if j-1 >= 0:
            seats_around.add(data[i-1][j-1])
        seats_around.add(data[i-1][j])
        if j+1 < len(data[i]):
            seats_around.add(data[i-1][j+1])
    if j-1 >= 0:
        seats_around.add(data[i][j-1])
    if j+1 < len(data[i]):
        seats_around.add(data[i][j+1])
    if i+1 < len(data):
        if j-1 >= 0:
            seats_around.add(data[i+1][j-1])
        seats_around.add(data[i+1][j])
        if j+1 < len(data[i]):
            seats_around.add(data[i+1][j+1])
    #echo i, " ", j, " ", data[i][j], " ", seats_around
    if data[i][j] == 'L':
        return seats_around.count('#') == 0
    else:
        return seats_around.count('#') >= 4


proc should_change_2(i: int, j: int, data: seq[seq[char]]): bool =
    if data[i][j] == '.':
        return false
    # if all seats around are empty, fill it
    var seats_around: seq[char] = @[]
    # point in all 8 directions
    # left
    var index = 1
    while true:
        if j-index >= 0:
            if data[i][j-index] != '.':
                seats_around.add(data[i][j-index])
                break
            index += 1
        else:
            break
    # right
    index = 1
    while true:
        if j+index < len(data[i]):
            if data[i][j+index] != '.':
                seats_around.add(data[i][j+index])
                break
            index += 1
        else:
            break
    # up
    index = 1
    while true:
        if i-index >= 0:
            if data[i-index][j] != '.':
                seats_around.add(data[i-index][j])
                break
            index += 1
        else:
            break
    # down
    index = 1
    while true:
        if i+index < len(data):
            if data[i+index][j] != '.':
                seats_around.add(data[i+index][j])
                break
            index += 1
        else:
            break
    # up-left
    index = 1
    while true:
        if i-index >= 0 and j-index >= 0:
            if data[i-index][j-index] != '.':
                seats_around.add(data[i-index][j-index])
                break
            index += 1
        else:
            break
    # up-right
    index = 1
    while true:
        if i-index >= 0 and j+index < len(data[i]):
            if data[i-index][j+index] != '.':
                seats_around.add(data[i-index][j+index])
                break
            index += 1
        else:
            break
    # down-left
    index = 1
    while true:
        if i+index < len(data) and j-index >= 0:
            if data[i+index][j-index] != '.':
                seats_around.add(data[i+index][j-index])
                break
            index += 1
        else:
            break
    # down-right
    index = 1
    while true:
        if i+index < len(data) and j+index < len(data[i]):
            if data[i+index][j+index] != '.':
                seats_around.add(data[i+index][j+index])
                break
            index += 1
        else:
            break
    #echo i, " ", j, " ", data[i][j], " ", seats_around
    if data[i][j] == 'L':
        return seats_around.count('#') == 0
    else:
        return seats_around.count('#') >= 5

proc display(data: seq[seq[char]]): void =
    for line in data:
        echo line.join("")
    echo ""

# Apply one time the rule
proc transform(game: var Game): bool =
    #display(game.data)
    var newData = game.data
    for i, line in game.data:
        for j, c in line:
            if should_change(i, j, game.data):
                newData[i][j] = (if game.data[i][j] == 'L': '#' else: 'L')
    if newData == game.data:
        return false
    else:
        game.data = newData
    #display(newData)
    return true

proc transform2(game: var Game): bool =
    var newData = game.data
    for i, line in game.data:
        for j, c in line:
            if should_change_2(i, j, game.data):
                newData[i][j] = (if game.data[i][j] == 'L': '#' else: 'L')
    if newData == game.data:
        return false
    else:
        game.data = newData
    #display(newData)
    return true


proc count_seats(game: Game): int =
    for line in game.data:
        result += line.count('#')

proc sol1(game: var Game): int =
    while true:
        if not game.transform():
            break
    return game.count_seats()

proc sol2(game: var Game): int =
    #display(game.data)
    while true:
        if not game.transform2():
            break
    return game.count_seats()


assert sol1(testGame) == 37
var game = Game(data: data)
dump sol1(game)

testGame = Game(data: test)
game = Game(data: data)
assert sol2(testGame) == 26
dump sol2(game)