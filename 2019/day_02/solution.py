from copy import deepcopy

with open('data.txt', 'r') as program_file:
    program = [int(e) for e in program_file.read().split(',')]

def run_string(string):
    return ",".join([str(r) for r in run_sequence([int(e) for e in string.split(",")])])

def run_array(array):
    return ",".join([str(r) for r in run_sequence(array)])

def run_sequence(program, index=0):
    opcode = program[index]
    if opcode == 99:
        return program
    else:
        value_a = program[program[index+1]]
        value_b = program[program[index+2]]
        if opcode == 1:
            program[program[index+3]] = value_a+value_b
        else:
            program[program[index+3]] = value_a*value_b
        return run_sequence(program, index+4)

assert run_string("1,0,0,0,99") == "2,0,0,0,99"
assert run_string("2,3,0,3,99") == "2,3,0,6,99"
assert run_string("2,4,4,5,99,0") == "2,4,4,5,99,9801"
assert run_string("1,1,1,4,99,5,6,0,99") == "30,1,1,4,2,5,6,0,99"

# Restore 1202
program_part1 = deepcopy(program)
program_part1[1] = 12
program_part1[2] = 2

print("part 1: %d" % run_sequence(program_part1)[0])


def search_output(program, output):
    for noun in range(100):
        for verb in range(100):
            search_program = deepcopy(program)
            search_program[1] = noun
            search_program[2] = verb
            if run_sequence(search_program)[0] == output:
                return noun, verb

noun, verb = search_output(program, 19690720)
print(noun, verb)
print("part 2: %d" % (100*int(noun)+int(verb)))
