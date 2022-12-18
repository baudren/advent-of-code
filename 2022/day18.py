from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    data = file_to_lines(a)
    cubes = []
    px, py, pz = {}, {}, {}
    faces = 0
    for line in data:
        faces += 6
        cube = tuple([int(e) for e in line.split(",")])
        cubes.append(cube)
        x, y, z = cube
        xc, yc, zc = f"{y},{z}", f"{z},{x}", f"{x},{y}"
        if xc in px:
            if x-1 in px[xc]:
                faces -= 2
            if x+1 in px[xc]:
                faces -= 2
            px[xc].add(x)
        else:
            px[xc] = set((x,))
        if yc in py:
            if y-1 in py[yc]:
                faces -= 2
            if y+1 in py[yc]:
                faces -= 2
            py[yc].add(y)
        else:
            py[yc] = set((y,))
        if zc in pz:
            if z-1 in pz[zc]:
                faces -= 2
            if z+1 in pz[zc]:
                faces -= 2
            pz[zc].add(z)
        else:
            pz[zc] = set((z,))
    return faces


def sol2(a):
    data = file_to_lines(a)
    cubes = []
    px, py, pz = {}, {}, {}
    bx, by, bz = (10,-10), (10, -10), (10, -10)
    faces = 0
    for line in data:
        faces += 6
        cube = tuple([int(e) for e in line.split(",")])
        cubes.append(cube)
        x, y, z = cube
        if x < bx[0]:
            bx = (x, bx[1])
        elif x > bx[1]:
            bx = (bx[0], x)
        if y < by[0]:
            by = (y, by[1])
        elif y > by[1]:
            by = (by[0], y)
        if z < bz[0]:
            bz = (z, bz[1])
        elif z > bz[1]:
            bz = (bz[0], z)
        xc, yc, zc = f"{y},{z}", f"{z},{x}", f"{x},{y}"
        if xc in px:
            if x-1 in px[xc]:
                faces -= 2
            if x+1 in px[xc]:
                faces -= 2
            px[xc].add(x)
        else:
            px[xc] = set((x,))
        if yc in py:
            if y-1 in py[yc]:
                faces -= 2
            if y+1 in py[yc]:
                faces -= 2
            py[yc].add(y)
        else:
            py[yc] = set((y,))
        if zc in pz:
            if z-1 in pz[zc]:
                faces -= 2
            if z+1 in pz[zc]:
                faces -= 2
            pz[zc].add(z)
        else:
            pz[zc] = set((z,))
    # removing entirely enclosed droplets
    edges = (bx, by, bz)
    # there can be larger than one enclosed droplets, so removing two faces at a time, as long as part of a space
    # that is fully enclosed
    pockets = {}
    r_pockets = {}
    index = 0
    removed = set()
    for x in range(bx[0], bx[1]+1):
        for y in range(by[0], by[1]+1):
            for z in range(bz[0], bz[1]+1):
                xc, yc, zc = f"{y},{z}", f"{z},{x}", f"{x},{y}"
                if xc in px and yc in py and zc in pz:
                    if x not in px[xc] and y not in py[yc] and z not in pz[zc]:
                        if x-1 in px[xc] and y-1 in py[yc] and z-1 in pz[zc]:
                            pockets[index] = (x, y, z)
                            r_pockets[(x, y, z)] = index
                            index += 1
    points = px, py, pz
    faces -= explore_air_pockets(pockets, r_pockets, points, edges)

    # 3272 was wrong, 3278 was too high, 3266 was too high again, 2600 was wrong, 1042 was wrong also, 3473 was wrong
    return faces

def explore_air_pockets(pockets, r_pockets, points, edges):
    px, py, pz = points
    bx, by, bz = edges
    wrong_faces = 0
    for index in list(pockets.keys()):
        # flood fill from this location
        index_wrong_faces = 0
        if pockets[index] not in r_pockets:
            continue
        visited = set()
        frontier = set((pockets[index], ))
        trapped_bubble = True
        while frontier:
            elem = frontier.pop()
            visited.add(elem)
            x, y, z = elem
            xc, yc, zc = f"{y},{z}", f"{z},{x}", f"{x},{y}"
            if xc in px:
                if x-1 in px[xc]:
                    index_wrong_faces += 1
                if x+1 in px[xc]:
                    index_wrong_faces += 1
            if yc in py:
                if y-1 in py[yc]:
                    index_wrong_faces += 1
                if y+1 in py[yc]:
                    index_wrong_faces += 1
            if zc in pz:
                if z-1 in pz[zc]:
                    index_wrong_faces += 1
                if z+1 in pz[zc]:
                    index_wrong_faces += 1
            # add all neighbours that are empty, if I reach the boundary, remove this index from 
            neighbours = []
            for i in range(-1, 2, 2):
                neighbours.append((x+i, y, z))
                neighbours.append((x, y+i, z))
                neighbours.append((x, y, z+i))
            good_neighbours = []
            for neighbour in neighbours:
                x, y, z = neighbour
                xc, yc, zc = f"{y},{z}", f"{z},{x}", f"{x},{y}"
                if xc not in px or x not in px[xc]:
                    if yc not in py or y not in py[yc]:
                        if zc not in pz or z not in pz[zc]:
                            if neighbour not in visited:
                                if neighbour in [p for p in r_pockets if p != pockets[index]]:
                                    false_index = r_pockets.pop(neighbour)
                                frontier.add(neighbour)
                                good_neighbours.append(neighbour)
            for neighbour in good_neighbours:
                x, y, z = neighbour
                if x < bx[0] or x > bx[1]:
                    trapped_bubble = False
                    break
                if y < by[0] or y > by[1]:
                    trapped_bubble = False
                    break
                if z < bz[0] or z > bz[1]:
                    trapped_bubble = False
                    break
            if not trapped_bubble:
                break
        if trapped_bubble:
            wrong_faces += index_wrong_faces
    return wrong_faces

test = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
asserts_sol1 = {
        test: 64,
        }

asserts_sol2 = {
        test: 58,
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
