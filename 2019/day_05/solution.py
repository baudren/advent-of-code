program = [int(e) for e in open('data.txt', 'r').read().split(',')]

def run_string(string, input=1):
    return run_sequence([int(e) for e in string.split(",")], input)

actions = {
    1: 'add',
    2: 'multiply',
    3: 'read_i',
    4: 'write_o',
    5: 'jump_if_true',
    6: 'jump_if_false',
    7: 'less_than',
    8: 'equals',
    99: 'break',
}

class Opcode:

    def __init__(self, opcode, index):
        self.opcode = opcode
        self.is_finished = False
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
            value_a = program[program[index+1]] if not self.parameter_modes[0] else program[index+1]
            value_b = program[program[index+2]] if not self.parameter_modes[1] else program[index+2]
            if self.action == 'add':
                program[program[index+3]] = value_a + value_b
            elif self.action == 'multiply':
                program[program[index+3]] = value_a * value_b
            elif self.action == 'less_than':
                program[program[index+3]] = 1 if value_a < value_b else 0
            elif self.action == 'equals':
                program[program[index+3]] = 1 if value_a == value_b else 0
            if program[index+3] == index:
                self.next_index = index
        elif self.action == 'read_i':
            program[program[index+1]] = input
            if program[index+1] == index:
                self.next_index = index
        elif self.action == 'write_o':
            if self.parameter_modes[0] == 0:
                return(program[program[index+1]])
            else:
                return(program[index+1])
        elif self.action in ['jump_if_true', 'jump_if_false']:
            self.next_index = index+3
            value = program[program[index+1]] if not self.parameter_modes[0] else program[index+1]
            if (value != 0 and self.action == 'jump_if_true') or (value == 0 and self.action == 'jump_if_false'):
                self.next_index = program[program[index+2]] if not self.parameter_modes[1] else program[index+2]
        else:
            self.is_finished = True

    def __str__(self):
        return "%s, %s, %s" % (str(self.opcode), self.action, self.parameter_modes)

def run_sequence(program, output, input=-1, index=0):
    opcode = Opcode(program[index], index)
    value = opcode.act(program, input, index)
    if value is not None:
        output.append(value)
    if opcode.is_finished:
        return output
    else:
        return run_sequence(program, output, input, opcode.next_index)


print(run_sequence(program.copy(), [], 1)[-1])
# EQUALS position mode
assert run_sequence([3,9,8,9,10,9,4,9,99,-1,8], [], 7) == [0]
assert run_sequence([3,9,8,9,10,9,4,9,99,-1,8], [], 8) == [1]
# LESS THAN position mode
assert run_sequence([3,9,7,9,10,9,4,9,99,-1,8], [], 7) == [1]
assert run_sequence([3,9,7,9,10,9,4,9,99,-1,8], [], 8) == [0]
# EQUALS immediate mode
assert run_sequence([3,3,1108,-1,8,3,4,3,99], [], 9) == [0]
assert run_sequence([3,3,1108,-1,8,3,4,3,99], [], 8) == [1]
# LESS THAN immediate mode
assert run_sequence([3,3,1107,-1,8,3,4,3,99], [], 7) == [1]
assert run_sequence([3,3,1107,-1,8,3,4,3,99], [], 8) == [0]
# JUMP tests position mode
assert run_sequence([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [], 0) == [0]
assert run_sequence([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [], 10) == [1]
# JUMP tests immediate mode
assert run_sequence([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [], 0) == [0]
assert run_sequence([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [], 0) == [0]

# COMPLEX
assert run_sequence([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [], 7) == [999]
assert run_sequence([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [], 8) == [1000]
assert run_sequence([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [], 9) == [1001]


print(run_sequence(program.copy(), [], 5)[-1])