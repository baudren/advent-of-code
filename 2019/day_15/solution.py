import itertools
import numpy as np
import tcod

program = [int(e) for e in open('data.txt', 'r').read().split(',')]

SCREEN_WIDTH = 60
SCREEN_HEIGHT = 60

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

directions = {
    tcod.KEY_UP: (0, -1),
    tcod.KEY_DOWN: (0, 1),
    tcod.KEY_LEFT: (-1, 0),
    tcod.KEY_RIGHT: (1, 0),
}
mapping = {
    tcod.KEY_UP: 1,
    tcod.KEY_DOWN: 2,
    tcod.KEY_LEFT: 3,
    tcod.KEY_RIGHT: 4,
}

class RepairDroid:

    def __init__(self, program, screen={}):
        self.output = []
        self.index = 0
        self.offset = 0
        self.input = []
        self.screen = screen
        self.program = program.copy()

    def pick_direction(self, position):
        keys = [tcod.KEY_UP, tcod.KEY_RIGHT, tcod.KEY_DOWN, tcod.KEY_LEFT]
        # check all not blocked path
        blocked = self.blocked.get(position, [])
        for key in keys:
            if key not in blocked:
                new_pos = tuple((e+f for e,f in zip(position, directions[key])))
                if new_pos not in self.screen:
                    return key
        # in case of dead end, backtrack, and mark the previous spot as blocked
        for i, key in enumerate(keys):
            if key not in blocked:
                new_pos = tuple((e+f for e,f in zip(position, directions[key])))
                if new_pos in self.screen and self.screen[new_pos] == '.':
                    if new_pos not in self.blocked:
                        self.blocked[new_pos] = []
                    self.blocked[new_pos].append(keys[(i+2)%4])
                    return key
        return False
        # takes first not explored
        # 
    def run_interactive(self):
        window_title = "Repair Droid"

        position = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.screen[position] = "@"
        tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, False)
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.sys_set_fps(250)
        for p, v in self.screen.items():
            tcod.console_put_char(0, p[0], p[1], v)
        tcod.console_flush()
        index = 0
        # pick a direction until you hit a wall, then turn right
        direction = 0
        self.blocked = {position: []}
        input()
        while True:
            # READ input
            key = self.pick_direction(position)
            if key is False:
                self.screen[self.exit_position] = ">"
                self.screen[position] = "."
                return self.screen
            #key = tcod.console_wait_for_keypress(True).vk
            self.input.append(mapping[key])
            index += 1
            output, cur_index, cur_offset = run_sequence(self.program, self.output, self.input, self.index, self.offset)
            if cur_index is not True:
                tcod.console_set_window_title("Repair Droid - %d steps" % index)
                self.index = cur_index
                self.offset = cur_offset
                result = output.pop()
                # if result == 2:
                #     tcod.console_put_char(0, position[0], position[1], ".")
                #     self.screen[position] = '.'
                #     position = tuple(e+f for e,f in zip(position, directions[key]))
                #     tcod.console_put_char(0, position[0], position[1], ">")
                #     self.screen[position] = '>'
                #     return self.screen
                if result in [1, 2]:
                    tcod.console_put_char(0, position[0], position[1], ".")
                    self.screen[position] = '.'
                    position = tuple(e+f for e,f in zip(position, directions[key]))
                    tcod.console_put_char(0, position[0], position[1], "@")
                    self.screen[position] = '@'
                    if result == 2:
                        self.exit_position = position
                else:
                    if position not in self.blocked:
                        self.blocked[position] = []
                    self.blocked[position].append(direction)
                    moved = False
                    # hit a wall
                    wall = tuple(e+f for e, f in zip(position, directions[key]))
                    self.screen[wall] = '#'
                    tcod.console_put_char(0, wall[0], wall[1], "#")
                tcod.console_flush()
            else:
                print("should not be here")
                break
        return index

    def fill_oxygen(self):
        #input()
        self.screen[self.exit_position] = "O"
        window_title = "Oxygen filling"
        #tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, False)
        #tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_clear(0)
        for p, v in self.screen.items():
            tcod.console_put_char(0, p[0], p[1], v)
        tcod.console_flush()
        minutes = 1
        while True:
            tcod.console_set_window_title("Oxygen filling - %d minutes" % minutes)
            new_pos = []
            for position, v in self.screen.items():
                if v == 'O':
                    for neighbour in self.get_neighbours(position):
                        if neighbour in self.screen and self.screen[neighbour] == '.':
                            new_pos.append(neighbour)
            if not new_pos:
                return minutes-1
            else:
                for pos in new_pos:
                    self.screen[pos] = 'O'
                    tcod.console_put_char(0, pos[0], pos[1], 'O')
            tcod.console_flush()
            minutes += 1


    def get_neighbours(self, p):
        return [
            (p[0]+1, p[1]),
            (p[0]-1, p[1]),
            (p[0], p[1]+1),
            (p[0], p[1]-1),
        ] 
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
robot = RepairDroid(expanded.copy(), {})
robot.run_interactive()
steps = robot.fill_oxygen()
print(steps)
