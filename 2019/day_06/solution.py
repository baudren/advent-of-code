orbit_data = open('data.txt', 'r').read().splitlines()
# orbit_data = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L""".splitlines()
orbits = {}
for orbit in orbit_data:
    center, orbitting = orbit.split(')')
    orbits[orbitting] = center

def compute_length(orbits):
    total = 0
    for body in orbits:
        sum = 0
        test = body
        while True:
            if orbits[test] in orbits:
                sum += 1
                test = orbits[test]
            else:
                total += sum+1
                break
    return total

orbit_data = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
""".splitlines()
#orbits = {}
#for orbit in orbit_data:
#    center, orbitting = orbit.split(')')
#    orbits[orbitting] = center
def number_of_hops(orbits):
    source = orbits["YOU"]
    destination = orbits["SAN"]
    print(source, destination)
    # Find the path to CON for each
    source_path, destination_path = [source], [destination]
    while True:
        if orbits[source] in orbits:
            source_path.append(orbits[source])
            source = orbits[source]
        else:
            break
    while True:
        if orbits[destination] in orbits:
            destination_path.append(orbits[destination])
            destination = orbits[destination]
        else:
            break
    keys_in_destination_path = {}
    for body in destination_path:
        keys_in_destination_path[body] = True
    for body in source_path:
        if body in keys_in_destination_path:
            intersection = body
            break
    return source_path.index(intersection)+destination_path.index(intersection)

print(compute_length(orbits))
print(number_of_hops(orbits))