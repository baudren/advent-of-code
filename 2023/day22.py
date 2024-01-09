from copy import deepcopy
from rich import print
import streamlit as st
import os

from utils import *
import collections

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

Location = namedtuple('Location', 'x y z')


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class Brick:
    def __init__(self, start, end, label):
        self.s = start
        self.e = end
        self.label = label

    def at_xyz(self, x, y, z):
        if x >= self.s.x and x <= self.e.x:
            if y >= self.s.y and y <= self.e.y:
                if z >= self.s.z and z <= self.e.z:
                    return True
        return False

    def extent(self):
        x = self.e.x - self.s.x
        y = self.e.y - self.s.y
        z = self.e.z - self.s.z
        return Location(x,y,z)

    def __repr__(self):
        return self.label

def move(brick, bricks, blocks, is_blocked):
    if brick.s.z == 1:
        return False
    z = brick.s.z - 1
    blocked = False
    e = brick.extent()
    if e.x != 0:
        for other in bricks:
            if other != brick:
                for x in range(brick.s.x, brick.e.x+1):
                    if other.at_xyz(x, brick.s.y, z):
                        blocked = True
                        if other not in blocks:
                            blocks[other] = set()
                        blocks[other].add(brick)
                        if brick not in is_blocked:
                            is_blocked[brick] = set()
                        is_blocked[brick].add(other)

    elif e.y != 0:
        for other in bricks:
            if other != brick:
                for y in range(brick.s.y, brick.e.y+1):
                    if other.at_xyz(brick.s.x, y, z):
                        blocked = True
                        if other not in blocks:
                            blocks[other] = set()
                        blocks[other].add(brick)
                        if brick not in is_blocked:
                            is_blocked[brick] = set()
                        is_blocked[brick].add(other)
    else:
        for other in bricks:
            if other != brick:
                if other.at_xyz(brick.s.x, brick.s.y, z):
                    blocked = True
                    if other not in blocks:
                        blocks[other] = set()
                    blocks[other].add(brick)
                    if brick not in is_blocked:
                        is_blocked[brick] = set()
                    is_blocked[brick].add(other)

    if not blocked:
        new_s = Location(brick.s.x, brick.s.y, brick.s.z-1)
        new_e = Location(brick.e.x, brick.e.y, brick.e.z-1)
        brick.s = new_s
        brick.e = new_e
    return not blocked

def sol1(data):
    bricks = []
    lowest_z = {}
    label_i = 0
    for line in data:
        s, e = line.split("~")
        label = chr(65+label_i)
        start = Location(*[int(i) for i in s.split(",")])
        end = Location(*[int(i) for i in e.split(",")])
        brick = Brick(start, end, label)
        bricks.append(brick)
        if start.z not in lowest_z:
            lowest_z[start.z] = []
        lowest_z[start.z].append(brick)
        label_i += 1
        #st.code((start, end))

    # falling
    blocks, is_blocked = {}, {}
    for z in range(max(list(lowest_z.keys()))+1):
        for brick in lowest_z.get(z, []):
            moved = move(brick, bricks, blocks, is_blocked)
            while moved:
                moved = move(brick, bricks, blocks, is_blocked)

    total = 0
    for brick in bricks:
        if brick not in blocks:
            total += 1
        else:
            ok = True
            for other in blocks[brick]:
                if len(is_blocked[other]) == 1:
                    ok = False
            if ok:
                total += 1
    return total


def sol2(data):
    bricks = []
    bricks_d = {}
    lowest_z = {}
    label_i = 0
    for i, line in enumerate(data):
        s, e = line.split("~")
        label = chr(65+label_i)
        start = Location(*[int(i) for i in s.split(",")])
        end = Location(*[int(i) for i in e.split(",")])
        brick = Brick(start, end, label)
        bricks.append(brick)
        bricks_d[id(brick)] = brick
        if start.z not in lowest_z:
            lowest_z[start.z] = []
        lowest_z[start.z].append(i)
        label_i += 1

    # falling
    blocks, is_blocked = {}, {}
    for z in range(max(list(lowest_z.keys()))+1):
        for index in lowest_z.get(z, []):
            brick = bricks[index]
            moved = move(brick, bricks, blocks, is_blocked)
            while moved:
                moved = move(brick, bricks, blocks, is_blocked)

    # starting from everything is fallen, remove one, and make everything fall
    total = 0
    for i, brick in enumerate(bricks):
        new_bricks = deepcopy(bricks)
        new_bricks.pop(i)
        lowest_z = {}
        for b in new_bricks:
            if b.s.z not in lowest_z:
                lowest_z[b.s.z] = []
            lowest_z[b.s.z].append(b)
        for z in range(max(list(lowest_z.keys()))+1):
            for b in lowest_z.get(z, []):
                moved = move(b, new_bricks, blocks, is_blocked)
                if moved:
                    total += 1
                while moved:
                    moved = move(b, new_bricks, blocks, is_blocked)
    return total


if not st.session_state.file_exists:
    data = st.text_area("input text from site")
    if data:
        write_to_file(data)
        st.rerun()
    st.markdown("This should disappear after execution")
    st.divider()

else:
    data = load()

if not data:
    st.stop()

data = basic_transform(data)
data_bk = data.copy()

st.markdown("### Part 1")
if select1 == 'data':
    st.markdown("#### Final answer")
else:
    st.markdown("#### Example")
    c1, c2 = st.columns(2)
    with c1:
        value = st.session_state.get("example1_data", "")
        data = st.text_area('example 1', value=value)
        if data:
            st.session_state["example1_data"] = data
        data = basic_transform(data)
    with c2:
        value = st.session_state.get("example1_answer", "")
        answer = st.text_input('answer 1', value=value)
        if answer:
            st.session_state["example1_answer"] = answer
if data:
    if answer:
        answer = int(answer)
        if sol1(data) != answer:
            st.markdown(f"**:red[Example failing: {sol1(data)=} != {answer}]**")
        else:
            st.markdown("**:green[All good]**")
    st.markdown(f"{sol1(data)=}")


st.divider()
st.markdown("### Part 2")
answer = None
data = data_bk
if select2 == 'data':
    st.markdown("#### Final answer")
else:
    st.markdown("#### Example")
    c1, c2 = st.columns(2)
    with c1:
        value = st.session_state.get("example2_data", "")
        data = st.text_area('example 2', value=value)
        if data:
            st.session_state["example2_data"] = data
        data = basic_transform(data)
    with c2:
        value = st.session_state.get("example2_answer", "")
        answer = st.text_input('answer 2', value=value)
        if answer:
            st.session_state["example2_answer"] = answer

if data:
    if answer:
        answer = int(answer)
        if sol2(data) != answer:
            st.markdown(f"**:red[Example failing: {sol2(data)=} != {answer}]**")
        else:
            st.markdown(":green[All good]")
    st.markdown(f"{sol2(data)=}")
