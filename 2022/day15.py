from rich import print
from utils import load, file_to_lines, file_to_ints

def show_m(map_):
    print()
    for y in range(0, 21):
        l = ""
        for x in range(0, 21):
            l += map_.get((x, y), '.')
        print(l)
    print()

# Bresenham line
def bline(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    a = y1-y0
    b = -(x1-x0)
    c = x1*y0-x0*y1
    return a, b, -c

# intersection point of two lines
def intersects(l1, l2):
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    D = a1*b2 - b1*a2
    Dx = c1*b2 - b1*c2
    Dy = a1*c2 - c1*a2
    if D != 0:
        x = int(Dx / D)
        y = int(Dy / D)
        return x, y
    else:
        return False

def compute_m(x0, y0, x1, y1):
    return abs(x1-x0)+abs(y1-y0)


def is_in(boundaries, x, y):
    for boundary in boundaries:
        sx, sy, m_dist = boundary
        if sy-m_dist <= y <= sy+m_dist:
            if sx+abs(sy-y)-m_dist <= x <= sx-abs(sy-y)+m_dist:
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
    lines = []
    boundaries = []

    for line in data:
        s, b = line.split(": ")
        sx, sy = [int(e.split("=")[1]) for e in s.split(" at ")[1].split(", ")]
        map_[(sx, sy)] = "S"
        bx, by = [int(e.split("=")[1]) for e in b.split(" at ")[1].split(", ")]
        map_[(bx, by)] = "B"
        m_dist = abs(bx-sx)+abs(by-sy)
        # 4 lines extending from outside the diamond, where the missing beacon can be
        l1 = bline((sx-m_dist-1, sy), (sx, sy-m_dist-1))
        l2 = bline((sx, sy-m_dist-1), (sx+m_dist+1, sy))
        l3 = bline((sx+m_dist+1, sy), (sx, sy+m_dist+1))
        l4 = bline((sx, sy+m_dist+1), (sx-m_dist-1, sy))
        lines.extend([l1, l2, l3, l4])
        boundaries.append((sx, sy, m_dist))
        # intersections = []
        # for i in range(len(lines)):
        #     for j in range(i+1, len(lines)):
        #         intersect = intersects(lines[i], lines[j])
        #         if intersect:
        #             intersections.append(intersect)
        # print(intersections)
        # exit()
    intersections = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            intersect = intersects(lines[i], lines[j])
            if intersect and not is_in(boundaries, intersect[0], intersect[1]):
                intersections.append(intersect)
    
    for i in intersections:
        if bounds[0] <= i[0] <= bounds[1]:
            if bounds[0] <= i[1] <= bounds[1]:
                signal = i
                break
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
        test: 56000011
        }


def reduce_allowed(allowed_areas, boundary, bounds):
    new_allowed = []
    sx, sy, m_dist = boundary
    while len(allowed_areas):
        allowed_area = allowed_areas.pop()
        print(allowed_area)
        print(boundary)
        if not overlaps(allowed_area, boundary):
            new_allowed.append(allowed_area)
        else:
            print("overlaps! Splitting")
        # Diamond is cutting 
    print(len(new_allowed))
    return new_allowed

def overlaps(allowed_area, boundary):
    x0, y0, x1, y1 = allowed_area
    sx, sy, m_dist = boundary
    # top left
    if compute_m(x0, y0, sx, sy) > m_dist and sx < x0 and sy < y0:
        return False
    # top
    elif compute_m(sx, y0, sx, sy) > m_dist and sy < y0:
        return False
    # top right
    elif compute_m(x1, y0, sx, sy) > m_dist and sx > x1 and sy < y0:
        return False
    # right
    elif compute_m(x1, sy, sx, sy) > m_dist and sx > x1:
        return False
    # bottom right
    elif compute_m(x1, y1, sx, sy) > m_dist and sx > x1 and sy > y1:
        return False
    elif compute_m(sx, y1, sx, sy) > m_dist and sy > y1:
        return False
    elif compute_m(x0, y1, sx, sy) > m_dist and sx < x0 and sy > y1:
        return False
    elif compute_m(x0, sy, sx, sy) > m_dist and sx < x0:
        return False
    return True

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d, 10) == expected, f"'sol1({d}, 10)' expected '{expected}' but was '{sol1(d, 10)}'"
    # print(f"\n{sol1(data, 2_000_000)=}\n")
    #for d,expected in asserts_sol2.items():
    #    assert sol2(d, (0, 20)) == expected, f"'sol2({d} (0, 20))' expected '{expected}' but was '{sol2(d, (0, 20))}'"
    print(f"\n{sol2(data, (0, 4_000_000))=}\n")
