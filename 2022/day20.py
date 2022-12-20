from rich import print
from utils import load, file_to_lines, file_to_ints


def sol1(a):
    data = file_to_ints(a)
    original_coords = {k: data[k] for k in range(len(data))}
    coords = {k: k for k in range(len(data))}
    original = list(data)
    for k, v in original_coords.items():
        #print(data)
        #print(coords)
        position = coords[k]
        movement = data.pop(position)
        position = (position + movement) % len(data)
        data.insert(position, movement)
        coords = update_coords(coords, k, coords[k], position)
        #print(data)
        #print(coords)
        #input()
        #print(i, movement)
        #print(f"{data=}")
        #print()
        
    i0 = data.index(0)
    return data[(i0+1000)%len(data)]+data[(i0+2000)%len(data)]+data[(i0+3000)%len(data)]

def update_coords(coords, original_position, previous_position, position):
    new_coords = {}
    for k, v in coords.items():
        if k == original_position:
            new_coords[k] = position
        else:
            if v < previous_position:
                if v < position:
                    new_coords[k] = v
                else:
                    new_coords[k] = v+1
            else:
                if v <= position:
                    new_coords[k] = v-1
                else:
                    new_coords[k] = v
    return new_coords

def sol2(a):
    data = [811589153*e for e in file_to_ints(a)]
    original_coords = {k: data[k] for k in range(len(data))}
    coords = {k: k for k in range(len(data))}
    original = list(data)
    for i in range(10):
        for k, v in original_coords.items():
            #print(data)
            #print(coords)
            position = coords[k]
            movement = data.pop(position)
            position = (position + movement) % len(data)
            data.insert(position, movement)
            coords = update_coords(coords, k, coords[k], position)
            #print(data)
            #print(coords)
            #input()
            #print(i, movement)
            #print(f"{data=}")
            #print()
        
    i0 = data.index(0)
    return data[(i0+1000)%len(data)]+data[(i0+2000)%len(data)]+data[(i0+3000)%len(data)]

test = """1
2
-3
3
-2
0
4"""
asserts_sol1 = {
        test: 3
        }

asserts_sol2 = {
        test: 1623178306
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
