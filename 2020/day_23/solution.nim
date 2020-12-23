import strutils, sugar, tables, sequtils, lists

let test = "389125467"
let data = "284573961"

proc sol1(data: string, moves: int): string =
    var cards: seq[int] = toSeq(data.items).mapIt(parseInt($it))
    let length = cards.len
    var to_move: seq[int] = @[]
    var target: int
    var head: int = cards[0]
    var head_index: int
    for i in 1..moves:
        to_move = @[]
        head_index = cards.find(head)
        for j in head_index+1..head_index+3:
            if j >= length:
                to_move.add(cards[0])
                cards.delete(0)
            else:
                to_move.add(cards[(head_index+1) mod cards.len])
                cards.delete((head_index+1) mod cards.len)
        # find the target
        target = -1
        for j in countdown(head-1, 1):
            if j in cards:
                target = cards.find(j)
                break
        if target == -1:
            for j in countdown(9, 1):
                if j in cards:
                    target = cards.find(j)
                    break
        if target < cards.len - 1:
            cards = cards[0..target] & to_move & cards[target+1..^1]
        else:
            cards = cards & to_move
        to_move = @[]
        head_index = cards.find(head)
        head_index = (head_index + 1) mod cards.len
        head = cards[head_index]
    let index_1 = cards.find(1)
    return cards[index_1+1..^1].join("") & cards[0..<index_1].join("")

proc sol2(data: string, moves: int): int =
    var
        l = initSinglyLinkedRing[int]()
        nodes: Table[int, SinglyLinkedNode[int]]
        head: SinglyLinkedNode[int]
    let length = 1_000_000

    for i, card in toSeq(data.items).mapIt(parseInt($it)):
        var a = newSinglyLinkedNode[int](card)
        l.append(a)
        nodes[card] = a
        if i == 0:
            head = a
    for i in 10..length:
        var a = newSinglyLinkedNode[int](i)
        l.append(a)
        nodes[i] = a
    var to_move: seq[int] = @[]
    var target: int
    var 
        node_to_move: SinglyLinkedNode[int]
    for i in 1..moves:
        node_to_move = head.next
        to_move = @[]
        to_move.add(head.next.value)
        to_move.add(head.next.next.value)
        to_move.add(head.next.next.next.value)
        head.next = head.next.next.next.next
        target = -1
        for j in countdown(head.value-1, 1):
            if j notin to_move:
                target = j
                break
        if target == -1:
            for j in countdown(length, head.value):
                if j notin to_move:
                    target = j
                    break
        node_to_move.next.next.next = nodes[target].next
        nodes[target].next = node_to_move
        head = head.next
    return nodes[1].next.value * nodes[1].next.next.value

assert test.sol1(10) == "92658374"
assert test.sol1(100) == "67384529"
dump data.sol1(100)
dump data.sol2(10_000_000)