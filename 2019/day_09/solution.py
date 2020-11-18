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
# crashes for 924 1207 1054

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
                print("before")
                program[program[index+3]+offset] = 1 if value_a < value_b else 0
                print("there")
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
            return output, True
        elif opcode.is_waiting:
            return output, index
        else:
            index = opcode.next_index
            offset = opcode.offset

import sys
sys.setrecursionlimit(10**7)

def expand(program):
    p_e = [0 for _ in range(10*len(program))]
    p_e[:len(program)] = program
    return p_e, program

program_test, orig = expand([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
assert run_sequence(program_test, [], [])[0] == orig

program_test, orig = expand([1102,34915192,34915192,7,4,7,99,0])
program, orig = expand(program)
#print(run_sequence(program_test, [], []))
print(run_sequence(program, [], [1]))
print(program[935:940])

print(run_sequence(program, [], [2]))

