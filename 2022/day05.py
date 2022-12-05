from rich import print
from utils import load, file_to_lines, file_to_ints
from pprint import pprint

class Stacks:

    def __init__(self, initial):
        self.size = int(initial.split("\n")[-1].strip().split(" ")[-1])
        self.columns = {k+1:[] for k in range(self.size)}
        stacks = initial.split("\n")[:-1]
        for k in range(self.size):
            for l in range(len(stacks)):
                if stacks[l][k*4+1:k*4+2].strip():
                    self.columns[k+1].append(stacks[l][k*4+1:k*4+2])
        for k in range(self.size):
            self.columns[k+1].reverse()
    
    def move(self, moves):
        for move in moves:
            quantity = int(move.split(" from ")[0].split(" ")[1])
            initial = int(move.split(" from ")[1].split(" to ")[0])
            destination = int(move.split(" from ")[1].split(" to ")[1])
            for k in range(quantity):
                self.columns[destination].append(self.columns[initial].pop())
    
    def move_9001(self, moves):
        for move in moves:
            quantity = int(move.split(" from ")[0].split(" ")[1])
            initial = int(move.split(" from ")[1].split(" to ")[0])
            destination = int(move.split(" from ")[1].split(" to ")[1])
            self.columns[destination].extend(self.columns[initial][-quantity:])
            for _ in range(quantity):
                self.columns[initial].pop()

    def top(self):
        result = ""
        for k in range(self.size):
            result += self.columns[k+1][-1]
        return result


def sol1(a):
    initial, move_list = a.split("\n\n")
    moves = move_list.split("\n")
    stacks = Stacks(initial)
    stacks.move(moves)
    return stacks.top()


def sol2(a):
    initial, move_list = a.split("\n\n")
    moves = move_list.split("\n")
    stacks = Stacks(initial)
    stacks.move_9001(moves)
    return stacks.top()


asserts_sol1 = {
        """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""": "CMZ"
        }

asserts_sol2 = {
        """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""": "MCD"
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
