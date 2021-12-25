class Map:

    def __init__(self, scanners):
        self.scanners = scanners
        self.scanners[0].pos = (0, 0, 0)
    
    def remove_duplicates(self):
        while True:
            for i, s1 in self.scanners.items():
                for j, s2 in self.scanners.items():
                    if i == j: continue
                    if s1.pos is None:
                        continue                        
                    if s2.pos is not None:
                        continue
                    d1 = s1.dists(0)
                    for k in range(6):
                        d2 = s2.dists(k)
                        found = set([item for p, v in d1.items() if p in d2 for item in v])
                        other = set([item for p, v in d2.items() if p in d1 for item in v])
                        f = [v for p,v in d1.items() if p in d2]
                        o = [v for p,v in d2.items() if p in d1]
                        if len(other) >= 12 and s1.pos is not None:
                            s2.set_orientation(k)
                            d2 = s2.dists(0)
                            # Take two tuples with one common elements, to identify the corresponding point
                            a, a_id = [(p,v) for p, v in d2.items() if p in d1][0]
                            b, b_id = None, None
                            c, c_id = None, None
                            for item, item_id in [(p,v) for p, v in d2.items() if p in d1][1:]:
                                if a_id[0] in item_id:
                                    b, b_id = item, item_id
                                    break
                            for item, item_id in [(p,v) for p, v in d2.items() if p in d1][1:]:
                                if a_id[1] in item_id:
                                    c, c_id = item, item_id
                                    break
                            common_ab_2 = [e for e in a_id if e in b_id][0]
                            common_ac_2 = [e for e in a_id if e in c_id][0]
                            common_ab_1 = [e for e in d1[a] if e in d1[b]][0]
                            common_ac_1 = [e for e in d1[a] if e in d1[c]][0]
                            s11 = s1.beacons[common_ab_1]
                            s12 = s1.beacons[common_ac_1]

                            for rot in range(8):
                                s21 = s2.get_beacon(common_ab_2, rot)
                                s22 = s2.get_beacon(common_ac_2, rot)
                                if(s11-s21 == s12-s22):
                                    add = s12-s22
                                    if s2.pos is None:
                                        s2.rot = rot
                                        add = s12-s22
                                        s2.set_pos(add)
            if all([s.pos is not None for s in self.scanners.values()]):
                break

    def number_of_beacons(self):
        beacons = set()
        for i, s in self.scanners.items():
            for b in s.beacons:
                beacons.add(b.to_tuple())
        return len(beacons)
    
    def max_distance(self):
        max_ = 0
        for i, s1 in self.scanners.items():
            for j in range(i+1, len(self.scanners)):
                s2 = self.scanners[j]
                d = s1.dist_from(s2)
                if d > max_:
                    max_ = d
        return max_


