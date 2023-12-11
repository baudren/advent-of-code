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

def sol1(data):
    galaxies = []
    rows = set()
    columns = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((x, y))
                rows.add(y)
                columns.add(x)
    new_data = []
    width = len(data[0])+len(data[0])-len(columns)
    for y, line in enumerate(data):
        new_line = []
        if y not in rows:
            new_data.append("".join(['.' for _ in range(width)]))
            new_data.append("".join(['.' for _ in range(width)]))
        else:
            for x, c in enumerate(line):
                if x not in columns:
                    new_line.extend(['.', '.'])
                else:
                    new_line.append(c)
            new_data.append("".join(new_line))
    galaxies = []
    data = new_data
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((x, y))

    total = 0
    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies)):
            ax, ay = galaxies[i]
            bx, by = galaxies[j]
            total += abs(by-ay)+abs(bx-ax)
    return total


def sol2(data):
    galaxies = []
    rows = set()
    cols = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((x, y))
                rows.add(y)
                cols.add(x)
    empty_rows = set()
    empty_cols = set()
    factor = 1000000
    for y in range(len(data)):
        if y not in rows:
            empty_rows.add(y)
    for x in range(len(data[0])):
        if x not in cols:
            empty_cols.add(x)
    new_galaxies = []
    for galaxy in galaxies:
        x, y = galaxy
        empty_cols_before = len([c for c in empty_cols if c < x])
        empty_rows_before = len([r for r in empty_rows if r < y])
        new_gal = (x+factor*empty_cols_before-empty_cols_before, y+factor*empty_rows_before-empty_rows_before)
        new_galaxies.append(new_gal)

    galaxies = new_galaxies
    total = 0
    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies)):
            ax, ay = galaxies[i]
            bx, by = galaxies[j]
            total += abs(by-ay)+abs(bx-ax)
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
