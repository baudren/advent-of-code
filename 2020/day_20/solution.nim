import strutils
import sugar
import tables
import sequtils
import algorithm

let test = readFile("test.txt").splitLines
let data = readFile("data.txt").splitLines
let monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.splitLines
var monster_pairs: seq[(int, int)] = @[]
for row, line in monster:
    for col, c in line:
        if c == '#':
            monster_pairs.add((row, col))

type
    Tile = object
        id: int
        image: seq[string]
        borders: seq[int]

proc toBinary(str: string): int =
    return str.replace('#', '1').replace('.', '0').parseBinInt

proc inv(a: int): int =
    return a.toBin(10).reversed.join("").parseBinInt

proc toTiles(data: seq[string]): seq[Tile] =
    var tiles: seq[Tile] = @[]
    var tile: Tile = Tile(id: 0, image: @[], borders: @[])
    for line in data:
        if line.startsWith("Tile"):
            tile.id = line.split(" ")[1][0..^2].parseInt
        elif line != "":
            tile.image.add(line)
        else:
            # top
            let (t, r) = (tile.image[0].toBinary, tile.image.mapIt(it[^1]).join("").toBinary)
            let (b, l) = (tile.image[^1].toBinary, tile.image.mapIt(it[0]).join("").toBinary)
            tile.borders.add(@[t, r, b.inv, l.inv, t.inv, r.inv, b, l])
            tiles.add(tile)
            tile = Tile(id: 0, image: @[])
    let (t, r) = (tile.image[0].toBinary, tile.image.mapIt(it[^1]).join("").toBinary)
    let (b, l) = (tile.image[^1].toBinary, tile.image.mapIt(it[0]).join("").toBinary)
    tile.borders.add(@[t, r, b.inv, l.inv, t.inv, r.inv, b, l])
    tiles.add(tile)
    return tiles

proc flip(tile: var Tile, vertical: bool): void =
    var image: seq[string] = @[]
    let t = tile.borders
    if vertical:
        for line in tile.image:
            image.add(line.reversed.join(""))
        tile.image = image
        tile.borders = @[t[0].inv, t[3].inv, t[2].inv, t[1].inv, t[0], t[3], t[2], t[1]]
    else:
        tile.image.reverse
        tile.borders = @[t[2].inv, t[1].inv, t[0].inv, t[3].inv, t[2], t[1], t[0], t[3]]

proc rot(tile: var Tile, right: bool): void =
    var image: seq[string] = @[]
    let t = tile.borders
    for i in 0..<tile.image.len:
        var newLine: seq[char]
        for line in tile.image:
            if right:
                newLine.add(line[i])
            else:
                newLine.add(line[tile.image.len-1-i])
        if right:
            newLine.reverse
        image.add(newLine.join(""))
        if right:
            tile.borders = @[t[3], t[0], t[1], t[2], t[3].inv, t[0].inv, t[1].inv, t[2].inv]
        else:
            tile.borders = @[t[1], t[2], t[3], t[0], t[1].inv, t[2].inv, t[3].inv, t[0].inv]
    tile.image = image

proc rot(data: seq[string]): seq[string] =
    for i in 0..<data.len:
        var newLine: seq[char]
        for line in data:
            newLine.add(line[i])
        result.add(newLine.reversed.join(""))

proc flip(data: seq[string]): seq[string] =
    for line in data:
        result.add(line.reversed.join(""))

proc sol1(tiles: seq[Tile]): int64 =
    var corners: seq[Tile] = @[]
    for i, tile in tiles:
        var found: int = 0
        for border in tile.borders[0..3]:
            for j, tileb in tiles:
                if j != i:
                    if border in tileb.borders:
                        found += 1
        if found == 2:
            corners.add(tile)
    return corners.mapIt(it.id).foldl(a*b)

proc reconstruct(tiles: seq[Tile]): seq[string] =
    var positions: Table[(int, int), Tile] = initTable[(int, int), Tile]()
    for i, tile in tiles:
        var found: seq[int]
        for k, border in tile.borders[0..3]:
            for j, tileb in tiles:
                if j != i:
                    if border in tileb.borders:
                        found.add(k)
                        break
        var tile = tile
        if found.len == 2 and positions.len == 0:
            if 0 in found and 1 in found:
                tile.flip(false)
            elif 2 in found and 3 in found:
                tile.flip(true)
            elif 0 in found and 3 in found:
                tile.flip(true)
                tile.flip(false)
            positions[(0, 0)] = tile
    # One corner set, trying to set all the top line
    var (row, col) = (0, 0)
    var (row_count, col_count) = (0, 0)
    var fitted: seq[int] = @[positions[(0, 0)].id]
    # rows
    while true:
        while true:
            var found: bool = false
            for tile in tiles:
                if tile.id notin fitted:
                    if positions[(row, col)].borders[1] in tile.borders:
                        var tile = tile
                        var rot: int = 0
                        var flipped: bool = false
                        while true:
                            if tile.borders[3].inv == positions[(row, col)].borders[1]:
                                break
                            elif rot < 3 or flipped:
                                tile.rot(true)
                                rot += 1
                            else:
                                tile.flip(true)
                                flipped = true
                        positions[(row, col+1)] = tile
                        fitted.add(tile.id)
                        found = true
                        break
            if found:
                col += 1
                continue
            else:
                # add the row+1, 0 tile
                col_count = col + 1
                if fitted.len < tiles.len:
                    for tile in tiles:
                        if tile.id notin fitted:
                            if positions[(row, 0)].borders[2] in tile.borders:
                                var tile = tile
                                var rot: int = 0
                                var flipped: bool = false
                                while true:
                                    if tile.borders[0].inv == positions[(row, 0)].borders[2]:
                                        break
                                    elif rot < 3 or flipped:
                                        tile.rot(true)
                                        rot += 1
                                    else:
                                        tile.flip(true)
                                        flipped = true
                                positions[(row+1, 0)] = tile
                                fitted.add(tile.id)
                col = 0
                row += 1
                break
        if fitted.len == tiles.len:
            row_count = row
            break
    # merge the images
    for row in 0..<row_count:
        var lines: seq[string] = @[]
        for i in 1..8:
            lines.add(positions[(row, 0)].image[i][1..8].join(""))
        for col in 1..<col_count:
            for i in 1..8:
                lines[i-1] = lines[i-1] & positions[(row, col)].image[i][1..8].join("")
        result.add(lines)


proc sol2(image: seq[string]): int =
    var image = image
    var found: seq[(int, int)] = @[]
    var rot: int = 0
    var flipped: bool = false      
    while found == @[]:
        for row, line in image:
            for col, c in line:
                if col < line.len - monster[0].len - 1 and row < line.len - monster.len - 1:
                    var loch_ness: bool = true
                    for pair in monster_pairs:
                        if image[row+pair[0]][col+pair[1]] != '#':
                            loch_ness = false
                            break
                    if loch_ness:
                        found.add((row, col))
        if rot < 3 or flipped:
            image = image.rot()
            rot += 1
        else:
            image = image.flip()
            flipped = true
    return image.join("").count("#") - found.len * monster.join("").count("#")


var testTiles = test.toTiles
assert sol1(testTiles) == 20899048083289

var dataTiles = data.toTiles
dump sol1(dataTiles)

let testImage = reconstruct(testTiles)
assert sol2(testImage) == 273

let image = reconstruct(dataTiles)
dump sol2(image)