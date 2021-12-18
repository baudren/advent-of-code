from math import floor, ceil


class Node:
    def __init__(self, data, depth=0):
        self.data = data
        self.depth = depth
        self.left = self.right = None
        self.value = None
        if '[' in data:
            left, right = parse(data)
            self.left = Node(left, depth+1)
            self.right = Node(right, depth+1)
            self.is_simple = False
        else:
            self.is_simple = True
            self.value = int(data)
    
    def __repr__(self):
        if self.value is None:
            return f"[{self.left},{self.right}]"
        else:
            return f"{self.value}"

    def cleanup(self):
        action = True
        while action:
            action = self.explode()
            if not action:
                action = self.split()


    def mag(self):
        if self.value is not None:
            return self.value
        else:
            return 3*self.left.mag()+2*self.right.mag()

    def explode(self):
        explored = []
        index = self.explode_rec(explored, -1)
        if index != -1:
            if index >= 1:
                explored[index-1].value += explored[index].old_left
            if index < len(explored)-1:
                explored[index+1].value += explored[index].old_right
        return index != -1
    
    def explode_rec(self, explored, index):
        if self.is_simple:
            explored.append(self)
            return index
        else:
            if self.right.is_simple and self.left.is_simple and self.depth >= 4:
                if index == -1:
                    self.old_left = self.left.value
                    self.old_right = self.right.value
                    self.right = None
                    self.left = None
                    self.value = 0
                    self.is_simple = True
                    index = len(explored)
                    explored.append(self)
                    return index
            index = self.left.explode_rec(explored, index)
            index = self.right.explode_rec(explored, index)
        return index

    def split(self):
        splitted = self.split_rec()
        return splitted
        
    def split_rec(self):
        if self.value is not None and self.value > 9:
            self.left = Node(f"{floor(self.value/2)}", self.depth + 1)
            self.right = Node(f"{ceil(self.value/2)}", self.depth + 1)
            self.value = None
            self.is_simple = False
            return True
        elif self.value is not None:
            return False
        else:
            splitted = self.left.split_rec()
            if not splitted:
                splitted = self.right.split_rec()
            return splitted

def parse(string):
    depth = 0
    left = ""
    right = ""
    left_finished = False
    for c in string:
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        if c == "," and depth == 1:
            left_finished = True
        elif left_finished:
            right += c
        else:
            left += c
    return left[1:], right[:-1]

def sol1(data):
    p = Node(data[0])
    for line in data[1:]:
        p = add(p, line)
        p.cleanup()
    return p.mag()

def sol2(data):
    max_ = 0
    for index, line in enumerate(data):
        for j, otherline in enumerate(data):
            if j != index:
                p = Node(line)
                p = add(p, otherline)
                p.cleanup()
                mag = p.mag()
                if mag > max_:
                    max_ = mag
    return max_

def add(pair, other):
    return Node(f"[{pair},{other}]")


if __name__ == "__main__":
    data = [e.strip() for e in open('day18.txt', 'r').readlines()]
    assert sol1("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split("\n")) == 4140
    print(sol1(data))
    assert sol2("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split("\n")) == 3993
    print(sol2(data))
