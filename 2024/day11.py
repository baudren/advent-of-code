from rich import print
from utils import *

basic_transform = file_to_lines

def sol1(data):
    N = 25
    numbers = {int(e):1 for e in data[0].split()}
    for i in range(N):
        new_numbers = {}
        for n in numbers:
            if n == 0:
                new_numbers[1] = new_numbers.get(1, 0) + numbers[n]
            elif len(str(n)) % 2 == 0:
                a = int(str(n)[:len(str(n))//2])
                b = int(str(n)[len(str(n))//2:])
                new_numbers[a] = new_numbers.get(a, 0)+numbers[n]
                new_numbers[b] = new_numbers.get(b, 0)+numbers[n]
            else:
                new_numbers[n*2024] = new_numbers.get(n*2024, 0) + numbers[n]
        numbers = new_numbers
        #print(numbers)
    return(sum(numbers.values()))


def sol2(data):
    N = 75
    numbers = {int(e):1 for e in data[0].split()}
    for i in range(N):
        new_numbers = {}
        for n in numbers:
            if n == 0:
                new_numbers[1] = new_numbers.get(1, 0) + numbers[n]
            elif len(str(n)) % 2 == 0:
                a = int(str(n)[:len(str(n))//2])
                b = int(str(n)[len(str(n))//2:])
                new_numbers[a] = new_numbers.get(a, 0)+numbers[n]
                new_numbers[b] = new_numbers.get(b, 0)+numbers[n]
            else:
                new_numbers[n*2024] = new_numbers.get(n*2024, 0) + numbers[n]
        numbers = new_numbers
        #print(numbers)
    return(sum(numbers.values()))

data = load()
#data = "125 17"
data = basic_transform(data)

print("\n\n\n\n\n")
print(sol1(data))
print(sol2(data))

from time import time
t0 = time()
for _ in range(10):
    sol2(data)
t1 = time()
print((t1-t0)/10)