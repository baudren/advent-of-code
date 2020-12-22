import strutils, sugar, tables, sequtils, re, algorithm

let test = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".splitLines
let data = readFile("data.txt").splitLines

type
    Player = object
        cards: seq[int]
    Game = object
        players: seq[Player]
        winner: int
        played_hands: seq[(seq[int], seq[int])]

proc toGame(data: seq[string]): Game =
    var (a, b) = (Player(cards: @[]), Player(cards: @[]))
    var first = true
    for line in data:
        if line == "":
            first = false
        elif not line.startsWith("Player"):
            if first:
                a.cards.add(line.parseInt)
            else:
                b.cards.add(line.parseInt)
    return Game(players: @[a, b], played_hands: @[])

proc playRound(game: var Game): bool =
    let (a, b) = (game.players[0].cards[0], game.players[1].cards[0])
    game.players[0].cards.delete(0)
    game.players[1].cards.delete(0)
    if a > b:
        game.players[0].cards.add(@[a, b])
        if game.players[1].cards.len == 0:
            game.winner = 0
            return true
    else:
        game.players[1].cards.add(@[b, a])
        if game.players[0].cards.len == 0:
            game.winner = 1
            return true
    return false

proc playRecRound(game: var Game): bool =
    # Prevent infinite play
    for played in game.played_hands:
        if game.players[0].cards == played[0] and game.players[1].cards == played[1]:
            game.winner = 0
            return true
    game.played_hands.add((game.players[0].cards, game.players[1].cards))
    let (a, b) = (game.players[0].cards[0], game.players[1].cards[0])
    game.players[0].cards.delete(0)
    game.players[1].cards.delete(0)
    if a <= game.players[0].cards.len and b <= game.players[1].cards.len:
        var (p1rec, p2rec) = (Player(cards: game.players[0].cards[0..<a]), Player(cards: game.players[1].cards[0..<b]))
        var subGame = Game(players: @[p1rec, p2rec], played_hands: @[])
        while true:
            if subGame.playRecRound():
                break
        if subGame.winner == 0:
            game.players[0].cards.add(@[a, b])
            if game.players[1].cards.len == 0:
                game.winner = 0
                return true
        else:
            game.players[1].cards.add(@[b, a])
            if game.players[0].cards.len == 0:
                game.winner = 1
                return true
    else:
        if a > b:
            game.players[0].cards.add(@[a, b])
            if game.players[1].cards.len == 0:
                game.winner = 0
                return true
        else:
            game.players[1].cards.add(@[b, a])
            if game.players[0].cards.len == 0:
                game.winner = 1
                return true


proc sol1(game: var Game): int =
    while true:
        if game.playRound():
            break
    for i, value in game.players[game.winner].cards.reversed:
        result += value*(i+1)

proc sol2(game: var Game): int =
    while true:
        if game.playRecRound():
            break
    for i, value in game.players[game.winner].cards.reversed:
        result += value*(i+1)

var testGame = test.toGame
assert testGame.sol1 == 306
var game = data.toGame
dump game.sol1

testGame = test.toGame
assert testGame.sol2 == 291
game = data.toGame
dump game.sol2