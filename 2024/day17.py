import math
from rich import print
from utils import *

basic_transform = file_to_lines

class OpCodeComputer:

    def __init__(self, registers, program):
        self.registers = registers
        self.program = program
        self.program_str = [str(e) for e in program]
        self.inst_pointer = 0

    def run_from(self, value):
        self.registers["A"] = value
        self.inst_pointer = 0
        # only really valid for my input... sorry
        while True:
            if self.program[self.inst_pointer] == 3:
                return self.registers["A"], self.registers["B"] % 8
            self.apply()
        
    def run(self):
        output = []
        while True:
            if self.inst_pointer >= len(self.program):
                return ",".join(output)
                break
            o = self.apply()
            if o:
                output.append(o)

    def combo(self, operand):
        if operand == 4:
            return self.registers["A"]
        elif operand == 5:
            return self.registers["B"]
        elif operand == 6:
            return self.registers["C"]
        elif operand == 7:
            raise NotImplementedError()
        else:
            return operand

    def apply(self):
        op_code, operand = self.program[self.inst_pointer:self.inst_pointer+2]
        if op_code == 0:
            # The adv instruction (opcode 0) performs division.
            # The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the instruction's combo operand.
            # The result of the division operation is truncated to an integer and then written to the A register.
            operand = self.combo(operand)
            self.registers["A"] = int(self.registers["A"] // math.pow(2, operand))
            self.inst_pointer += 2
        elif op_code == 1:
            # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand
            # then stores the result in register B.
            self.registers["B"] = self.registers["B"] ^ operand
            self.inst_pointer += 2
        elif op_code == 2:
            # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits),
            # then writes that value to the B register.
            self.registers["B"] = self.combo(operand) % 8
            self.inst_pointer += 2
        elif op_code == 3:
            # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
            # it jumps by setting the instruction pointer to the value of its literal operand;
            # if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
            if self.registers["A"] == 0:
                self.inst_pointer += 2
            else:
                self.inst_pointer = operand
        elif op_code == 4:
            # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B.
            # (For legacy reasons, this instruction reads an operand but ignores it.)
            self.registers["B"] = self.registers["B"] ^ self.registers["C"]
            self.inst_pointer += 2
        elif op_code == 5:
            #print(operand, self.combo(operand), self.combo(operand) % 8)
            # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
            # (If a program outputs multiple values, they are separated by commas.)
            self.inst_pointer += 2
            return str(int(self.combo(operand) % 8))
        elif op_code == 6:
            # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register.
            # (The numerator is still read from the A register.)
            operand = self.combo(operand)
            self.registers["B"] = int(self.registers["A"] // math.pow(2, operand))
            self.inst_pointer += 2
        elif op_code == 7:
            # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register.
            # (The numerator is still read from the A register.)
            operand = self.combo(operand)
            self.registers["C"] = int(self.registers["A"] // math.pow(2, operand))
            self.inst_pointer += 2

def sol1(data):
    registers = {}
    for line in data:
        if "Register" in line:
            registers[line.split(" ")[1].split(":")[0]] = int(line.split(": ")[1])
        elif "Program" in line:
            program = [int(e) for e in line.split(": ")[1].split(",")]
    computer = OpCodeComputer(registers, program)
    return computer.run()

def find_rec(n, computer, previous, next):
    if n < 0:
        return
    number = computer.program[-1-n]
    found = False
    count = 0
    i = previous[-1]*8
    while True:
        a, b = computer.run_from(i)
        if a > previous[-1]:
            break
        if b == number and a == previous[-1]:
            if count == next.get(n, 0):
                found = True
                break
            else:
                count += 1
        i += 1
    if not found:
        previous.pop(-1)
        if n-1 not in next:
            next[n-1] = 0
        next[n-1] += 1
        for k in next:
            if k > n-1:
                next[k] = 0
        return find_rec(n-1, computer, previous, next)

    previous.append(i)
    if n == len(computer.program)-1:
        return i
    else:
        return find_rec(n+1, computer, previous, next)

def sol2(data):
    registers = {}
    for line in data:
        if "Register" in line:
            registers[line.split(" ")[1].split(":")[0]] = int(line.split(": ")[1])
        elif "Program" in line:
            program = [int(e) for e in line.split(": ")[1].split(",")]
    computer = OpCodeComputer(registers, program)
    return find_rec(0, computer, [0], {})


data = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))