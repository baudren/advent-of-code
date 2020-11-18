import itertools
import numpy as np
from pprint import pprint

program = [int(e) for e in open('data.txt', 'r').read().split(',')]

actions = {
    1: 'add',
    2: 'multiply',
    3: 'read_i',
    4: 'write_o',
    5: 'jump_if_true',
    6: 'jump_if_false',
    7: 'less_than',
    8: 'equals',
    9: 'change_offset',
    99: 'break',
}


class ScanningDroid:

    def __init__(self, program):
        self.program = program.copy()
    
    def scan(self):
        affected = 0
        for x in range(50):
            for y in range(50):
                output = []
                run_sequence(self.program.copy(), output, [x, y], 0, 0)
                affected += output[0]
        return affected

    def print(self, start, end):
        size = end-start
        screen = np.zeros((size, size), dtype=int)
        for x in range(start, end):
            for y in range(start, end):
                output = []
                run_sequence(self.program.copy(), output, [x, y], 0, 0)
                screen[x-start, y-start] = output[0]
        print('\n'.join([''.join([str(f) for f in e]) for e in screen]))


    def search_for_santa(self):
        x, y = 37, 49
        moving_right = True
        ones = set()
        last = 0, 0
        length = 0
        potential = 0, 0
        while True:
            output = []
            print(x, y)
            run_sequence(self.program.copy(), output, [x, y], 0, 0)
            # Keeping track
            if output[0] == 1:
                ones.add((x, y))
                last = (x, y)
                length = 0
            
            if moving_right and (x, y-100) in ones:
                if potential != (0, 0):
                    potx, poty = potential
                    if (potx-100, poty) in ones:
                        return (potx-100, poty)
                else:
                    potential = x, y
                    y = y-100
                    moving_right = False
                    input()
                    continue
            elif not moving_right and (x-100, y) in ones:
                if potential != (0, 0):
                    potx, poty = potential
                    if (potx, poty-100) in ones:
                        return (potx, poty-100)
                else:
                    potential = x, y
                    x = x-100
                    moving_right = True
                    input()
                    continue

            if output[0] == 0:
                moving_right = not moving_right
                length += 1
                #print("Was moving right?", not moving_right)
                #print(length)
                if length > 1:
                    x, y = last[0]-1, last[1]-1
                    length = 0
                #input()

            # increment
            if moving_right:
                y += 1
            else:
                x += 1

            
class Opcode:

    def __init__(self, opcode, index, offset):
        self.opcode = opcode
        self.offset = offset
        self.is_finished = False
        self.is_waiting = False
        if opcode < 100:
            self.action = actions[opcode]
            self.parameter_modes = [0, 0, 0]
        else:
            self.action = actions[int(str(opcode)[-2:])]
            self.parameter_modes = [int(e) for e in str(opcode)[-3::-1]]
        if self.action in ['add', 'multiply', 'less_than', 'equals']:
            self.next_index = index+4
        else:
            self.next_index = index+2
        while len(self.parameter_modes) < 3:
            self.parameter_modes.append(0)

    def act(self, program, input, index) -> int:
        if self.action in ['add', 'multiply', 'less_than', 'equals']:
            value_a = self.get_index_with_parameter(program, index+1, self.parameter_modes[0])
            value_b = self.get_index_with_parameter(program, index+2, self.parameter_modes[1])
            offset = self.offset if self.parameter_modes[2] == 2 else 0
            if self.action == 'add':
                program[program[index+3]+offset] = value_a + value_b
            elif self.action == 'multiply':
                program[program[index+3]+offset] = value_a * value_b
            elif self.action == 'less_than':
                program[program[index+3]+offset] = 1 if value_a < value_b else 0
            elif self.action == 'equals':
                program[program[index+3]+offset] = 1 if value_a == value_b else 0
            if program[index+3]+offset == index:
                self.next_index = index
        elif self.action == 'read_i':
            if not input:
                self.is_waiting = True
                return
            offset = self.offset if self.parameter_modes[0] == 2 else 0
            program[program[index+1]+offset] = input.pop(0)
            if program[index+1]+offset == index:
                self.next_index = index
        elif self.action == 'write_o':
            if self.parameter_modes[0] == 0:
                return(program[program[index+1]])
            elif self.parameter_modes[0] == 1:
                return(program[index+1])
            else:
                return(program[program[index+1]+self.offset])
        elif self.action == 'change_offset':
            self.offset += self.get_index_with_parameter(program, index+1, self.parameter_modes[0])
        elif self.action in ['jump_if_true', 'jump_if_false']:
            self.next_index = index+3
            value = self.get_index_with_parameter(program, index+1, self.parameter_modes[0])
            if (value != 0 and self.action == 'jump_if_true') or (value == 0 and self.action == 'jump_if_false'):
                self.next_index = self.get_index_with_parameter(program, index+2, self.parameter_modes[1])
        else:
            self.is_finished = True

    def get_index_with_parameter(self, program, index, parameter):
        if parameter == 0:
            return program[program[index]]
        elif parameter == 1:
            return program[index]
        elif parameter == 2:
            return program[program[index]+self.offset]

    def __str__(self):
        return "%s, %s, %s" % (str(self.opcode), self.action, self.parameter_modes)

def run_sequence(program, output, input, index=0, offset=0):
    while True:
        opcode = Opcode(program[index], index, offset)
        value = opcode.act(program, input, index)
        if value is not None:
            output.append(value)
        if opcode.is_finished:
            return output, True, True
        elif opcode.is_waiting:
            return output, index, offset
        else:
            index = opcode.next_index
            offset = opcode.offset


def expand(program):
    p_e = [0 for _ in range(10*len(program))]
    p_e[:len(program)] = program
    return p_e, program

expanded, program = expand(program)
#number_of_steps = 318 -> how to find it automatically? implement breadth-first search...
robot = ScanningDroid(expanded)
#print(robot.scan())
#robot.print(90, 160)
print(robot.search_for_santa())