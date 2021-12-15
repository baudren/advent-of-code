import numpy as np

class Node:
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
    
    def __eq__(self, other):
        return self.position == other.position
    def __repr__(self):
        return f"{self.position}"
    def __hash__(self): return hash(self.position)


def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = 0
    end_node.h = end_node.f = maze[end]

    open_set = set()
    open_set.add(start_node)
    closed_set = set()

    while len(open_set) > 0:
        current_node = next(iter(open_set))
        for item in open_set:
            if item.g < current_node.g:
                current_node = item

        closed_set.add(current_node)
        open_set.remove(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            score = current_node.parent.g+maze[current_node.position]
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], score

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            children.append(Node(current_node, node_position))

        for child in children:
            if child in closed_set or child in open_set:
                continue

            child.g = child.parent.g + maze[child.position]
            child.h = (end_node.position[0] - child.position[0]) + (end_node.position[1] - child.position[1])
            child.f = child.g + child.h

            open_set.add(child)


def sol1(data):
    path, cost = astar(data, (0, 0), (len(data)-1, len(data)-1))
    return cost

def sol2(data):
    data1 = np.where(data + 1 > 9, 1, data + 1)
    data2 = np.where(data1 + 1 > 9, 1, data1 + 1)
    data3 = np.where(data2 + 1 > 9, 1, data2 + 1)
    data4 = np.where(data3 + 1 > 9, 1, data3 + 1)
    row = np.concatenate((
        data, 
        data1,
        data2,
        data3,
        data4
        ), axis=1)
    row1 = np.where(row+1>9, 1, row+1)
    row2 = np.where(row1+1>9, 1, row1+1)
    row3 = np.where(row2+1>9, 1, row2+1)
    row4 = np.where(row3+1>9, 1, row3+1)
    data = np.concatenate((
        row, 
        row1,
        row2,
        row3,
        row4
        ), axis=0)
    path, cost = astar(data, (0, 0), (len(data)-1, len(data)-1))
    return cost


if __name__ == "__main__":
    data = np.array([int(e) for f in open('day15.txt').readlines() for e in f.strip()]).reshape(100,100)
    test = np.array([int(e) for f in """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split("\n") for e in f]).reshape(10,10)
    assert sol1(test) == 40
    print(sol1(data))
    assert sol2(test) == 315
    print(sol2(data))