from rich import print
from utils import load, file_to_lines, file_to_ints

def show_m(map_):
    print()
    for y in range(-2, 23):
        l = ""
        for x in range(-2, 26):
            l += map_.get((x, y), '.')
        print(l)
    print()

def is_in(boundaries, x, y):
    for boundary in boundaries:
        sx, sy, m_dist = boundary
        if sy-m_dist <= y <= sy+m_dist:
            if sx+abs(sy-y)-m_dist <= x <= sx-abs(sy-y)+m_dist+1:
                return True
    return False

def sol1(a, pos):
    data = file_to_lines(a)
    map_ = {}
    for line in data:
        s, b = line.split(": ")
        sx, sy = [int(e.split("=")[1]) for e in s.split(" at ")[1].split(", ")]
        map_[(sx, sy)] = "S"
        bx, by = [int(e.split("=")[1]) for e in b.split(" at ")[1].split(", ")]
        map_[(bx, by)] = "B"
        m_dist = abs(bx-sx)+abs(by-sy)
        if sy-m_dist < pos and sy+m_dist > pos:
            # do sthg
            for x in range(sx+abs(sy-pos)-m_dist, sx-abs(sy-pos)+m_dist+1):
                if (x, pos) not in map_:
                    map_[(x, pos)] = '#'
        #exit()
    total = 0
    for k in map_:
        if k[1] == pos:
            if map_[k] == '#':
                total += 1
    return total

def sol2(a, bounds):
    data = file_to_lines(a)
    map_ = {}
    # each line should remove space from the search
    # Define boundary of what's removed instead of everything
    boundaries = []
    for line in data:
        s, b = line.split(": ")
        sx, sy = [int(e.split("=")[1]) for e in s.split(" at ")[1].split(", ")]
        map_[(sx, sy)] = "S"
        bx, by = [int(e.split("=")[1]) for e in b.split(" at ")[1].split(", ")]
        map_[(bx, by)] = "B"
        m_dist = abs(bx-sx)+abs(by-sy)
        boundaries.append((sx,sy,m_dist))
    signal = None
    for x in range(4_000_001):
        for y in range(4_000_001):
            if y % 1_000_000 == 0:
                print(x, y)
            if not is_in(boundaries, x, y):
                signal = (x, y)
                break
    if not signal:
        print("Not found")
        exit()
    #signal = (14, 11)
    return signal[0]*4_000_000+signal[1]

test = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
asserts_sol1 = {
        test: 26
        }

asserts_sol2 = {
        test: 0
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d, 10) == expected, f"'sol1({d}, 10)' expected '{expected}' but was '{sol1(d, 10)}'"
    # print(f"\n{sol1(data, 2_000_000)=}\n")
    #for d,expected in asserts_sol2.items():
    #    assert sol2(d, (0, 20)) == expected, f"'sol2({d} (0, 20))' expected '{expected}' but was '{sol2(d (0, 20))}'"
    print(f"\n{sol2(data, (0, 4_000_000))=}\n")
