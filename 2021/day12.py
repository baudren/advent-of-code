def sol1(data):
    mapping = {}
    for line in data:
        a, b = line.split("-")
        if a in mapping:
            mapping[a].append(b)
        else:
            mapping[a] = [b]
        if b in mapping:
            mapping[b].append(a)
        else:
            mapping[b] = [a]
    paths = {}
    explore_rec(paths, mapping, [], 'start')
    return len(paths)

def explore_rec(paths, mapping, path, position):
    if position not in path:
        path.append(position)
    elif position == 'start':
        return
    elif position not in ['start', 'end'] and position.islower():
        return
    else:
        path.append(position)
    if position == 'end':
        paths[",".join(path)] = True
        return
    else:
        if position in mapping:
            for outcome in mapping[position]:
                explore_rec(paths, mapping, [p for p in path], outcome)
        else:
            return


def sol2(data):
    mapping = {}
    for line in data:
        a, b = line.split("-")
        if a in mapping:
            mapping[a].append(b)
        else:
            mapping[a] = [b]
        if b in mapping:
            mapping[b].append(a)
        else:
            mapping[b] = [a]
    paths = {}
    explore_rec_2(paths, mapping, [], 'start', False)
    return len(paths)

def explore_rec_2(paths, mapping, path, position, repeated):
    if position not in path:
        path.append(position)
    elif position == 'start':
        return
    elif position not in ['start', 'end'] and position.islower():
        # If there's no lowercase repeat already, this is allowed, else break
        if repeated:
            return
        else:
            repeated = True
            path.append(position)
    else:
        path.append(position)
    if position == 'end':
        paths[",".join(path)] = True
        return
    else:
        if position in mapping:
            for outcome in mapping[position]:
                explore_rec_2(paths, mapping, [p for p in path], outcome, repeated)
        else:
            return
if __name__ == "__main__":
    data = """vp-BY
ui-oo
kk-IY
ij-vp
oo-start
SP-ij
kg-uj
ij-UH
SP-end
oo-IY
SP-kk
SP-vp
ui-ij
UH-ui
ij-IY
start-ui
IY-ui
uj-ui
kk-oo
IY-start
end-vp
uj-UH
ij-kk
UH-end
UH-kk""".split("\n")
    test = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split("\n")
    assert sol1(test) == 10
    assert sol1("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".split("\n")) == 19
    assert sol1("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split("\n")) == 226
    print(sol1(data))
    assert sol2(test) == 36
    print(sol2(data))