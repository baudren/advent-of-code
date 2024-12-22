import math
from rich import print
from utils import *

basic_transform = file_to_lines


def operation(secret, number, mul=True):
    other = secret * number if mul else int(secret / number)
    secret = other ^ secret
    return secret % 16777216

def get_next(secret):
    secret = operation(secret, 64)
    secret = operation(secret, 32, False)
    return operation(secret, 2048)

def sol1(data):
    total = 0
    for line in data:
        secret = int(line)
        for i in range(2000):
            secret = get_next(secret)
        total += secret
    return total


def sol2(data):
    total = 0
    diffs = {}
    bananas = {}
    size = 2000
    for line in data:
        secret = int(line)
        initial_secret = int(line)
        bananas[initial_secret] = {-1: int(line[-1])}
        diffs[initial_secret] = {}
        max_bananas = int(line[-1])
        for i in range(size):
            secret = get_next(secret)
            new_bananas = int(str(secret)[-1])
            diffs[initial_secret][i] = new_bananas - bananas[initial_secret][i-1]
            bananas[initial_secret][i] = new_bananas
    sequences = {}
    global_sequences = set()
    for secret in diffs:
        sequences[secret] = {}
        for k in range(4, size):
            key = (diffs[secret][k-3], diffs[secret][k-2], diffs[secret][k-1], diffs[secret][k])
            if key in sequences[secret]:
                continue
            sequences[secret][key] = bananas[secret][k]
            global_sequences.add(key)
    best_result = 0
    for sequence in global_sequences:
        result = 0
        for secret in diffs:
            result += sequences[secret].get(sequence, 0)
        if result > best_result:
            best_result = result

    return best_result


data = """1
2
3
2024"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))
