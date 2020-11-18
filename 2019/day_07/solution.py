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
    99: 'break',
}

class Opcode:

    def __init__(self, opcode, index):
        self.opcode = opcode
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
            if not input:
                self.is_waiting = True
                return
            program[program[index+1]] = input.pop(0)
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

def run_sequence(program, output, input, index=0):
    opcode = Opcode(program[index], index)
    value = opcode.act(program, input, index)
    if value is not None:
        output.append(value)
    if opcode.is_finished:
        return output, True
    elif opcode.is_waiting:
        return output, index
    else:
        return run_sequence(program, output, input, opcode.next_index)


def find_highest_output(program):
    max = 0
    best = ()
    phases = {}
    for i, j, k, l, m in itertools.permutations([0, 1, 2, 3, 4]):
        a, _ = run_sequence(program.copy(), [], [i, 0])
        b, _ = run_sequence(program.copy(), [], [j, a[0]])
        c, _ = run_sequence(program.copy(), [], [k, b[0]])
        d, _ = run_sequence(program.copy(), [], [l, c[0]])
        e, _ = run_sequence(program.copy(), [], [m, d[0]])
        if e[0] > max:
            max = e[0]
            best = (i, j, k, l, m)
        phases[(i, j, k, l, m)] = e
    return max, best

program_test = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
assert find_highest_output(program_test)[0] == 43210
program_test = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
assert find_highest_output(program_test)[0] == 54321
max, best = find_highest_output(program)
print(max, best)

def run_feedback_loop(program):
    max = 0
    best = ()
    for i, j, k, l, m in itertools.permutations([5, 6, 7, 8, 9]):
        p_a, p_b, p_c, p_d, p_e = (program.copy() for _ in range(5))
        in_a, in_b, in_c, in_d, in_e = [i, 0], [j], [k], [l], [m]
        i_a, i_b, i_c, i_d, i_e = (0 for _ in range(5))
        while True:
            a, r_a = run_sequence(p_a, [], in_a, i_a)
            in_b.append(a[0])
            b, r_b = run_sequence(p_b, [], in_b, i_b)
            in_c.append(b[0])
            c, r_c = run_sequence(p_c, [], in_c, i_c)
            in_d.append(c[0])
            d, r_d = run_sequence(p_d, [], in_d, i_d)
            in_e.append(d[0])
            e, r_e = run_sequence(p_e, [], in_e, i_e)
            if r_e is not True:
                in_a.append(e[0])
                i_a, i_b, i_c, i_d, i_e = r_a, r_b, r_c, r_d, r_e
            else:
                print("Finished")
                value = e[0]
                break
        if value > max:
            max = value
            best = (i, j, k, l, m)
    return max, best
program_test = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
max, best = find_highest_output(program_test)
print(run_feedback_loop(program_test))
print(run_feedback_loop(program))