class Scanner:

    def __init__(self, id_):
        self.id = id_
        self.beacons = []
        self.used = set()
        self.pos = None
        self.orientation = 0
        self.rot = 0
    
    def dist_from(self, other):
        manhattan = 0
        for p, q in zip(self.pos, other.pos):
            manhattan += abs(q-p)
        return manhattan

    def set_orientation(self, k):
        if k != self.orientation:
            self.orientation = k
            new_beacons = []
            for beacon in self.beacons:
                x, y, z = beacon.x, beacon.y, beacon.z
                if k == 0:
                    x, y, z = x, y, z
                elif k == 1:
                    x, y, z = y, x, z
                elif k == 2:
                    x, y, z = z, y, x
                elif k == 3:
                    x, y, z = z, x, y
                elif k == 4:
                    x, y, z = x, z, y
                elif k == 5:
                    x, y, z = y, z, x
                new_beacons.append(Beacon(",".join((str(x), str(y), str(z)))))
            self.beacons = new_beacons

    def set_pos(self, pos):
        # recompute all beacons based on pos, rot and orientation
        new_beacons = []
        for beacon in self.beacons:
            x, y, z = beacon.x, beacon.y, beacon.z
            if self.rot == 0:
                x, y, z = x, y, z
            elif self.rot == 1:
                x, y, z = -x, y, z
            elif self.rot == 2:
                x, y, z = x, -y, z
            elif self.rot == 3:
                x, y, z = x, y, -z
            elif self.rot == 4:
                x, y, z = -x, -y, z
            elif self.rot == 5:
                x, y, z = x, -y, -z
            elif self.rot == 6:
                x, y, z = -x, y, -z
            elif self.rot == 7:
                x, y, z = -x, -y, -z
            x += pos[0]
            y += pos[1]
            z += pos[2]
            new_beacons.append(Beacon(",".join((str(x), str(y), str(z)))))
        self.beacons = new_beacons
        self.pos = pos


    def add_beacon(self, beacon):
        self.beacons.append(beacon)
    
    def get_beacon(self, i, rot):
        if rot == 0:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(x), str(y), str(z))))
        elif rot == 1:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(-x), str(y), str(z))))
        elif rot == 2:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(x), str(-y), str(z))))
        elif rot == 3:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(x), str(y), str(-z))))
        elif rot == 4:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(-x), str(-y), str(z))))
        elif rot == 5:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(x), str(-y), str(-z))))
        elif rot == 6:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(-x), str(y), str(-z))))
        elif rot == 7:
            x, y, z = self.beacons[i].x,self.beacons[i].y,self.beacons[i].z
            beacon = Beacon(",".join((str(-x), str(-y), str(-z))))
        return beacon

    def __repr__(self):
        return f"Scanner({self.id})"
    
    def actual_length(self):
        return len(self.beacons)-len(self.used)
    
    # Return absolute values
    def dists(self, k):
        dists = {}
        for i, b1 in enumerate(self.beacons):
            #if i not in self.used:
                for j in range(i+1, len(self.beacons)):
                    #if j not in self.used:
                        b2 = self.beacons[j]
                        if k == 0:
                            value = (abs(b2.x-b1.x), abs(b2.y-b1.y), abs(b2.z-b1.z))
                        elif k == 1:
                            value = (abs(b2.y-b1.y), abs(b2.x-b1.x), abs(b2.z-b1.z))
                        elif k == 2:
                            value = (abs(b2.z-b1.z), abs(b2.y-b1.y), abs(b2.x-b1.x))
                        elif k == 3:
                            value = (abs(b2.z-b1.z), abs(b2.x-b1.x), abs(b2.y-b1.y))
                        elif k == 4:
                            value = (abs(b2.x-b1.x), abs(b2.z-b1.z), abs(b2.y-b1.y))
                        elif k == 5:
                            value = (abs(b2.y-b1.y), abs(b2.z-b1.z), abs(b2.x-b1.x))
                        dists[value] = (i, j)
        return dists


class Beacon:

    def __init__(self, pos):
        self.x, self.y, self.z = (int(e) for e in pos.split(","))
    
    def __repr__(self):
        return f"Beacon({self.x}, {self.y}, {self.z})"
    
    def __sub__(self, other):
        return (self.x-other.x,self.y-other.y,self.z-other.z)
    
    def __add__(self, other):
        return (self.x+other.x,self.y+other.y,self.z+other.z)
    
    def to_tuple(self):
        return (self.x, self.y, self.z)

def sol(scanners):
    m = Map(scanners)
    m.remove_duplicates()
    return m.number_of_beacons(), m.max_distance()


def parse(data):
    scanners = {}
    scanner = None
    for line in data:
        if '---' in line:
            if scanner is not None:
                scanners[scanner.id] = scanner
            scanner = Scanner(int(line.split(" ")[2]))
        elif line:
            scanner.add_beacon(Beacon(line))
    scanners[scanner.id] = scanner
    return scanners

if __name__ == "__main__":
    data = [e.strip() for e in open('day19.txt', 'r').readlines()]
    test = [e.strip() for e in open('day19_test.txt', 'r').readlines()]

    assert sol(parse(test)) == (79, 3621)
    print(sol(parse(data)))
