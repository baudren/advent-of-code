from collections import Counter

class Map:

    def __init__(self, scanners):
        self.scanners = scanners
        self.scanners[0].pos = (0, 0, 0)
    
    def remove_duplicates(self):
        while True:
            for i, s1 in self.scanners.items():
                for j, s2 in self.scanners.items():
                    if i == j: continue
                    if s2.pos is not None: continue
                    if s1.pos is None: continue
                    print(f"scanners {i}, {j}")
                    d1 = s1.adists(0)
                    for k in range(6):
                        d2 = s2.adists(k)
                        found = set([item for p, v in d1.items() if p in d2 for item in v])
                        other = set([item for p, v in d2.items() if p in d1 for item in v])
                        #print(k, len(other))
                        if len(other) >= 12:
                            print("Found axes!")
                            print(k)
                            s2.set_orientation(k)
                            for r1 in range(4):
                                for r2 in range(4):
                                    d1 = s1.rdists(r1)
                                    d2 = s2.rdists(r2)
                                    found = set([item for p, v in d1.items() if p in d2 for item in v])
                                    other = set([item for p, v in d2.items() if p in d1 for item in v])
                                    if len(other) >= 12:
                                        print("Found rotation!")
                                        print(r1, r2)
                            break
                        else:
                            continue
                        break
                    #print(d1)
            if all([s.pos is not None for s in self.scanners.values()]):
                break
            else:
                break
    
    def number_of_beacons(self):
        return sum([len(scanner.beacons) for scanner in self.scanners.values()])

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
    
    # relative dists with rotation
    def rdists(self, rot):
        dists = {}
        for i, b1 in enumerate(self.beacons):
            for j in range(i+1, len(self.beacons)):
                b2 = self.beacons[j]
                #if i != j:
                if rot == 0:
                    dists[(b2.x-b1.x, b2.y-b1.y, b2.z-b1.z)] = (i,j)
                elif rot == 1:
                    dists[(b1.x-b2.x, b2.y-b1.y, b2.z-b1.z)] = (i,j)
                elif rot == 2:
                    dists[(b2.x-b1.x, b1.y-b2.y, b2.z-b1.z)] = (i,j)
                elif rot == 3:
                    dists[(b2.x-b1.x, b2.y-b1.y, b1.z-b2.z)] = (i,j)
        return dists
    # relative dists
    def dists(self, k):
        dists = {}
        for i, b1 in enumerate(self.beacons):
            for j in range(i+1, len(self.beacons)):
                b2 = self.beacons[j]
                #if i != j:
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
                elif k == 6:
                    dists[(b1.x-b2.x, b1.y-b2.y, b1.z-b2.z)] = (i,j)
                elif k == 7:
                    dists[(b1.y-b2.y, b1.x-b2.x, b1.z-b2.z)] = (i,j)
                elif k == 8:
                    dists[(b1.z-b2.z, b1.y-b2.y, b1.x-b2.x)] = (i,j)
                elif k == 9:
                    dists[(b1.z-b2.z, b1.x-b2.x, b1.y-b2.y)] = (i,j)
                elif k == 10:
                    dists[(b1.x-b2.x, b1.z-b2.z, b1.y-b2.y)] = (i,j)
                elif k == 11:
                    dists[(b1.y-b2.y, b1.z-b2.z, b1.x-b2.x)] = (i,j)

                elif k == 12:
                    dists[(b1.x-b2.x, b2.y-b1.y, b2.z-b1.z)] = (i,j)
                elif k == 13:
                    dists[(b2.y-b1.y, b1.x-b2.x, b2.z-b1.z)] = (i,j)
                elif k == 14:
                    dists[(b2.z-b1.z, b2.y-b1.y, b1.x-b2.x)] = (i,j)
                elif k == 15:
                    dists[(b2.z-b1.z, b1.x-b2.x, b1.y-b2.y)] = (i,j)
                elif k == 16:
                    dists[(b1.x-b2.x, b2.z-b1.z, b1.y-b2.y)] = (i,j)
                elif k == 17:
                    dists[(b1.y-b2.y, b1.z-b2.z, b2.x-b1.x)] = (i,j)
                elif k == 18:
                    dists[(b2.x-b1.x, b1.y-b2.y, b1.z-b2.z)] = (i,j)
                elif k == 19:
                    dists[(b1.y-b2.y, b2.x-b1.x, b1.z-b2.z)] = (i,j)
                elif k == 20:
                    dists[(b1.z-b2.z, b1.y-b2.y, b2.x-b1.x)] = (i,j)
                elif k == 21:
                    dists[(b2.z-b1.z, b2.x-b1.x, b1.y-b2.y)] = (i,j)
                elif k == 22:
                    dists[(b2.x-b1.x, b1.z-b2.z, b2.y-b1.y)] = (i,j)
                elif k == 23:
                    dists[(b2.y-b1.y, b2.z-b1.z, b1.x-b2.x)] = (i,j)
        return dists
    # Return absolute values
    def adists(self, k):
        dists = {}
        for i, b1 in enumerate(self.beacons):
            for j in range(i+1, len(self.beacons)):
                b2 = self.beacons[j]
                if k == 0:
                    dists[(abs(b2.x-b1.x), abs(b2.y-b1.y), abs(b2.z-b1.z))] = (i,j)
                elif k == 1:
                    dists[(abs(b2.y-b1.y), abs(b2.x-b1.x), abs(b2.z-b1.z))] = (i,j)
                elif k == 2:
                    dists[(abs(b2.z-b1.z), abs(b2.y-b1.y), abs(b2.x-b1.x))] = (i,j)
                elif k == 3:
                    dists[(abs(b2.z-b1.z), abs(b2.x-b1.x), abs(b2.y-b1.y))] = (i,j)
                elif k == 4:
                    dists[(abs(b2.x-b1.x), abs(b2.z-b1.z), abs(b2.y-b1.y))] = (i,j)
                elif k == 5:
                    dists[(abs(b2.y-b1.y), abs(b2.z-b1.z), abs(b2.x-b1.x))] = (i,j)
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
    #assert sol2(*parse(test)) == 1924
    print(sol2(*parse(data)))
