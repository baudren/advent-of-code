import itertools

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

class PaintingRobot:

    def __init__(self, program, image_mode=False):
        self.position = (0, 0)
        self.painted = set()
        self.panel = {}
        self.input = []
        self.output = []
        self.direction = [0, 1]
        self.index = 0
        self.offset = 0
        self.program = program.copy()
        if image_mode:
            self.panel[self.position] = 1
    
    def run(self):
        while True:
            self.read_paint_color()
            output, cur_index, cur_offset = run_sequence(self.program, self.output, self.input, self.index, self.offset)
            if cur_index is not True:
                self.index = cur_index
                self.offset = cur_offset
                self.paint_and_move()
            else:
                break
        return self.panel, self.painted
    
    def read_paint_color(self):
        self.input.append(self.panel.get(self.position, 0))
    
    def paint_and_move(self):
        self.panel[self.position] = self.output.pop(0)
        self.painted.add(self.position)
        turn = self.output.pop()
        if self.direction[0] != 0:
            self.direction[1] = self.direction[0] if turn == 0 else -self.direction[0]
            self.direction[0] = 0
        elif self.direction[1] != 0:
            self.direction[0] = -self.direction[1] if turn == 0 else self.direction[1]
            self.direction[1] = 0
        self.position = (self.position[0]+self.direction[0], self.position[1]+self.direction[1])



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
robot = PaintingRobot(expanded.copy(), image_mode=False)
panel, painted = robot.run()

print(len(panel))

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def print_panel(panel):
    keys = panel.keys()
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for key in keys:
        if key[0] < min_x:
            min_x = key[0]
        if key[0] > max_x:
            max_x = key[0]
        if key[1] < min_y:
            min_y = key[1]
        if key[1] > max_y:
            max_y = key[1]
    w = max_x - min_x + 1
    h = max_y - min_y+1
    image = np.zeros((h, w))
    for key in keys:
        image[h-(key[1]+h-1)-1, key[0]] = 255 if panel[key] == 1 else 0
    plt.imshow(image)
    plt.show()

robot_2 = PaintingRobot(expanded.copy(), image_mode=True)
panel_2, painted_2 = robot_2.run()
print_panel(panel_2)