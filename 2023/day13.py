from rich import print
import streamlit as st
import os

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())

debug = False

with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

def find_col_symmetry(pattern, already=0):
    match = True
    for col in range(1,len(pattern[0])):
        # try each row
        match = True
        for row in pattern:
            start = row[col-1::-1]
            end = row[col:]
            if len(start) < len(end):
                if not end.startswith(start):
                    match = False
                    break
            else:
                if not start.startswith(end):
                    match = False
                    break
        if not already and match:
            break
        if match and col != already:
            break
    return col if match else 0

def find_row_symmetry(pattern, already=0):
    match = True
    cols = []

    for row in range(1,len(pattern)):
        # try each column
        match = True
        for col in range(len(pattern[0])):
            start = "".join([e[col] for e in pattern][row-1::-1])
            end = "".join([e[col] for e in pattern][row:])
            if len(start) < len(end):
                if not end.startswith(start):
                    match = False
                    break
            else:
                if not start.startswith(end):
                    match = False
                    break
        if not already and match:
            break
        if match and row != already:
            break
    return row if match else 0

def sol1(data):
    total = 0
    patterns = []
    pattern = []
    for line in data:
        if line:
            pattern.append(line)
        else:
            patterns.append(pattern)
            pattern = []
    patterns.append(pattern)
    for i, pattern in enumerate(patterns):
        col = find_col_symmetry(pattern)
        if col:
            total += col
        else:
            row = find_row_symmetry(pattern)
            if row == 0:
                break
            total += 100*row
    return total

def change_smudge(pattern, col=0, row=0):
    value = 0
    if debug: st.code(("original", col, row))
    if debug: st.code("\n".join(pattern))
    for i, r in enumerate(pattern):
        for j, c in enumerate(r):
            new_row = [c for c in r]
            new_row[j] = '.' if c == '#' else '#'
            new_row = "".join(new_row)
            new_pattern = pattern[:i]+[new_row]+pattern[i+1:]
            if debug: st.code("\n".join(new_pattern))
            new_col = find_col_symmetry(new_pattern, col)
            if col and new_col and new_col != col:
                value = new_col
                break
            if row and new_col:
                value = new_col
                break
            if not new_col or new_col == col:
                new_row = find_row_symmetry(new_pattern, row)
                if col and new_row:
                    value = 100*new_row
                    break
                if row and new_row and new_row != row:
                    value = 100*new_row
                    break
        if value:
            break
    return value

def sol2(data):
    total = 0
    patterns = []
    pattern = []
    for line in data:
        if line:
            pattern.append(line)
        else:
            patterns.append(pattern)
            pattern = []
    patterns.append(pattern)
    for i, pattern in enumerate(patterns):
        col = find_col_symmetry(pattern)
        value = 0
        if col:
            value = change_smudge(pattern, col=col)
        else:
            row = find_row_symmetry(pattern)
            value = change_smudge(pattern, row=row)
        if not value:
            st.code((i, "error"))
        total += value
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
