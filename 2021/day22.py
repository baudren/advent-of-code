from typing import List

def sol1(data):
    init_region = set()
    for instruction in data:
        on, xr, yr, zr = parse(instruction)
        if xr[0] <= -50:
            xr = (-50, xr[1])
        if xr[1] >= 50:
            xr = (xr[0], 50)
        if yr[0] <= -50:
            yr = (-50, yr[1])
        if yr[1] >= 50:
            yr = (yr[0], 50)
        if zr[0] <= -50:
            zr = (-50, zr[1])
        if zr[1] >= 50:
            zr = (zr[0], 50)
        for x in range(xr[0], xr[1]+1):
            for y in range(yr[0], yr[1]+1):
                for z in range(zr[0], zr[1]+1):
                    if (x,y,z) in init_region:
                        if not on: init_region.remove((x,y,z))
                    else:
                        if on: init_region.add((x,y,z))
    return len(init_region)


class Cuboid:
    def __init__(self, xr, yr, zr):
        self.xr = xr
        self.yr = yr
        self.zr = zr
    
    def __repr__(self):
        return f"Cuboid({self.xr}, {self.yr}, {self.zr})"
    
    def __eq__(self, other):
        return self.xr == other.xr and self.yr == other.yr and self.zr == other.zr

def sol2(data):
    cuboids = []
    for index, instruction in enumerate(data):
        on, xr, yr, zr = parse(instruction)
        if not cuboids:
            if on:
                cuboids.append(Cuboid(xr, yr, zr))
        else:
            next_cuboids = []
            overlapped = []
            added = []
            if on:
                to_add = [Cuboid(xr, yr, zr)]
                for i, cuboid in enumerate(list(cuboids)):
                    if len(to_add) == 0:
                        next_cuboids.append(cuboid)
                        added.append(i)
                    else:
                        overlaps = False
                        cuboid_should_be_kept = True
                        to_add_two = []
                        for j, new_cuboid in enumerate(list(to_add)):
                            if a_fully_inside_b(a=cuboid, b=new_cuboid):
                                overlaps = True
                                to_add_two.append(new_cuboid)
                            elif a_fully_inside_b(a=new_cuboid, b=cuboid):
                                pass  
                            else:
                                if b_intersects_with_a(a=cuboid, b=new_cuboid):
                                    splitted = add_b_to_a(a=cuboid, b=new_cuboid)
                                    to_add_two.extend(splitted)
                                else:
                                    to_add_two.append(new_cuboid)
                        to_add = to_add_two
                        if not overlaps:
                            next_cuboids.append(cuboid)
                            added.append(i)
                next_cuboids.extend(to_add)
                next_cuboids = list((c for i, c in enumerate(next_cuboids) if i not in overlapped))
            else:
                to_remove = Cuboid(xr, yr, zr)
                for i, cuboid in enumerate(list(cuboids)):
                    if a_fully_inside_b(a=cuboid, b=to_remove):
                        pass
                    else:
                        if b_intersects_with_a(a=to_remove, b=cuboid):
                            splitted = add_b_to_a(a=to_remove, b=cuboid)
                            if not splitted:
                                print("Here")
                                exit()
                            next_cuboids.extend(splitted)
                        else:
                            next_cuboids.append(cuboid)
            cuboids = next_cuboids
    return sum([volume(e) for e in cuboids])

def volume(a: Cuboid) -> int:
    return (a.xr[1]-a.xr[0]+1)*(a.yr[1]-a.yr[0]+1)*(a.zr[1]-a.zr[0]+1)

def a_fully_inside_b(a: Cuboid, b: Cuboid) -> bool:
    x = b.xr[0] <= a.xr[0] and b.xr[1] >= a.xr[1]
    y = b.yr[0] <= a.yr[0] and b.yr[1] >= a.yr[1]
    z = b.zr[0] <= a.zr[0] and b.zr[1] >= a.zr[1]
    return x and y and z

def b_intersects_with_a(a: Cuboid, b: Cuboid) -> bool:
    x = (a.xr[0] <= b.xr[0] <= a.xr[1]) or (a.xr[0] <= b.xr[1] <= a.xr[1]) or (b.xr[0] <= a.xr[0] and a.xr[1] <= b.xr[1])
    y = (a.yr[0] <= b.yr[0] <= a.yr[1]) or (a.yr[0] <= b.yr[1] <= a.yr[1]) or (b.yr[0] <= a.yr[0] and a.yr[1] <= b.yr[1])
    z = (a.zr[0] <= b.zr[0] <= a.zr[1]) or (a.zr[0] <= b.zr[1] <= a.zr[1]) or (b.zr[0] <= a.zr[0] and a.zr[1] <= b.zr[1])
    return x and y and z

# Trying to add cuboid b to cuboid a,
# or remove cuboid a from cuboid b
def add_b_to_a(a: Cuboid, b: Cuboid) -> List[Cuboid]:
    cuboids = []
    xr, yr, zr = list(b.xr), list(b.yr), list(b.zr)
    #print(xr, yr, zr)
    #print(a)
    #print(b)
    if b.xr[0] < a.xr[0]:
        cuboids.append(Cuboid((b.xr[0], a.xr[0]-1), b.yr, b.zr))
        xr[0] = a.xr[0]
    if b.xr[1] > a.xr[1]:
        cuboids.append(Cuboid((a.xr[1]+1, b.xr[1]), b.yr, b.zr))
        xr[1] = a.xr[1]
    if b.yr[0] < a.yr[0]:
        cuboids.append(Cuboid(tuple(xr), (b.yr[0], a.yr[0]-1), b.zr))
        yr[0] = a.yr[0]
    if b.yr[1] > a.yr[1]:
        cuboids.append(Cuboid(tuple(xr), (a.yr[1]+1, b.yr[1]), b.zr))
        yr[1] = a.yr[1]
    if b.zr[0] < a.zr[0]:
        cuboids.append(Cuboid(tuple(xr), tuple(yr), (b.zr[0], a.zr[0]-1)))
    if b.zr[1] > a.zr[1]:
        cuboids.append(Cuboid(tuple(xr), tuple(yr), (a.zr[1]+1, b.zr[1])))   
    return cuboids

def parse(instruction):
    on = "on" in instruction
    xyz = instruction.split(" ")[1]
    xr = tuple(int(e) for e in xyz.split(",")[0].split("=")[1].split(".."))
    yr = tuple(int(e) for e in xyz.split(",")[1].split("=")[1].split(".."))
    zr = tuple(int(e) for e in xyz.split(",")[2].split("=")[1].split(".."))
    return on, xr, yr, zr

if __name__ == "__main__":
    data = [e.strip() for e in open('day22.txt', 'r').readlines()]
    test = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".split("\n")
    assert sol1("""on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".split("\n")) == 39
    assert sol1(test) == 590784
    print(sol1(data))
    assert sol2("""on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""".split("\n")) == 2758514936282235
    print(sol2(data))
