import math
from rich import print
from utils import *
from collections import defaultdict, Counter
import re
from functools import lru_cache

basic_transform = file_to_lines

# DON'T LOOK DOWN
global_moves = {}
global_moves['v'] = {
    ('A', '1'): '^<<',
    ('A', '2'): '^<',
    ('A', '4'): '^^<<',
    ('A', '5'): '^^<',
    ('A', '7'): '^^^<<',
    ('A', '8'): '^^^<',
    ('0', '4'): '^^<',
    ('0', '7'): '^^^<',
    ('0', '3'): '^>',
    ('0', '6'): '^^>',
    ('0', '9'): '^^^>',
    ('1', 'A'): '>>v',
    ('1', '5'): '^>',
    ('1', '8'): '^^>',
    ('1', '6'): '^>>',
    ('1', '9'): '^^>>',
    ('2', '4'): '^<', 
    ('2', '7'): '^^<',
    ('2', 'A'): 'v>',
    ('2', '6'): '^>',
    ('2', '9'): '^^>',
    ('3', '0'): 'v<',
    ('3', '4'): '^<<',
    ('3', '5'): '^<',
    ('3', '7'): '^^<<',
    ('3', '8'): '^^<',
    ('4', '0'): '>vv', #exception
    ('4', '2'): 'v>',
    ('4', '8'): '^>',
    ('4', 'A'): '>>vv', #exception
    ('4', '3'): 'v>>',
    ('4', '9'): '^>>',
    ('5', '1'): 'v<',
    ('5', '7'): '^<',
    ('5', 'A'): 'vv>',
    ('5', '3'): 'v>',
    ('5', '9'): '^>',
    ('6', '1'): 'v<<',
    ('6', '7'): '^<<',
    ('6', '0'): 'vv<',
    ('6', '2'): 'v<',
    ('6', '8'): '^<',
    ('7', '0'): '>vvv', #exception
    ('7', '2'): 'vv>',
    ('7', '5'): 'v>',
    ('7', 'A'): '>>vvv', #exception
    ('7', '3'): 'vv>>',
    ('7', '6'): 'v>>',
    ('8', '1'): 'vv<',
    ('8', '4'): 'v<',
    ('8', 'A'): 'vvv>',
    ('8', '3'): 'vv>',
    ('8', '6'): 'v>',
    ('9', '1'): 'vv<<',
    ('9', '4'): 'v<<',
    ('9', '0'): 'vvv<',
    ('9', '2'): 'vv<',
    ('9', '5'): 'v<',
    ('^', '>'): 'v>',
    ('A', 'v'): 'v<',
    ('A', '<'): 'v<<',
    ('<', 'A'): '>>^', # exception
    ('v', 'A'): '^>',
    ('>', '^'): '^<',
    ('<', '^'): '>^', # exception
    ('^', '<'): 'v<',
}

global_moves['h'] = {
    ('A', '1'): '^<<', # exception
    ('A', '2'): '<^',
    ('A', '4'): '^^<<', # exception
    ('A', '5'): '<^^',
    ('A', '7'): '^^^<<', # exception
    ('A', '8'): '<^^^',
    ('0', '4'): '^^<', # exception
    ('0', '7'): '^^^<', # exception
    ('0', '3'): '>^',
    ('0', '6'): '>^^',
    ('0', '9'): '>^^^',
    ('1', 'A'): '>>v',
    ('1', '5'): '>^',
    ('1', '8'): '>^^',
    ('1', '6'): '>>^',
    ('1', '9'): '>>^^',
    ('2', '4'): '<^', 
    ('2', '7'): '<^^',
    ('2', 'A'): '>v',
    ('2', '6'): '>^',
    ('2', '9'): '>^^',
    ('3', '0'): '<v',
    ('3', '4'): '<<^',
    ('3', '5'): '<^',
    ('3', '7'): '<<^^',
    ('3', '8'): '<^^',
    ('4', '0'): '>vv',
    ('4', '2'): '>v',
    ('4', '8'): '>^',
    ('4', 'A'): '>>vv',
    ('4', '3'): '>>v',
    ('4', '9'): '>>^',
    ('5', '1'): '<v',
    ('5', '7'): '<^',
    ('5', 'A'): '>vv',
    ('5', '3'): '>v',
    ('5', '9'): '>^',
    ('6', '1'): '<<v',
    ('6', '7'): '<<^',
    ('6', '0'): '<vv',
    ('6', '2'): '<v',
    ('6', '8'): '<^',
    ('7', '0'): '>vvv',
    ('7', '2'): '>vv',
    ('7', '5'): '>v',
    ('7', 'A'): '>>vvv',
    ('7', '3'): '>>vv',
    ('7', '6'): '>>v',
    ('8', '1'): '<vv',
    ('8', '4'): '<v',
    ('8', 'A'): '>vvv',
    ('8', '3'): '>vv',
    ('8', '6'): '>v',
    ('9', '1'): '<<vv',
    ('9', '4'): '<<v',
    ('9', '0'): '<vvv',
    ('9', '2'): '<vv',
    ('9', '5'): '<v',
    ('^', '>'): '>v',
    ('A', 'v'): '<v',
    ('A', '<'): 'v<<', # exception
    ('<', 'A'): '>>^',
    ('v', 'A'): '>^',
    ('>', '^'): '<^',
    ('<', '^'): '>^',
    ('^', '<'): 'v<', # exception
}

