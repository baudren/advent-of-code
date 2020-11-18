in_stream = open('data.txt', 'r').read()
in_stream = "12345678"

def phase(numbers):
    out = {}
    for i, v in numbers.items():
        print(i, v)
        out[i] = int(str(sum([u*relative_offset(i, j) for j, u in numbers.items()]))[-1])
    return out
    
def relative_offset(i, j):
    return [0, 1, 0, -1][i*]

def part_one(in_stream):
    numbers = {i: int(e) for i, e in enumerate(list(in_stream))}
    for _ in range(100):
        numbers = phase(numbers)
    return ''.join([str(v) for v in numbers.values()])

print(part_one(in_stream))
