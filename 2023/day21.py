from rich import print
import streamlit as st
import os
import functools

from utils import *

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
        if (bounds[0]-1, y) not in walls:
            neighbors.append((x-1, y))
    if x < bounds[0]-2:
        if (x+1, y) not in walls:
            neighbors.append((x+1, y))
    else:
        if (0, y) not in walls:
            neighbors.append((x+1, y))
    if y > 0:
        if (x, y-1) not in walls:
            neighbors.append((x, y-1))
    else:
        if (x, bounds[1]-1) not in walls:
            neighbors.append((x, y-1))
    if y < bounds[0] -2:
        if (x, y+1) not in walls:
            neighbors.append((x, y+1))
    else:
        if (x, 0) not in walls:
            neighbors.append((x, y+1))
    return tuple(neighbors)

def sol1(data):
    positions = set([])
    walls = set([])
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'S':
                positions.add((x, y))
    walls = frozenset(walls)
    bounds = (len(data[0]), len(data))
    for step in range(64):
        new_positions = set()
        for pos in positions:
            #st.code(pos)
            for n in get_neighbors(pos, walls, bounds):
                new_positions.add(n)
        positions = new_positions

    total = 0
    return len(positions)


def sol2(data):
    positions = set([])
    walls = set([])
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'S':
                positions.add((x, y))
    walls = frozenset(walls)
    bounds = (len(data[0]), len(data))

    original = frozenset(positions)
    
    # then this loop seeds the neighbor quadrants in a defined way
    # List of active quadrants, starting with the first one, coordinates 0, 0
    active = set([(0, 0), ])
    inactive = {}
    positions = original.copy()
    known = {(0, 0): original}
    st.code((active, inactive, positions, known))
    for step in range(100):
        debug = False
        new_positions = set()
        for pos in positions:
            x, y = pos
            # map to first quadrant
            for n in get_neighbors_2((x % bounds[0], y % bounds[1]), walls, bounds):
                xx, yy = n
                xxx, yyy = x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy
                new_pos = xxx, yyy
                quadrant = (xxx//bounds[0], yyy//bounds[1])
                if debug: st.code((new_pos, quadrant))
                if quadrant[0] != 0:
                    if debug: st.code((new_pos, quadrant))
                #if debug: print(("neighbors", n))
                #if debug: print((x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy))
                new_positions.add((x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy))
        positions = new_positions

    total = 0
    return len(positions)

# Find loop for one quadrant
    # known = set([frozenset(positions), ])
    # lengths = [len(positions), ]
    # for step in range(1000):
    #     debug = step % 100 == 0
    #     new_positions = set()
    #     for pos in positions:
    #         x, y = pos
    #         # map to first quadrant
    #         for n in get_neighbors((x % bounds[0], y % bounds[1]), walls, bounds):
    #             xx, yy = n
    #             #if debug: print(("neighbors", n))
    #             #if debug: print((x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy))
    #             new_positions.add((x//bounds[0]*bounds[0]+xx, y//bounds[1]*bounds[1]+yy))
    #     if debug: st.code((step, len(new_positions)))
    #     #if debug: print(new_positions)
    #     positions = new_positions
    #     if positions in known:
    #         st.code("found a loop for step "+str(step))
    #         st.code((len(positions), lengths[-1]))
    #         break
    #     else:
    #         known.add(frozenset(positions))
    #         lengths.append(len(positions))
    

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