global_moves['lv_rh'] = {
    ('A', '1'): '^<<',
    ('A', '2'): '^<',
    ('A', '4'): '^^<<',
    ('A', '5'): '^^<',
    ('A', '7'): '^^^<<',
    ('A', '8'): '^^^<',
    ('0', '4'): '^^<',
    ('0', '7'): '^^^<',
    ('0', '3'): '>^',
    ('0', '6'): '>^^',
    ('0', '9'): '>^^^',
    ('1', 'A'): '>>v',
    ('1', '5'): '>^',
    ('1', '8'): '>^^',
    ('1', '6'): '>>^',
    ('1', '9'): '>>^^',
    ('2', '4'): '^<', 
    ('2', '7'): '^^<',
    ('2', 'A'): '>v',
    ('2', '6'): '>^',
    ('2', '9'): '>^^',
    ('3', '0'): 'v<',
    ('3', '4'): '^<<',
    ('3', '5'): '^<',
    ('3', '7'): '^^<<',
    ('3', '8'): '^^<',
    ('4', '0'): '>vv', #exception
    ('4', '2'): '>v',
    ('4', '8'): '>^',
    ('4', 'A'): '>>vv', #exception
    ('4', '3'): '>>v',
    ('4', '9'): '>>^',
    ('5', '1'): 'v<',
    ('5', '7'): '^<',
    ('5', 'A'): '>vv',
    ('5', '3'): '>v',
    ('5', '9'): '>^',
    ('6', '1'): 'v<<',
    ('6', '7'): '^<<',
    ('6', '0'): 'vv<',
    ('6', '2'): 'v<',
    ('6', '8'): '^<',
    ('7', '0'): '>vvv', #exception
    ('7', '2'): '>vv',
    ('7', '5'): '>v',
    ('7', 'A'): '>>vvv', #exception
    ('7', '3'): '>>vv',
    ('7', '6'): '>>v',
    ('8', '1'): 'vv<',
    ('8', '4'): 'v<',
    ('8', 'A'): '>vvv',
    ('8', '3'): '>vv',
    ('8', '6'): '>v',
    ('9', '1'): 'vv<<',
    ('9', '4'): 'v<<',
    ('9', '0'): 'vvv<',
    ('9', '2'): 'vv<',
    ('9', '5'): 'v<',
    ('^', '>'): '>v',
    ('A', 'v'): 'v<',
    ('A', '<'): 'v<<',
    ('<', 'A'): '>>^', # exception
    ('v', 'A'): '>^',
    ('>', '^'): '^<',
    ('<', '^'): '>^', # exception
    ('^', '<'): 'v<',
}

