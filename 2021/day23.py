parking = (0,1,3,5,7,9,10)

costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

target = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

def state_to_str(state):
    flat = ""
    for j in (2, 4, 6, 8):
        flat += "".join([state.get((i, j), ".") for i in range(1, 5)])
    flat += "".join([state.get((0, j), ".") for j in parking])
    return flat

def str_to_state(str_):
    state = {}
    for j in (2, 4, 6, 8):
        for i in range(1, 5):
            elem = str_[i-1+(j-2)//2*4]
            if elem != '.':
                state[(i, j)] = elem 
    for i, j in enumerate(parking):
        elem = str_[16+i]
        if elem != '.':
            state[(0, j)] = elem
    return state


def parse(data):
    state = {}
    for j in (2, 4, 6, 8):
        for a in range(1, 5):
            state[(a, j)] = data[a+1][j+1]
    return state


def print_state(state):
    grid = []
    for i in range(5):
        line = ""
        for j in range(11):
            line += state.get((i, j), " " if i != 0 and (j < 2 or j > 8) else ".")
        grid.append(line)
    print()
    for line in grid:
        print(line)
    print()


def distance(state):
    # distance of a sorted board should be 0
    distance = 0
    for pos, char in state.items():
        if pos[1] != target[char]:
            distance += costs[char]*(abs(pos[1]-target[char]) + 1 + pos[0])  # assume you only need to enter the room
    return distance


class Node:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.str_ = state_to_str(state)
    
    def __eq__(self, other):
        return self.str_ == other.str_
    def __repr__(self):
        return f"{self.str_}"
    def __hash__(self): return hash(self.str_)


def astar(start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_str = state_to_str(end)
    open_set = set()
    open_set.add(start_node)
    closed_set = set()
    index = 0
    while len(open_set) > 0:
        index += 1
        current_node = next(iter(open_set))
        for item in open_set:
            if item.f < current_node.f:
                current_node = item
        
        if index % 1000 == 0:
            print(f"Current cost and distance: {current_node.g}, {current_node.f}")
            print_state(current_node.state)
        closed_set.add(current_node)
        open_set.remove(current_node)

        if current_node.str_ == end_str:
            print("Found the end!!")
            score = current_node.g
            path = []
            while current_node.parent is not None:
                path.append(current_node.state)
                current_node = current_node.parent
            return score, path[::-1]

        children = []
        state = dict(current_node.state)
        # Get all the movable chars inside rooms that are not at their right place
        can_move = []
        for j in (2, 4, 6, 8):
            for i in range(1, 5):
                if (i, j) in state:
                    # If in the right place, check if below is correct
                    if target[state[(i, j)]] == j:
                        if any([state[(k, j)] != state[(i, j)] for k in range(i+1, 5)]):
                            can_move.append((i, j))
                    else:
                        can_move.append((i, j))
                    break # Don't check below

        # Search all the possible room to room
        for i, j in can_move:
            coord, cost = find_destination(i, j, state)
            if coord is not None:
                new_state = dict(state)
                new_state[coord] = new_state.pop((i, j))
                children.append((Node(current_node, new_state), cost))
        # Search all the possible parking to room
        for j in parking:
            if (0, j) in state:
                coord, cost = find_destination(0, j, state)
                if coord is not None:
                    new_state = dict(state)
                    new_state[coord] = new_state.pop((0, j))
                    children.append((Node(current_node, new_state), cost))
        # Search all the possible room to parking
        for i, j in can_move:
            for k in parking:
                if (0, k) not in state:
                    # It's free, check if it's blocked
                    for u in range(min(k, j)+1, max(k, j)):
                        if (0, u) in state:
                            break
                    else:
                        new_state = dict(state)
                        new_state[(0, k)] = new_state.pop((i, j))
                        children.append((Node(current_node, new_state), costs[state[(i, j)]]*(i+abs(k-j))))

        for child, cost in children:
            child.g = child.parent.g + cost
            child.h = distance(child.state)
            child.f = child.g + 500*child.h

            open_set.add(child)
        if index == 1:
            #exit()
            pass
        

def find_destination(i, j, state):
    dest_coord, dest_cost = None, None
    char = state[(i, j)]
    if (1, target[char]) not in state and all([state.get((k, target[char]), char) == char for k in range(1, 5)]):
        # Find actual destination
        dest = 1
        for k in range(1, 5):
            if (k, target[char]) in state:
                dest = k - 1
                break
        else:
            dest = 4
        # Check if blocked
        # lateral movement
        for k in range(min(target[char], j)+1, max(target[char], j)):
            if (0, k) in state:
                break
        else:
            dest_coord = (dest, target[char]) 
            dest_cost = costs[char]*(i+dest+abs(j-target[char]))
    return dest_coord, dest_cost

def sol(data):
    start = parse(data.split("\n"))
    #print_state(start)
    #start = str_to_state("AAAABBBBCCCC.DDD......D")
    #start = end
    end = str_to_state("AAAABBBBCCCCDDDD.......")
    cost, path = astar(start, end)
    for state in path:
        print_state(state)
    return cost


if __name__ == "__main__":
    #assert sol("""#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########""") == 44169
  print(sol("""#############
#...........#
###B#B#C#D###
  #D#C#B#A#
  #D#B#A#C#
  #D#A#A#C#
  #########
"""))
