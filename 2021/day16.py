from aocd import get_data, submit
import numpy as np
from time import time
from functools import reduce
import operator


class Packet:

    def __init__(self, hexa=None, binary=None):
        if hexa:
            self.hexa = hexa
            self.bin = bin(int(hexa, 16))[2:].zfill(len(hexa)*4)
        else:
            self.hexa = hex(int(binary, 2))[2:]
            self.bin = binary
        self.version = int(self.bin[:3], 2)
        self.type_id = int(self.bin[3:6], 2)
        self.is_literal = self.type_id == 4
        self.children = []
        if self.is_literal:
            self.number_bin = ""
            index = 0
            has_next = True
            while has_next:
                has_next = self.bin[6+index*5] == '1'
                self.number_bin += self.bin[6+index*5+1:6+index*5+5]
                index += 1
            self.number = int(self.number_bin, 2)
            self.length = 6+index*5
        else:
            self.length_type_id = self.bin[6]
            if self.length_type_id == '0':
                self.length_in_bits = int(self.bin[7:7+15], 2)
                previous_length = 0
                while previous_length < self.length_in_bits:
                    child = Packet(binary=self.bin[7+15+previous_length:])
                    self.children.append(child)
                    previous_length += child.length
                self.length = 7+15+previous_length
            else:
                self.number_of_packets = int(self.bin[7:7+11], 2)
                n = 0
                previous_length = 0
                while n < self.number_of_packets:
                    child = Packet(binary=self.bin[7+11+previous_length:])
                    self.children.append(child)
                    previous_length += child.length
                    n += 1
                self.length = 7+11+previous_length
            if self.type_id == 0: # sum packets
                self.number = sum(c.number for c in self.children)
            elif self.type_id == 1: # product packets
                self.number = reduce(operator.mul, [c.number for c in self.children], 1)
            elif self.type_id == 2: # min
                self.number = min(c.number for c in self.children)
            elif self.type_id == 3: # max
                self.number = max(c.number for c in self.children)
            elif self.type_id == 5: # greater than
                self.number = 1 if self.children[0].number > self.children[1].number else 0
            elif self.type_id == 6: # less than
                self.number = 1 if self.children[0].number < self.children[1].number else 0
            elif self.type_id == 7: # equal to
                self.number = 1 if self.children[0].number == self.children[1].number else 0

    def __repr__(self):
        return f"{self.hexa}: {self.bin}"
    
    def sum_versions(self):
        return self.version + sum(c.sum_versions() for c in self.children)


def sol1(data):
    return Packet(data).sum_versions()

def sol2(data):
    return Packet(data).number

if __name__ == "__main__":
    #data = np.array([int(e) for e in get_data(day=7, year=2021).split(",")])
    data = open('day16.txt').readlines()[0]
    assert sol1("8A004A801A8002F478") == 16
    assert sol1("620080001611562C8802118E34") == 12
    assert sol1("C0015000016115A2E0802F182340") == 23
    assert sol1("A0016C880162017C3686B18A3D4780") == 31
    print(sol1(data))

    assert sol2("C200B40A82") == 3
    assert sol2("04005AC33890") == 54
    assert sol2("880086C3E88112") == 7
    assert sol2("CE00C43D881120") == 9
    assert sol2("D8005AC2A8F0") == 1
    assert sol2("F600BC2D8F") == 0
    assert sol2("9C005AC2F8F0") == 0
    assert sol2("9C0141080250320F1802104A08") == 1
    print(sol2(data))
    #submit(sol2(data), part="b", day=7, year=2021)