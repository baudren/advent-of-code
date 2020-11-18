import numpy as np
from math import floor

min_, max_ = 245182, 790572
numbers = np.arange(min_, max_+1)    

def match(number):
    d = floor(number/10)
    has_double = '0' in str(number-d)
    if not has_double:
        return False
    s = str(number)
    for i, n in enumerate(s[:-1]):
        if n > s[i+1]:
            return False
    return True

def match2(number):
    d = floor(number/10)
    numbers = set(str(number))
    has_double = []
    for i in numbers:
        match = ''.join(['1' if e == i else '0' for e in str(number)])
        if match.count('1') >= 2:
            has_double.append(match.count('1') == 2)
    if not has_double or not any(has_double):
        return False
    s = str(number)
    for i, n in enumerate(s[:-1]):
        if n > s[i+1]:
            return False
    return True


vm = np.vectorize(match)
print("part 1:", np.sum(np.where(vm(numbers), 1, 0)))

vm2 = np.vectorize(match2)
print("part 2:", np.sum(np.where(vm2(numbers), 1, 0)))
