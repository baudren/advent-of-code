from rich import print
from utils import load, file_to_lines, file_to_ints
from functools import reduce
import operator

def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

def add_sizes_rec(files, location):
    # if no more subfolders, sum all
    has_subfolder = False
    sub_total = 0
    for k, v in getFromDict(files, location).items():
        if type(v) == type({}):
            has_subfolder = True
            add_sizes_rec(files, location+[k])
            sub_total += getFromDict(files, location+[k, "size"])
    total = 0
    for v in getFromDict(files, location).values():
        if type(v) == type(1):
            total += v
    total += sub_total
    setInDict(files, location+["size"], total)

def explore_sizes_rec(files, location, value):
    size = getFromDict(files, location+["size"])
    for k, v in getFromDict(files, location).items():
        if type(v) == type({}):
            explore_sizes_rec(files, location+[k], value)
    if size <= 100000:
        value.append(size)
    
def explore_sizes_rec_2(files, location, missing, value):
    size = getFromDict(files, location+["size"])
    for k, v in getFromDict(files, location).items():
        if type(v) == type({}):
            explore_sizes_rec_2(files, location+[k], missing, value)
    if size >= missing:
        value.append(size)
    

def sol1(a):
    data = file_to_lines(a)
    files = {}
    current_directory = []
    for line in data:
        if " cd " in line and not ".." in line:
            if not current_directory:
                current_directory.append(line.split(" cd ")[1])
                files[current_directory[-1]] = {}
            else:
                current_directory.append(line.split(" cd ")[1])
                setInDict(files, current_directory, {})
        elif " cd .." in line:
            current_directory.pop()
        elif not "dir" in line and not "$" in line:
            # file
            size, filename = line.split(" ")
            size = int(size)
            setInDict(files, current_directory+[filename], size)

    add_sizes_rec(files, ["/"])
    total = []
    explore_sizes_rec(files, ["/"], total)
    return sum(total)


def sol2(a):
    data = file_to_lines(a)
    files = {}
    current_directory = []
    for line in data:
        if " cd " in line and not ".." in line:
            if not current_directory:
                current_directory.append(line.split(" cd ")[1])
                files[current_directory[-1]] = {}
            else:
                current_directory.append(line.split(" cd ")[1])
                setInDict(files, current_directory, {})
        elif " cd .." in line:
            current_directory.pop()
        elif not "dir" in line and not "$" in line:
            # file
            size, filename = line.split(" ")
            size = int(size)
            setInDict(files, current_directory+[filename], size)

    add_sizes_rec(files, ["/"])
    missing = 70000000-getFromDict(files, ["/", "size"])
    fit = []
    explore_sizes_rec_2(files, ["/"], 30000000-missing, fit)

    return min(fit)


asserts_sol1 = {
        """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""": 95437
        }

asserts_sol2 = {
        """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""": 24933642
        }

if __name__ == "__main__":
    data = load()
    for d,expected in asserts_sol1.items():
        assert sol1(d) == expected, f"'sol1({d})' expected '{expected}' but was '{sol1(d)}'"
    print(f"\n{sol1(data)=}\n")
    for d,expected in asserts_sol2.items():
        assert sol2(d) == expected, f"'sol2({d})' expected '{expected}' but was '{sol2(d)}'"
    print(f"\n{sol2(data)=}\n")
