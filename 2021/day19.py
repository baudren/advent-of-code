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
                        for k in range(24):
                            d2 = s2.dists(k)
                            found = set([item for p, v in d1.items() if p in d2 for item in v])
                            other = set([item for p, v in d2.items() if p in d1 for item in v])
                            if len(other) >= 12 and s1.pos is not None:
                                print(f"match with orientation {k}")
                                s2.orientation = k
                                # do the same as before but without the abs to determine which item matched exactly
                                first_tuple, ids = [(p,v) for p, v in d2.items() if p in d1][0]
                                s11 = s1.beacons[d1[first_tuple][0]]
                                s12 = s1.beacons[d1[first_tuple][1]]
                                s21 = s2.get_beacon(ids[0], 0)
                                s22 = s2.get_beacon(ids[1], 0)
                                #print(f"s11 {s11}, s12 {s12}")
                                #print(f"s21 {s21}, s22 {s22}")
                                for rot in range(8):
                                    s21 = s2.get_beacon(ids[0], rot)
                                    s22 = s2.get_beacon(ids[1], rot)
                                    #print(s11-s21, s12-s22)
                                    if(s11-s21 == s12-s22):
                                        print(f"match with rot {rot}")
                                        if s2.pos is None:
                                            s2.rot = rot
                                            add = s12-s22
                                            s2.set_pos((add[0]+s1.pos[0],add[1]+s1.pos[1],add[2]+s1.pos[2]))
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
    
    def set_pos(self, pos):
        self.pos = pos
        # recompute all beacons based on pos, rot and orientation
        new_beacons = []
        for beacon in self.beacons:
            x, y, z = beacon.x, beacon.y, beacon.z
            if self.orientation == 0:
                x, y, z = x, y, z
            elif self.orientation == 1:
                x, y, z = y, x, z
            elif self.orientation == 2:
                x, y, z = z, y, x
            elif self.orientation == 3:
                x, y, z = z, x, y
            elif self.orientation == 4:
                x, y, z = x, z, y
            elif self.orientation == 5:
                x, y, z = y, z, x
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
            x += self.pos[0]
            y += self.pos[1]
            z += self.pos[2]
            new_beacons.append(Beacon(",".join((str(x), str(y), str(z)))))
        self.beacons = new_beacons


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
        #print(f"get_beacon: {beacon}")
        #print(self.beacons[i])
        return beacon

    def __repr__(self):
        return f"Scanner({self.id})"
    
    def actual_length(self):
        return len(self.beacons)-len(self.used)
    
    # Return values
    def dists(self, k):
        dists = {}
        for i, b1 in enumerate(self.beacons):
                for j in range(i+1, len(self.beacons)):
                    b2 = self.beacons[j]
                    if k == 0:
                        dists[(b2.x-b1.x, b2.y-b1.y, b2.z-b1.z)] = (i,j)
                    elif k == 1:
                        dists[(b1.x-b2.x, b2.y-b1.y, b2.z-b1.z)] = (i,j)
                    elif k == 2:
                        dists[(b2.x-b1.x, b1.y-b2.y, b2.z-b1.z)] = (i,j)
                    elif k == 3:
                        dists[(b2.x-b1.x, b2.y-b1.y, b1.z-b2.z)] = (i,j)
                    elif k == 4:
                        dists[(b2.y-b1.y, b2.x-b1.x, b2.z-b1.z)] = (i,j)
                    elif k == 5:
                        dists[(b1.y-b2.y, b2.x-b1.x, b2.z-b1.z)] = (i,j)
                    elif k == 6:
                        dists[(b2.y-b1.y, b1.x-b2.x, b2.z-b1.z)] = (i,j)
                    elif k == 7:
                        dists[(b2.y-b1.y, b2.x-b1.x, b1.z-b2.z)] = (i,j)
                    elif k == 8:
                        dists[(b2.z-b1.z, b2.y-b1.y, b2.x-b1.x)] = (i,j)
                    elif k == 9:
                        dists[(b1.z-b2.z, b2.y-b1.y, b2.x-b1.x)] = (i,j)
                    elif k == 10:
                        dists[(b2.z-b1.z, b1.y-b2.y, b2.x-b1.x)] = (i,j)
                    elif k == 11:
                        dists[(b2.z-b1.z, b2.y-b1.y, b1.x-b2.x)] = (i,j)
                    elif k == 12:
                        dists[(b2.z-b1.z, b2.x-b1.x, b2.y-b1.y)] = (i,j)
                    elif k == 13:
                        dists[(b1.z-b2.z, b2.x-b1.x, b2.y-b1.y)] = (i,j)
                    elif k == 14:
                        dists[(b2.z-b1.z, b1.x-b2.x, b2.y-b1.y)] = (i,j)
                    elif k == 15:
                        dists[(b2.z-b1.z, b2.x-b1.x, b1.y-b2.y)] = (i,j)
                    elif k == 16:
                        dists[(b2.x-b1.x, b2.z-b1.z, b2.y-b1.y)] = (i,j)
                    elif k == 17:
                        dists[(b1.x-b2.x, b2.z-b1.z, b2.y-b1.y)] = (i,j)
                    elif k == 18:
                        dists[(b2.x-b1.x, b1.z-b2.z, b2.y-b1.y)] = (i,j)
                    elif k == 19:
                        dists[(b2.x-b1.x, b2.z-b1.z, b1.y-b2.y)] = (i,j)
                    elif k == 20:
                        dists[(b2.y-b1.y, b2.z-b1.z, b2.x-b1.x)] = (i,j)
                    elif k == 21:
                        dists[(b1.y-b2.y, b2.z-b1.z, b2.x-b1.x)] = (i,j)
                    elif k == 22:
                        dists[(b2.y-b1.y, b1.z-b2.z, b2.x-b1.x)] = (i,j)
                    elif k == 23:
                        dists[(b2.y-b1.y, b2.z-b1.z, b1.x-b2.x)] = (i,j)
        return dists

    # relative
    def rdists(self, k):
        dists = {}
        for i, b1 in enumerate(self.beacons):
            for j, b2 in enumerate(self.beacons):
                if i != j:
                    if k == 0:
                        dists[(b2.x-b1.x, b2.y-b1.y, b2.z-b1.z)] = (i,j)
                    elif k == 1:
                        dists[(b2.y-b1.y, b2.x-b1.x, b2.z-b1.z)] = (i,j)
                    elif k == 2:
                        dists[(b2.z-b1.z, b2.y-b1.y, b2.x-b1.x)] = (i,j)
                    elif k == 3:
                        dists[(b2.z-b1.z, b2.x-b1.x, b2.y-b1.y)] = (i,j)
                    elif k == 4:
                        dists[(b2.x-b1.x, b2.z-b1.z, b2.y-b1.y)] = (i,j)
                    elif k == 5:
                        dists[(b2.y-b1.y, b2.z-b1.z, b2.x-b1.x)] = (i,j)
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
