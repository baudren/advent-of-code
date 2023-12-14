from rich import print
import streamlit as st
import os
import re

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

def move_grid_north(grid, bounds):
    moved = False
    for row in range(1, bounds[0]):
        for col in range(bounds[1]):
            key = (row, col)
            before = (row-1, col)
            if grid.get(key, '') == 'O' and before not in grid:
                grid[before] = 'O'
                del grid[key]
                moved = True
    return moved

def move_grid_south(grid, bounds):
    moved = False
    for row in range(bounds[0]-2, -1, -1):
        for col in range(bounds[1]):
            key = (row, col)
            before = (row+1, col)
            if grid.get(key, '') == 'O' and before not in grid:
                grid[before] = 'O'
                del grid[key]
                moved = True
    return moved

def move_grid_west(grid, bounds):
    moved = False
    for col in range(1, bounds[1]):
        for row in range(bounds[0]):
            key = (row, col)
            before = (row, col-1)
            if grid.get(key, '') == 'O' and before not in grid:
                grid[before] = 'O'
                del grid[key]
                moved = True
    return moved

def move_grid_east(grid, bounds):
    moved = False
    for col in range(bounds[1]-2, -1, -1):
        for row in range(bounds[0]):
            key = (row, col)
            before = (row, col+1)
            if grid.get(key, '') == 'O' and before not in grid:
                grid[before] = 'O'
                del grid[key]
                moved = True
    return moved

def sol1(data):
    grid = {}
    for row, line in enumerate(data):
        for col, c in enumerate(line):
            if c != '.':
                grid[(row, col)] = c
    while True:
        moved = move_grid_north(grid, (len(data), len(data[0])))
        if not moved:
            break
    total = 0
    for k, c in grid.items():
        if c == 'O':
            row, col = k
            total += (len(data)-row)
    return total

debug = False

def spin(grid, bounds):
    while move_grid_north(grid, bounds):
        pass
    while move_grid_west(grid, bounds):
        pass
    while move_grid_south(grid, bounds):
        pass
    while move_grid_east(grid, bounds):
        pass

def display_grid(grid, bounds):
    show = []
    for row in range(bounds[0]):
        line = "".join([grid.get((row, col), '.') for col in range(bounds[1])])
        show.append(line)
    st.code("\n".join(show))

def get_load(grid, bounds):
    total = 0
    for k, c in grid.items():
        if c == 'O':
            row, col = k
            total += bounds[0]-row
    return total

def find_pattern(values):
    string = ",".join([str(e) for e in values])
    found = False
    for i in range(2, len(values)//2):
        pattern = ",".join(list(reversed([str(values[len(values)-1-l]) for l in range(i)])))
        matches = [m.start() for m in re.finditer(pattern, string)]
        diffs = []
        for i, m in enumerate(matches[1:]):
            diffs.append(m-matches[i])
        if diffs and all((d == len(pattern)+1 for d in diffs)):
            found = True
            break
    return found, [int(e) for e in pattern.split(",")]
        

def sol2(data):
    grid = {}
    for row, line in enumerate(data):
        for col, c in enumerate(line):
            if c != '.':
                grid[(row, col)] = c
    bounds = (len(data), len(data[0]))
    values = []
    cycle = 0
    first_cycle = 0
    while True:
        spin(grid, bounds)
        value = get_load(grid, bounds)
        values.append(value)
        if cycle > 5:
            found, pattern = find_pattern(values)
            if found:
                first_cycle = cycle
                break
        cycle += 1
    index_burnout = first_cycle-len(pattern)*2
    return pattern[(pattern[(10-index_burnout-1)%len(pattern)]-index_burnout-2)%len(pattern)]

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
