import strutils
import sugar
import tables
import sequtils


let test = """.#.
..#
###""".split("\n").mapIt(toSeq(it.items))
var data = readFile("data.txt").split("\n").mapIt(toSeq(it.items))

type
    Game = object
        values: Table[(int, int, int), bool]
        enclosing: Table[int, seq[int]]
    Game2 = object
        values: Table[(int, int, int, int), bool]
        enclosing: Table[int, seq[int]]

proc toGame(data: seq[seq[char]]): Game =
    var values = initTable[(int, int, int), bool]()
    var enclosing: Table[int, seq[int]] = initTable[int, seq[int]]()
    enclosing[0] = @[-1, 1]
    enclosing[1] = @[-1, len(data)]
    enclosing[2] = @[-1, len(data[0])]
    for i, line in data:
        for j, c in line:
            values[(0, i, j)] = c == '#'
    return Game(values: values, enclosing: enclosing)

proc toGame2(data: seq[seq[char]]): Game2 =
    var values = initTable[(int, int, int, int), bool]()
    var enclosing: Table[int, seq[int]] = initTable[int, seq[int]]()
    enclosing[0] = @[-1, 1]
    enclosing[1] = @[-1, len(data)]
    enclosing[2] = @[-1, len(data[0])]
    enclosing[3] = @[-1, 1]
    for i, line in data:
        for j, c in line:
            values[(0, i, j, 0)] = c == '#'
    return Game2(values: values, enclosing: enclosing)

proc count_active(game: Game): int =
    for k in game.values.keys:
        if game.values[k] == true:
            result += 1
proc count_active(game: Game2): int =
    for k in game.values.keys:
        if game.values[k] == true:
            result += 1

proc display(game: Game): void =
    for i in game.enclosing[0][0]+1..game.enclosing[0][1]-1:
        echo "\nz=", i
        for j in game.enclosing[1][0]+1..game.enclosing[1][1]-1:
            for k in game.enclosing[2][0]+1..game.enclosing[2][1]-1:
                if game.values.getOrDefault((i, j, k)):
                    stdout.write "#"
                else:
                    stdout.write "."
            stdout.write "\n"

proc cell_should_change(game: var Game, i: int, j: int, k: int): bool =
    var active = 0
    for ii in i-1..i+1:
        for jj in j-1..j+1:
            for kk in k-1..k+1:
                if (ii != i or jj != j or kk != k) and game.values.getOrDefault((ii, jj, kk)):
                    active += 1
    if game.values.getOrDefault((i, j, k)):
        return active in [2, 3]
    else:
        return active == 3

proc cell_should_change(game: var Game2, i: int, j: int, k: int, w: int): bool =
    var active = 0
    for ii in i-1..i+1:
        for jj in j-1..j+1:
            for kk in k-1..k+1:
                for ww in w-1..w+1:
                    if (ii != i or jj != j or kk != k or ww != w) and game.values.getOrDefault((ii, jj, kk, ww)):
                        active += 1
    if game.values.getOrDefault((i, j, k, w)):
        return active in [2, 3]
    else:
        return active == 3

# Apply one time the rule
proc transform(game: var Game): void =
    #display(game.data)
    var newValues = game.values
    for i in game.enclosing[0][0]..game.enclosing[0][1]:
        for j in game.enclosing[1][0]..game.enclosing[1][1]:
            for k in game.enclosing[2][0]..game.enclosing[2][1]:
                newValues[(i, j, k)] = cell_should_change(game, i, j, k)
    game.values = newValues
    game.enclosing[0] = @[game.enclosing[0][0]-1, game.enclosing[0][1]+1]
    game.enclosing[1] = @[game.enclosing[1][0]-1, game.enclosing[1][1]+1]
    game.enclosing[2] = @[game.enclosing[2][0]-1, game.enclosing[2][1]+1]

proc transform(game: var Game2): void =
    var newValues = game.values
    for i in game.enclosing[0][0]..game.enclosing[0][1]:
        for j in game.enclosing[1][0]..game.enclosing[1][1]:
            for k in game.enclosing[2][0]..game.enclosing[2][1]:
                for w in game.enclosing[3][0]..game.enclosing[3][1]:
                    newValues[(i, j, k, w)] = cell_should_change(game, i, j, k, w)
    game.values = newValues
    game.enclosing[0] = @[game.enclosing[0][0]-1, game.enclosing[0][1]+1]
    game.enclosing[1] = @[game.enclosing[1][0]-1, game.enclosing[1][1]+1]
    game.enclosing[2] = @[game.enclosing[2][0]-1, game.enclosing[2][1]+1]
    game.enclosing[3] = @[game.enclosing[3][0]-1, game.enclosing[3][1]+1]

    
proc sol1(game: var Game): int =
    for i in 1..6:
        game.transform()
    return game.count_active()

proc sol2(game: var Game2): int =
    for i in 1..6:
        game.transform()
    return game.count_active()

var testGame = test.toGame
assert sol1(testGame) == 112
var game = data.toGame
dump sol1(game)


var testGame2 = test.toGame2
assert sol2(testGame2) == 848
var game2 = data.toGame2
dump sol2(game2)