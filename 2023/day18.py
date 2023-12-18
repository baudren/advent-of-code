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

def is_inside(grid, xx, yy, bounds):
    
    crosses = 0
    on_edge = 0
    points = [(i, yy) for i in range(bounds[0], xx+1)]
    for point in points:
        x, y = point
        if point in grid and not on_edge:
            if (x, y-1) in grid and (x, y+1) in grid:# and (x+1, y) not in grid:
                crosses += 1
            elif (x, y+1) in grid:
                on_edge = -1
            elif (x, y-1) in grid:
                on_edge = 1
        elif point in grid and on_edge != 0:
            if on_edge == 1 and (x, y+1) in grid:# and (x+1, y) not in grid:
                crosses += 1
                on_edge = 0
            elif on_edge == -1 and (x, y-1) in grid:# and (x+1, y) not in grid:
                crosses += 1
                on_edge = 0
    return crosses % 2 == 1


def dig(grid, bounds):
    to_dig = []
    for y in range(bounds[2], bounds[3]+1):
        for x in range(bounds[0], bounds[1]+1):
            if (x, y) not in grid:
                if is_inside(grid, x, y, bounds):
                    to_dig.append((x, y))
    for elem in to_dig:
        grid.add(elem)

def display_grid(grid, bounds):
    display = []
    for y in range(bounds[2], bounds[3]+1):
        line = []
        for x in range(bounds[0], bounds[1]+1):
            line.append('#' if (x, y) in grid else '.')
        display.append(''.join(line))
    st.code("\n".join(display))

directions = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U',
}
def sol1(data):
    current = (0, 0)
    grid = set([current])
    bounds = [0, 0, 0, 0]
    for line in data:
        d, step, color = line.split()
        step = int(step)
        for i in range(step):
            if d == 'R':
                current = (current[0]+1, current[1])
            elif d == 'L':
                current = (current[0]-1, current[1])
            elif d == 'U':
                current = (current[0], current[1]-1)
            else:
                current = (current[0], current[1]+1)
            grid.add(current)
            if current[0] < bounds[0]:
                bounds[0] = current[0]
            if current[0] > bounds[1]:
                bounds[1] = current[0]
            if current[1] < bounds[2]:
                bounds[2] = current[1]
            if current[1] > bounds[3]:
                bounds[3] = current[1]
    dig(grid, bounds)
    
    return len(grid)


def flood_fill(grid, node):
    if node in grid:
        return
    grid.add(node)
    x, y = node
    flood_fill((x-1, y))
    flood_fill((x+1, y))
    flood_fill((x, y-1))
    flood_fill((x, y+1))


def dig2(grid, bounds):
    for x in range(bounds[0], bounds[1]+1):
        if (x, 0) not in grid and is_inside(grid, x, 0, bounds):
            start_flood_fill = (x, 0)
            break
    flood_fill(grid, start_flood_fill)

def sol2(data):
    current = (0, 0)
    grid = set([current])
    bounds = [0, 0, 0, 0]
    for line in data:
        d, step, color = line.split()
        step = int("0x"+color[2:-2], 16)
        d = directions[int(color[-2:-1])]
        if d == 'R':
            if current[0]+step > bounds[1]:
                bounds[1] = current[0]+step
            grid.update([(current[0]+1+i, current[1]) for i in range(step)])
        elif d == 'L':
            if current[0]-step < bounds[0]:
                bounds[0] = current[0]-step
            grid.update([(current[0]-1-i, current[1]) for i in range(step)])
        elif d == 'U':
            if current[1]-step < bounds[2]:
                bounds[2] = current[1]-step
            grid.update([(current[0], current[1]-1-i) for i in range(step)])
        else:
            if current[1]+step > bounds[3]:
                bounds[2] = current[1]+step
            grid.update([(current[0], current[1]+1+i) for i in range(step)])
    st.code("start")
    dig2(grid, bounds)
    
    return len(grid)


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
