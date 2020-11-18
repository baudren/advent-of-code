import string
from time import time
maze = [list(a.strip()) for a in open('data.txt', 'r').readlines()]

class NodeExploration:

    def __init__(self, parent, key, length, pos):
        self.parent = parent
        self.key = key
        self.pos = pos
        self.length = length
        self.f = self.g = self.h = 0

    def path_length(self):
        length = 1
        current = self
        while True:
            if current.parent is not None:
                current = current.parent
                length += 1
            else:
                break
        return length

    def path(self):
        path = self.key
        cur = self
        while cur.parent:
            path += cur.parent.key
            cur = cur.parent
        return path[::-1]

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        self.key == other.key and self.length == other.length

    def __str__(self):
        return f"{self.key}, {self.f}, {self.parent.key}, {self.length}, {self.path_length()}"

    def __repr__(self):
        return self.__str__()


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        if self.parent is not None:
            return f"{self.position}, {self.g}, {self.f}, {self.h}, parent: {self.parent.position}"
        else:
            return f"{self.position}"#, {self.g}, {self.f}, {self.h}"

    def __repr__(self):
        return self.__str__()


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = [start_node]
    closed_list = []

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0

        # Find if there's a better fit
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares but no diagonals

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # No need to check if outside boundaries, because the maze is bounded

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] in ['#', *list(string.ascii_uppercase)]:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

def find_keys(maze):
    keys = {}
    possible_keys = list(string.ascii_lowercase)
    for i, line in enumerate(maze):
        for j, elem in enumerate(line):
            if elem in possible_keys:
                keys[elem] = (i, j)
    return keys

def find_entrance(maze):
    for i, line in enumerate(maze):
        for j, elem in enumerate(line):
            if elem == "@":
                return (i, j)

# Get the available keys
def get_available_keys(maze, node, pos=None):
    if node is not None:
        pos = node.pos
        excluded_keys = [node.key]
        current_node = node
        while current_node.parent is not None:
            current_node = current_node.parent
            excluded_keys.append(current_node.key)
    else:
        excluded_keys = []
    excluded_upper = [e.upper() for e in excluded_keys]
    available_keys = {}
    paths = {}
    # Flood
    open_nodes = [Node(None, pos)]
    closed_nodes = []
    explored = []
    index = 0
    while True:
        index += 1
        for i, node in enumerate(open_nodes):
            explored.append(node.position)
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares but no diagonals

                # Get node position
                node_position = (node.position[0] + new_position[0], node.position[1] + new_position[1])
                # if going back: stop
                if node_position in explored or node_position in [e.position for e in closed_nodes]:
                    continue

                # No need to check if outside boundaries, because the maze is bounded
                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] in ['#', *list(string.ascii_uppercase)] and maze[node_position[0]][node_position[1]] not in excluded_upper:
                    continue

                if maze[node_position[0]][node_position[1]] in list(string.ascii_lowercase) and maze[node_position[0]][node_position[1]] not in excluded_keys:
                    available_keys[maze[node_position[0]][node_position[1]]] = index
                    path = []
                    current = Node(node, node_position)
                    while current is not None:
                        path.append(current.position)
                        current = current.parent
                    paths[maze[node_position[0]][node_position[1]]] = path[::-1] # Return reversed path

                # Append
                children.append(Node(node, node_position))
            closed_nodes.extend(children)
        if not closed_nodes:
            break
        else:
            open_nodes = closed_nodes.copy()
            closed_nodes.clear()

    return available_keys, paths

def astar_mod(maze):
    start = find_entrance(maze)
    keys = find_keys(maze)
    complete = set()
    open_nodes = []
    available_keys, paths = get_available_keys(maze, None, start)
    for key in available_keys:
        new_pos = keys[key]
        node = NodeExploration(None, key, available_keys[key], new_pos)
        node.g = (26-1)**1
        node.f = node.g + node.length
        open_nodes.append(node)
    while open_nodes:
        #for node in open_nodes:
        #    print(node.path())
        #print()
        #input()
        # Get the current best node
        current_node = open_nodes[0]
        current_index = 0

        # Find if there's a better fit
        for index, item in enumerate(open_nodes):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # if current_node.parent:
        #     print(current_node)
        # Pop current off open list
        open_nodes.pop(current_index)
        #if (current_node.path() == "ba"): input()
        # Found the goal
        if current_node.path_length() == 26:
            # check if node not already there
            found = False
            for c in complete:
                if c.key == current_node.key and c.length == current_node.length:
                    found = True
                    break
            if not found:
                complete.add(current_node)
                print(current_node)
            if len(complete) == 100:
                break
        else:
            available_keys, paths = get_available_keys(maze, current_node)
            #if (current_node.path() == "ba"): print(available_keys)
            for key in available_keys:
                new_pos = keys[key]
                node = NodeExploration(current_node, key, current_node.length+available_keys[key], new_pos)
                node.g = (26-node.path_length())**1
                node.f = node.g+node.length
                # Add the child to the open list if not already there
                found = False
                for e in open_nodes:
                    if e.path() == node.path():
                        found = True
                        break
                if not found:
                    open_nodes.append(node)
    return complete

complete = astar_mod(maze)
min_ = 10000
for node in complete:
    if node.length < min_:
        min_node = node
        min_ = node.length
print(complete)
print(min_)
print(min_node.path())