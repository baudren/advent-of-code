#from rich import print
import streamlit as st
import os
import functools

from utils import *
import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

@functools.cache
def get_neighbors(pos, walls, bounds):
    neighbors = []
    x, y = pos
    if (x-1, y) not in walls and x-1 >= 0:
        neighbors.append((x-1, y))
    if (x+1, y) not in walls and x+1 < bounds[0]:
        neighbors.append((x+1, y))
    if (x, y-1) not in walls and y-1 >= 0:
        neighbors.append((x, y-1))
    if (x, y+1) not in walls and y+1 < bounds[1]:
        neighbors.append((x, y+1))
    return tuple(neighbors)


@functools.cache
def get_neighbors_2(pos, walls, bounds):
    neighbors = []
    x, y = pos
    if x > 0:
        if (x-1, y) not in walls:
            neighbors.append((x-1, y))
    else:
        neighbors.append((x-1, y))
    if x < bounds[0]-2:
        if (x+1, y) not in walls:
            neighbors.append((x+1, y))
    else:
        neighbors.append((x+1, y))
    if y > 0:
        if (x, y-1) not in walls:
            neighbors.append((x, y-1))
    else:
        neighbors.append((x, y-1))
    if y < bounds[0] -2:
        if (x, y+1) not in walls:
            neighbors.append((x, y+1))
    else:
        neighbors.append((x, y+1))
    return tuple(neighbors)

def sol1(data):
    walls = set([])
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'S':
                start = (x, y)
    walls = frozenset(walls)
    bounds = (len(data[0]), len(data))

    frontier = Queue()
    frontier.put(start)
    reached_odd = set([])
    reached_even = set([])
    reached_even.add(start)
    
    for step in range(1, 64+1):
        new_frontier = Queue()
        while not frontier.empty():
            current = frontier.get()
            for next in get_neighbors_2(current, walls, bounds):
                if step % 2 == 0:
                    if next not in reached_even:
                        new_frontier.put(next)
                        reached_even.add(next)
                else:
                    if next not in reached_odd:
                        new_frontier.put(next)
                        reached_odd.add(next)
        frontier = new_frontier
    total = 0
    if step % 2 == 0:
        total += len(reached_even)
    else:
        total += len(reached_odd)
    return total


def sol2(data):
    walls = set([])
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'S':
                start = (x, y)
    walls = frozenset(walls)
    bounds = (len(data[0]), len(data))

    frontier = Queue()
    frontier.put(start)
    reached_odd = set([])
    reached_even = set([])
    reached_even.add(start)
    #return 0
    size = 65+131*2
    values = []
    for step in range(1, size+1):
        new_frontier = Queue()
        while not frontier.empty():
            current = frontier.get()
            x, y = current
            for next in get_neighbors_2((x % bounds[0], y % bounds[1]), walls, bounds):
                xx, yy = next
                new_pos = x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy
                if step % 2 == 0:
                    if new_pos not in reached_even:
                        new_frontier.put(new_pos)
                        reached_even.add(new_pos)
                else:
                    if new_pos not in reached_odd:
                        new_frontier.put(new_pos)
                        reached_odd.add(new_pos)
        frontier = new_frontier
        if step % 2 == 0:
            values.append(len(reached_even))
        else:
            values.append(len(reached_odd))

    start = 65-1 # because my steps start at one....

    xs = [start+x*131 for x in range(3)]
    first_diff = values[xs[1]]-values[xs[0]]
    add = values[xs[2]]-values[xs[1]] - first_diff
    i = (26501365-start)//131
    return values[start]+i*first_diff+((i-1)*i//2)*add


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