global_moves['lh_rv'] = {
    ('A', '1'): '^<<', # exception
    ('A', '2'): '<^',
    ('A', '4'): '^^<<', # exception
    ('A', '5'): '<^^',
    ('A', '7'): '^^^<<', # exception
    ('A', '8'): '<^^^',
    ('0', '4'): '^^<', # exception
    ('0', '7'): '^^^<', # exception
    ('0', '3'): '^>',
    ('0', '6'): '^^>',
    ('0', '9'): '^^^>',
    ('1', 'A'): '>>v',
    ('1', '5'): '^>',
    ('1', '8'): '^^>',
    ('1', '6'): '^>>',
    ('1', '9'): '^^>>',
    ('2', '4'): '<^', 
    ('2', '7'): '<^^',
    ('2', 'A'): 'v>',
    ('2', '6'): '^>',
    ('2', '9'): '^^>',
    ('3', '0'): '<v',
    ('3', '4'): '<<^',
    ('3', '5'): '<^',
    ('3', '7'): '<<^^',
    ('3', '8'): '<^^',
    ('4', '0'): '>vv',
    ('4', '2'): 'v>',
    ('4', '8'): '^>',
    ('4', 'A'): '>>vv',
    ('4', '3'): 'v>>',
    ('4', '9'): '^>>',
    ('5', '1'): '<v',
    ('5', '7'): '<^',
    ('5', 'A'): 'vv>',
    ('5', '3'): 'v>',
    ('5', '9'): '^>',
    ('6', '1'): '<<v',
    ('6', '7'): '<<^',
    ('6', '0'): '<vv',
    ('6', '2'): '<v',
    ('6', '8'): '<^',
    ('7', '0'): '>vvv',
    ('7', '2'): 'vv>',
    ('7', '5'): 'v>',
    ('7', 'A'): '>>vvv',
    ('7', '3'): 'vv>>',
    ('7', '6'): 'v>>',
    ('8', '1'): '<vv',
    ('8', '4'): '<v',
    ('8', 'A'): 'vvv>',
    ('8', '3'): 'vv>',
    ('8', '6'): 'v>',
    ('9', '1'): '<<vv',
    ('9', '4'): '<<v',
    ('9', '0'): '<vvv',
    ('9', '2'): '<vv',
    ('9', '5'): '<v',
    ('^', '>'): 'v>',
    ('A', 'v'): '<v',
    ('A', '<'): 'v<<', # exception
    ('<', 'A'): '>>^',
    ('v', 'A'): '^>',
    ('>', '^'): '<^',
    ('<', '^'): '>^',
    ('^', '<'): 'v<', # exception
}
# DON'T LOOK UP

numpadstr = """789
456
123
 0A"""
numpad = {}
for j, line in enumerate(numpadstr.split("\n")):
    for i, char in enumerate(line.rstrip()):
        if char != " ":
            numpad[char] = (i, j)
arrowpadstr = """ ^A
<v>"""
arrowpad = {}
for j, line in enumerate(arrowpadstr.split("\n")):
    for i, char in enumerate(line.rstrip()):
        if char != " ":
            arrowpad[char] = (i, j)

global_cache = {}
global_cache['h'] = {}
global_cache['v'] = {}
global_cache['lh_rv'] = {}
global_cache['lv_rh'] = {}

def find_path(target_pad, pattern, move='h'):
    path = ""
    current_char = 'A'
    target_cur = target_pad[current_char]
    debug = target_pad == arrowpad
    debug = False
    moves = global_moves[move]
    cache = global_cache[move]
    if debug: print(pattern)
    if pattern in cache:
        path = cache[pattern]
    else:
        for i, char in enumerate(pattern):
            x, y = target_cur
            target_nex = target_pad[char]
            xx, yy = target_nex
            if debug: print(f"{char=}, {target_nex=}, {target_cur=}")
            #if debug: input()
            if yy == y:
                path += '<'*(x-xx) if xx < x else '>'*(xx-x)
            elif xx == x:
                path += '^'*(y-yy) if yy < y else 'v'*(yy-y)
            else:

                if (current_char, char) in moves:
                    path += moves[(current_char, char)]
                elif '0' in target_pad:
                    # if target destination is lower, start by moving sideways, then go down
                    if yy > y:
                        path += '<'*(x-xx) if xx < x else '>'*(xx-x)
                        path += 'v'*(yy-y)
                    # if target destination is higher, start by moving up, then sideways
                    else:
                        path += '^'*(y-yy)
                        path += '<'*(x -xx) if xx < x else '>'*(xx-x)
                else:
                    # the contrary
                    # if target destination is lower, start by moving down, then sideways
                    if yy > y:
                        path += 'v'*(yy-y)
                        path += '<'*(x-xx) if xx < x else '>'*(xx-x)
                    # if target destination is higher, start by moving sideways, then up
                    else:
                        path += '<'*(x-xx) if xx < x else '>'*(xx-x)
                        path += '^'*(y-yy)
            path += 'A'
            target_cur = target_nex
            current_char = char
            #if debug: input()
    if debug:
        print(path)
    if pattern not in cache:
        cache[pattern] = path
    return path


