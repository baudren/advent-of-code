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


directions = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U',
}

def get_polygon(data, offset, part_one=True):
    current = (0, 0)
    polygon = [(current[0]+offset[0], current[1]+offset[1]), ]
    for i, line in enumerate(data[:-1]):
        d, step, color = line.split()
        if part_one:
            step = int(step)
            next_dir = data[i+1].split()[0]
        else:
            step = int("0x"+color[2:-2], 16)
            d = directions[int(color[-2:-1])]
            next_dir = directions[int(data[i+1].split()[2][-2:-1])]
        if d == 'R':
            if next_dir == 'D':
                if offset == (0, 0): offset = (1, 0)
                elif offset == (1, 1): offset = (0, 1)
                elif offset == (0, 1): offset = offset
                elif offset == (1, 0): offset = offset
            else:
                if offset == (0, 0): offset = offset
                elif offset == (1, 1): offset = offset
                elif offset == (0, 1): offset = (1, 1)
                elif offset == (1, 0): offset = (0, 0)
            new_point = (current[0]+offset[0]+step, current[1]+offset[1])
            current = (current[0]+step, current[1])
        elif d == 'L':
            if next_dir == 'D':
                if offset == (0, 0): offset = offset
                elif offset == (1, 1): offset = offset
                elif offset == (0, 1): offset = (1, 1)
                elif offset == (1, 0): offset = (0, 0)
            else:
                if offset == (0, 0): offset = (1, 0)
                elif offset == (1, 1): offset = (0, 1)
                elif offset == (0, 1): offset = offset
                elif offset == (1, 0): offset = offset
            new_point = (current[0]+offset[0]-step, current[1]+offset[1])
            current = (current[0]-step, current[1])
        elif d == 'U':
            if next_dir == 'R':
                if offset == (0, 0): offset = offset
                elif offset == (1, 1): offset = offset
                elif offset == (0, 1): offset = (0, 0)
                elif offset == (1, 0): offset = (1, 1)
            else:
                if offset == (0, 0): offset = (0, 1)
                elif offset == (1, 1): offset = (1, 0)
                elif offset == (0, 1): offset = offset
                elif offset == (1, 0): offset = offset
            new_point = (current[0]+offset[0], current[1]+offset[1]-step)
            current = (current[0], current[1]-step)
        else:
            if next_dir == 'R':
                if offset == (0, 0): offset = (0, 1)
                elif offset == (1, 1): offset = (1, 0)
                elif offset == (0, 1): offset = offset
                elif offset == (1, 0): offset = offset
            else:
                if offset == (0, 0): offset = offset
                elif offset == (1, 1): offset = offset
                elif offset == (0, 1): offset = (0, 0)
                elif offset == (1, 0): offset = (1, 1)
            new_point = (current[0]+offset[0], current[1]+offset[1]+step)
            current = (current[0], current[1]+step)
        polygon.append(new_point)
    return polygon

def sol1(data):
    areas = []
    polygon = get_polygon(data, (0, 0), part_one=True)
    areas.append(get_area(polygon))
    polygon = get_polygon(data, (1, 1), part_one=True)
    areas.append(get_area(polygon))
    areas.append(get_area(polygon))
    return max(areas)

def get_area(polygon):
    polygon += [polygon[0], ]
    total = 0
    for i in range(len(polygon)-1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i+1]
        total += (x1*y2-x2*y1)
    return total // 2


def sol2(data):
    areas = []
    polygon = get_polygon(data, (0, 0), part_one=False)
    areas.append(get_area(polygon))
    polygon = get_polygon(data, (1, 1), part_one=False)
    areas.append(get_area(polygon))
    areas.append(get_area(polygon))
    return max(areas)


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
