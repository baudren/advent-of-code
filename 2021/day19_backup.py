class Map:

    def __init__(self, scanners):
        self.scanners = scanners
        self.scanners[0].pos = (0, 0, 0)
    
    def remove_duplicates(self):
        while True:
            try:
                for i, s1 in self.scanners.items():
                    for j in range(i+1, len(self.scanners)):
                        print(f"scanners {i}, {j}")
                        s2 = self.scanners[j]
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
                                print(f"match with orientation {k}")
                                #for e in found:
                                    #print(s1.beacons[e])
                                s2.set_orientation(k)
                                d2 = s2.dists(0)
                                first_tuple, ids = [(p,v) for p, v in d2.items() if p in d1][0]
                                s11 = s1.beacons[d1[first_tuple][1]]
                                s12 = s1.beacons[d1[first_tuple][0]]
                                print(s11)
                                print(s12)
                                print(s2.get_beacon(ids[0], 0))
                                print(s2.get_beacon(ids[1], 1))
                                for rot in range(8):
                                    s21 = s2.get_beacon(ids[0], rot)
                                    s22 = s2.get_beacon(ids[1], rot)
                                    #print(s11-s21, s12-s22)
                                    if(s11-s21 == s12-s22):
                                        print(f"match with rot {rot}")
                                        add = s12-s22
                                        print(add)
                                        if s2.pos is None:
                                            s2.rot = rot
                                            add = s12-s22
                                            s2.set_pos(add)
                                            #raise ValueError
            except ValueError:
                pass
            for i, s in self.scanners.items():
                print(i, s)
                print(s.pos)
            exit()
            if all([s.pos is not None for s in self.scanners.values()]):
                break
    
    def number_of_beacons(self):
        return sum([scanner.actual_length() for scanner in self.scanners.values()])

class Scanner:

    def __init__(self, id_):
        self.id = id_
        self.beacons = []
        self.used = set()
        self.pos = None
        self.orientation = 0
        self.rot = 0
    

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
            print("Reset the orientation!")

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

def sol1(scanners):
    print(scanners)
    m = Map(scanners)
    m.remove_duplicates()
    print(m.number_of_beacons())
    return m.number_of_beacons()


def sol2(scanners):
    return 0

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

    assert sol1(parse(test)) == 79
    print(sol1(parse(data)))
    assert sol2(*parse(test)) == 1924
    print(sol2(*parse(data)))
