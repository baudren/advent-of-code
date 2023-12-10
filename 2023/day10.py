from rich import print
import streamlit as st
import os

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')


def generate_neighbours(point, max_x, max_y):
    x, y = point
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y))
    if x < max_x:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < max_y:
        neighbors.append((x, y+1))
    return neighbors


def are_connected(a, b, structure):
    if structure[b] == '.':
        return False
    ax, ay = a
    bx, by = b
    sa = structure[a]
    sb = structure[b]
    if ax == bx:
        if by < ay:
            return sa in ['S', '|', 'L', 'J'] and sb in ['S', '|', '7', 'F']
        else:
            return sb in ['S', '|', 'L', 'J'] and sa in ['S', '|', '7', 'F']
    else:
        if bx > ax:
            return sa in ['S', '-', 'L', 'F'] and sb in ['S', '-', 'J', '7']
        else:
            return sb in ['S', '-', 'L', 'F'] and sa in ['S', '-', 'J', '7']

def sol1(data):
    # Find the starting point
    structure = {}
    max_x = len(data[0])-1
    max_y = len(data)-1
    start = (0, 0)
    for y, line in enumerate(data):
        if "S" in line:
            start = (line.index("S"), y)
        for x, c in enumerate(line):
            structure[(x, y)] = c
    loop = set([start,])
    current = start
    while True:
        found_neighbor = False
        for neighbor in generate_neighbours(current, max_x, max_y):
            if are_connected(current, neighbor, structure) and neighbor not in loop:
                loop.add(neighbor)
                current = neighbor
                found_neighbor = True
                break
        if not found_neighbor:
            break
    return len(loop)//2


def get_intersect_to_edge(start, max_x, max_y, structure, loop):
    x, y = start
    if x < max_x//2:
        points = [(i, y) for i in range(x+1)]
    else:
        points = [(i, y) for i in range(x, max_x+1)]
    crosses = 0
    on_edge = 0
    for point in points:
        if point in loop and not on_edge:
            if structure[point] == '|':
                crosses += 1
            elif structure[point] == 'F':
                on_edge = -1
            elif structure[point] == 'L':
                on_edge = 1
        elif point in loop and on_edge != 0:
            if on_edge == 1 and structure[point] == '7':
                crosses += 1
                on_edge = 0
            elif on_edge == -1 and structure[point] == 'J':
                crosses += 1
                on_edge = 0
            elif structure[point] != '-':
                on_edge = 0
    return crosses


def sol2(data):
    # Find the starting point
    structure = {}
    max_x = len(data[0])-1
    max_y = len(data)-1

    start = (0, 0)
    for y, line in enumerate(data):
        if "S" in line:
            start = (line.index("S"), y)
        for x, c in enumerate(line):
            structure[(x, y)] = c
    loop = set([start,])
    current = start
    while True:
        found_neighbor = False
        for neighbor in generate_neighbours(current, max_x, max_y):
            if are_connected(current, neighbor, structure) and neighbor not in loop:
                loop.add(neighbor)
                current = neighbor
                found_neighbor = True
                break
        if not found_neighbor:
            break
    structure[start] = "-"  # hardcoded for my input...
    # draw a line to an edge, if your intersection count is odd, you're inside
    inside = 0
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if structure[(x, y)] == '.' or (x, y) not in loop:
                if get_intersect_to_edge((x, y), max_x, max_y, structure, loop) % 2 == 1:
                    inside += 1
    return inside


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
