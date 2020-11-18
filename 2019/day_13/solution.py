import itertools
import numpy as np
import tcod
from particles import ParticleSystem
program = [int(e) for e in open('data.txt', 'r').read().split(',')]

SCREEN_WIDTH = 44
SCREEN_HEIGHT = 20
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

tiles = {
    0: " ",
    1: "#",
    2: "~",
    3: "_",
    4: "o",
}

class Arcade:

    def __init__(self, program):
        self.output = []
        self.index = 0
        self.offset = 0
        self.input = []
        self.screen = {}
        self.index = 0
        self.offset = 0
        self.program = program.copy()
    
    def run(self):
        while True:
            output, cur_index, cur_offset = run_sequence(self.program, self.output, self.input, self.index, self.offset)
            if cur_index is not True:
                self.index = cur_index
                self.offset = cur_offset
            else:
                break
        for i in range(len(output)//3):
            self.screen[(output[i*3], output[i*3+1])] = tiles[output[i*3+2]]
        return self.screen
    
    def run_interactive(self):
        window_title = "Breakout"

        tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, False)
        tcod.sys_set_fps(20)
        input()
        index = 0
        particle_systems = []
        init = True
        while True:
            self.output.clear()
            to_clear = []
            for i, ps in enumerate(particle_systems):
                if ps.age <= ps.max_age:
                    ps.draw()
                    ps.update()
                    ps.add_particles(3)
                else:
                    to_clear.append(i)
            for i in to_clear[::-1]:
                ps = particle_systems.pop(i)
                ps.clear()
            
            output, cur_index, cur_offset = run_sequence(self.program, self.output, self.input, self.index, self.offset)
            index += 1
            if cur_index is not True:
                self.index = cur_index
                self.offset = cur_offset
                ball_x, paddle_x = 0, 0
                collision = 0
                for i in range(len(output)//3):
                    if output[i*3] == -1 and output[i*3+1] == 0:
                        tcod.console_set_window_title("Breakout - score %d" % output[i*3+2])
                        score = int(output[i*3+2])
                    else:
                        if output[i*3+2] == 2:
                            tcod.console_set_char_foreground(0, output[i*3], output[i*3+1], tcod.green)
                        else:
                            tcod.console_set_char_foreground(0, output[i*3], output[i*3+1], tcod.white)
                        if output[i*3+2] == 4:
                            ball_x = output[i*3]
                        elif output[i*3+2] == 3:
                            paddle_x = output[i*3]
                        elif output[i*3+2] == 0:
                            if not init and output[i*3+1] != 18:
                                collision += 1
                                col_x, col_y = output[i*3], output[i*3+1]
                        tcod.console_put_char(0, output[i*3], output[i*3+1], tiles[output[i*3+2]], tcod.BKGND_NONE)
                if init:
                    init = False
                if collision > 1:
                    ps = ParticleSystem(col_x, col_y)
                    ps.add_particles(4)
                    particle_systems.append(ps)
                #print("Score: ")
                tcod.console_set_default_foreground(0, tcod.white)
                tcod.console_flush()
                #tcod.console_clear(0)

                if ball_x > paddle_x:
                    self.input.append(1)
                elif ball_x < paddle_x:
                    self.input.append(-1)
                else:
                    self.input.append(0)
            else:
                for i in range(len(output)//3):
                    if output[i*3] == -1 and output[i*3+1] == 0:
                        score = int(output[i*3+2])
                break
        return score


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
robot = Arcade(expanded.copy())
screen = robot.run()
print(list(screen.values()).count('~'))

window_title = 'Pong vertical'
fullscreen = False

expanded[0] = 2
robot = Arcade(expanded.copy())
from time import time
t0 = time()
s = robot.run_interactive()
t1 = time()
print(s)
print(t1-t0)