def parse_pattern(pattern):
    regex = r'[^A]+A+'
    matches = re.findall(regex, pattern)
    return dict(Counter(matches))


def sol1(data):
    total = 0
    robots = 2
    for code in data:
        path_h = find_path(numpad, code, move='h')
        path_v = find_path(numpad, code, move='v')
        path_lh_rv = find_path(numpad, code, move='lh_rv')
        path_lv_rh = find_path(numpad, code, move='lv_rh')
        counter_h = parse_pattern(path_h)
        counter_v = parse_pattern(path_v)
        counter_lh_rv = parse_pattern(path_lh_rv)
        counter_lv_rh = parse_pattern(path_lv_rh)
        total_h, total_v, total_lh_rv, total_lv_rh = 0, 0, 0, 0
        for subpattern, count in counter_h.items():
            total_h += find_shortest_path(subpattern, robots)*count
        for subpattern, count in counter_v.items():
            total_v += find_shortest_path(subpattern, robots)*count
        for subpattern, count in counter_lh_rv.items():
            total_lh_rv += find_shortest_path(subpattern, robots)*count
        for subpattern, count in counter_lv_rh.items():
            total_lv_rh += find_shortest_path(subpattern, robots)*count
        total += min(total_h, total_v, total_lh_rv, total_lv_rh)*int(code[:-1])
    return total

@lru_cache(maxsize=None)
def find_shortest_path(pattern, layer):
    if layer == 0: return len(pattern)
    path_h = find_path(arrowpad, pattern, move='h')
    path_v = find_path(arrowpad, pattern, move='v')
    path_lh_rv = find_path(arrowpad, pattern, move='lh_rv')
    path_lv_rh = find_path(arrowpad, pattern, move='lv_rh')
    counter_h = parse_pattern(path_h)
    counter_v = parse_pattern(path_v)
    counter_lh_rv = parse_pattern(path_lh_rv)
    counter_lv_rh = parse_pattern(path_lv_rh)
    total_h, total_v, total_lh_rv, total_lv_rh = 0, 0, 0, 0
    for subpattern, count in counter_h.items():
        total_h += find_shortest_path(subpattern, layer-1)*count
    for subpattern, count in counter_v.items():
        total_v += find_shortest_path(subpattern, layer-1)*count
    for subpattern, count in counter_lh_rv.items():
        total_lh_rv += find_shortest_path(subpattern, layer-1)*count
    for subpattern, count in counter_lv_rh.items():
        total_lv_rh += find_shortest_path(subpattern, layer-1)*count
    return min(total_h, total_v, total_lh_rv, total_lv_rh)

def sol2(data):
    total = 0
    robots = 25
    for code in data:
        path_h = find_path(numpad, code, move='h')
        path_v = find_path(numpad, code, move='v')
        path_lh_rv = find_path(numpad, code, move='lh_rv')
        path_lv_rh = find_path(numpad, code, move='lv_rh')
        counter_h = parse_pattern(path_h)
        counter_v = parse_pattern(path_v)
        counter_lh_rv = parse_pattern(path_lh_rv)
        counter_lv_rh = parse_pattern(path_lv_rh)
        total_h, total_v, total_lh_rv, total_lv_rh = 0, 0, 0, 0
        for subpattern, count in counter_h.items():
            total_h += find_shortest_path(subpattern, robots)*count
        for subpattern, count in counter_v.items():
            total_v += find_shortest_path(subpattern, robots)*count
        for subpattern, count in counter_lh_rv.items():
            total_lh_rv += find_shortest_path(subpattern, robots)*count
        for subpattern, count in counter_lv_rh.items():
            total_lv_rh += find_shortest_path(subpattern, robots)*count
        total += min(total_h, total_v, total_lh_rv, total_lv_rh)*int(code[:-1])
    return total


data = """029A
980A
179A
456A
379A"""
data = load()

data = basic_transform(data)
print(sol1(data))
print(sol2(data))
print(find_shortest_path.cache_info())