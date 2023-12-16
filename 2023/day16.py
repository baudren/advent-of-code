import copy
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

beams = ['>', '<', 'v', '^']

def evolve(grid, start, beam, bounds, debug=False):
    if debug: st.code((start, beam, "started"))
    if start[0] < 0 or start[0] >= bounds[0]:
        return
    if start[1] < 0 or start[1] >= bounds[1]:
        return

    x, y = start
    if beam == '>':
        while True:
            pos = (x, y)
            if debug: st.code(pos)
            if x >= bounds[0]:
                break
            if pos in grid:
                if beam in grid[pos]:
                    break
                if '|' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x, y+1), 'v', bounds, debug)
                    evolve(grid, (x, y-1), '^', bounds, debug)
                    break
                if '\\' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x, y+1), 'v', bounds, debug)
                    break
                if '/' in grid[pos]:
                    if debug: st.code("He")
                    grid[pos].add(beam)
                    evolve(grid, (x, y-1), '^', bounds, debug)
                    break
                else:
                    if debug: st.code("H")
                    grid[pos].add(beam)
            else:
                grid[pos] = set([beam])
            x += 1
    elif beam == '<':
        while True:
            pos = (x, y)
            if x < 0:
                break
            if pos in grid:
                if beam in grid[pos]:
                    break
                if '|' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x, y+1), 'v', bounds, debug)
                    evolve(grid, (x, y-1), '^', bounds, debug)
                    break
                if '\\' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x, y-1), '^', bounds, debug)
                    break
                if '/' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x, y+1), 'v', bounds, debug)
                    break
                else:
                    grid[pos].add(beam)
            else:
                grid[pos] = set([beam])
            x -= 1
    elif beam == 'v':
        while True:
            pos = (x, y)
            if y >= bounds[1]:
                break
            if pos in grid:
                if beam in grid[pos]:
                    break
                if '-' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x+1, y), '>', bounds, debug)
                    evolve(grid, (x-1, y), '<', bounds, debug)
                    break
                if '\\' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x+1, y), '>', bounds, debug)
                    break
                if '/' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x-1, y), '<', bounds, debug)
                    break
                else:
                    grid[pos].add(beam)
            else:
                grid[pos] = set([beam])
            y += 1
    elif beam == '^':
        while True:
            pos = (x, y)
            if y < 0:
                break
            if pos in grid:
                if beam in grid[pos]:
                    break
                if '-' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x+1, y), '>', bounds, debug)
                    evolve(grid, (x-1, y), '<', bounds, debug)
                    break
                if '\\' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x-1, y), '<', bounds, debug)
                    break
                if '/' in grid[pos]:
                    grid[pos].add(beam)
                    evolve(grid, (x+1, y), '>', bounds, debug)
                    break
                else:
                    grid[pos].add(beam)
            else:
                grid[pos] = set([beam])
            y -= 1
    if debug: st.code((start, beam, "finished"))

def print_grid(grid, bounds):
    display = []
    for y in range(bounds[1]):
        line = []
        for x in range(bounds[0]):
            if any([beam in grid.get((x, y), '') for beam in beams]):
                line.append('#')
            else:
                line.append('.')
        display.append("".join(line))
    st.code("\n".join(display))

def compute_total(grid):
    total = 0
    for k, v in grid.items():
        if any([beam in v for beam in beams]):
            total += 1
    return total


def sol1(data):
    grid = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != '.':
                grid[(x, y)] = set([char])
    bounds = (len(data[0]), len(data))
    evolve(grid, (0, 0), '>', bounds)
    return compute_total(grid)


def sol2(data):
    grid = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != '.':
                grid[(x, y)] = set([char])
    bounds = (len(data[0]), len(data))

    totals = []
    for x in range(bounds[0]):
        grid_copy = copy.deepcopy(grid)
        evolve(grid_copy, (x, 0), 'v', bounds)
        total = compute_total(grid_copy)
        totals.append(total)
    for y in range(bounds[1]):
        grid_copy = copy.deepcopy(grid)
        evolve(grid_copy, (0, y), '>', bounds)
        totals.append(compute_total(grid_copy))
    for x in range(bounds[0]):
        grid_copy = copy.deepcopy(grid)
        evolve(grid_copy, (x, bounds[1]-1), '^', bounds)
        totals.append(compute_total(grid_copy))
    for y in range(bounds[1]):
        grid_copy = copy.deepcopy(grid)
        evolve(grid_copy, (bounds[0]-1, y), '<', bounds)
        totals.append(compute_total(grid_copy))
    return max(totals)


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
