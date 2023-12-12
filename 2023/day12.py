from rich import print
import streamlit as st
import os
import itertools

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

def count_damaged(row):
    clusters = []
    current_cluster = 0
    for c in row.values():
        if c == '.' and current_cluster:
            clusters.append(current_cluster)
            current_cluster = 0
        elif c == '#':
            current_cluster += 1
    if current_cluster:
        clusters.append(current_cluster)
    return clusters


def sol1(data):
    total = 0
    for line in data:
        row = {i:c for i, c in enumerate(line.split()[0])}
        row_original = row.copy()
        unknowns = {i:c for i, c in row.items() if c == '?'}
        clusters = [int(e) for e in line.split()[1].split(",")]
        permutations = itertools.product(['.', '#'], repeat=len(unknowns))
        for permutation in permutations:
            for index, key in enumerate(unknowns.keys()):
                row[key] = permutation[index]
            if count_damaged(row) == clusters:
                total += 1
    return total

# remove the ? where we know what they should be
def remove_unknown(row, unknowns, clusters):
    st.code(row)
    st.code(unknowns)
    st.code(clusters)

def sol2(data):
    total = 0
    for line in data:
        row_unfolded = '?'.join(line.split()[0] for _ in range(5))
        row = {i:c for i, c in enumerate(row_unfolded)}
        unknowns = {i:c for i, c in row.items() if c == '?'}
        clusters = [int(e) for e in line.split()[1].split(",")]*5
        remove_unknown(row, unknowns, clusters)
        #permutations = list(itertools.product(['.', '#'], repeat=len(unknowns)))
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
