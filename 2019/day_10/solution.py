asteroids = [list(e.strip()) for e in open('data.txt', 'r').readlines()]
import numpy as np
from math import atan2, pi


def define_dict(asteroids):
    hash_map = {}
    for j, asteroid_line in enumerate(asteroids):
        for i, situation in enumerate(asteroids[j]):
            if situation == '#':
                hash_map[(i, j)] = 0
    return hash_map


def compute_los(asteroid_map):
    for coords in asteroid_map:
        number = 0
        for other in asteroid_map:
            if other != coords:
                if can_see(coords, other, asteroid_map):
                    number += 1
        asteroid_map[coords] = number

def can_see(coords, other, asteroid_map):
    vec = np.array([other[0]-coords[0], other[1]-coords[1]])
    debug = False
    if coords == (5, 8):
        debug = False
        #print("Comparing", coords, "with", other)
    for another in asteroid_map:
        if another not in [coords, other]:
            another_vec = np.array([another[0]-coords[0], another[1]-coords[1]])
            if debug:
                print(vec, another_vec, another)
            if another_vec[1]*vec[0] == another_vec[0]*vec[1] and vec @ another_vec > 0  and (abs(another_vec[1]) < abs(vec[1]) or (abs(another_vec[0])<abs(vec[0]))):
                if debug:
                    print("Obstructed by", another)
                return False
    return True

def get_max(asteroid_map):
    key, max = (), 0
    for k, v in asteroid_map.items():
        if v > max:
            max = v
            key = k
    return key, max


asteroids = [list(e.strip()) for e in """.#..#
.....
#####
....#
...##""".split("\n")]
asteroid_map = define_dict(asteroids)
compute_los(asteroid_map)
assert get_max(asteroid_map) == ((3, 4), 8)

# asteroids = [list(e.strip()) for e in """......#.#.
# #..#.#....
# ..#######.
# .#.#.###..
# .#..#.....
# ..#....#.#
# #..#....#.
# .##.#..###
# ##...#..#.
# .#....####""".split("\n")]
# asteroid_map = {}
# asteroid_map = define_dict(asteroids)
# compute_los(asteroid_map)
# k, m = get_max(asteroid_map)
# assert get_max(asteroid_map) == ((5, 8), 33)
# 
# 
# asteroids = [list(e.strip()) for e in """
# #.#...#.#.
# .###....#.
# .#....#...
# ##.#.#.#.#
# ....#.#.#.
# .##..###.#
# ..#...##..
# ..##....##
# ......#...
# .####.###.""".split("\n")]
# asteroid_map = {}
# asteroid_map = define_dict(asteroids)
# compute_los(asteroid_map)
# k, m = get_max(asteroid_map)
# assert get_max(asteroid_map) == ((1, 3), 35)
# 
# 
# 
# asteroids = [list(e.strip()) for e in """
# .#..#..###
# ####.###.#
# ....###.#.
# ..###.##.#
# ##.##.#.#.
# ....###..#
# ..#.#..#.#
# #..#.#.###
# .##...##.#
# .....#.#..""".split("\n")]
# asteroid_map = {}
# asteroid_map = define_dict(asteroids)
# compute_los(asteroid_map)
# k, m = get_max(asteroid_map)
# print(k, m)
# assert get_max(asteroid_map) == ((6, 4), 41)


asteroids = [list(e.strip()) for e in open('data.txt', 'r').readlines()]
asteroid_map = {}
asteroid_map = define_dict(asteroids)
# compute_los(asteroid_map)
# k, m = get_max(asteroid_map)
# print(k, m)
station = (23, 19)
EPSILON = 0.000001
def vaporize(asteroid_map, station):
    vaporized = []
    target = [station[0], 0]
    # compute angle and length
    keys = [e for e in asteroid_map if e != station]
    angles = [angle_between([x1 - x2 for (x1, x2) in zip(target, station)], [x1-x2 for (x1, x2) in zip(e, station)]) for e in asteroid_map if e != station]
    length = [np.linalg.norm(e) for e in asteroid_map if e != station]

    last_angle = 0.0-EPSILON
    while asteroid_map:
        min_angle, candidates = locate_min(angles, last_angle)
        if min_angle is False:
            break
        last_angle = min_angle
        closest = 10000
        closest_i = -1
        for e in candidates:
            if length[e] < closest:
                closest_i = e
        vaporized.append(keys[closest_i])
        asteroid_map.pop(keys[closest_i])
        keys.pop(closest_i), angles.pop(closest_i), length.pop(closest_i)
    return vaporized

def locate_min(angles, value):
    print("locate min", value)
    filtered = [e for e in angles if e > value]
    if not filtered:
        value -= 2*pi
        filtered = [e for e in angles if e > value]
        if not filtered:
            return False, []
    min_ = min(filtered)
    indices = [index for index, element in enumerate(angles) if element == min_]
    return min_, indices

def angle_between(v1, v2):
    x1, x2 = v1
    y1, y2 = v2
    angle = atan2(y2, y1) - atan2(x2, x1)
    if (angle < 0): angle += 2 * pi
    return angle

def rotate(target, length):
    if target[0] != length-1 and target[1] == 0:
        return [target[0]+1, target[1]]
    elif target[0] != 0 and target[1] == length-1:
        return [target[0]-1, target[1]]
    elif target[1] != length-1 and target[0] == length-1:
        return [target[0], target[1]+1]
    else:
        return [target[0], target[1]-1]

def destroy_asteroid(station, target, asteroid_map):
    can_see = []
    

vaporized = vaporize(asteroid_map.copy(), station)
print(vaporized[199])

