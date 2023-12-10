from rich import print
import streamlit as st
import os
import math

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
    instructions = [0 if e == 'L' else 1 for e in data[0]]
    mapping = {}
    for line in data[2:]:
        src = line.split("=")[0].strip()
        a = line.split("=")[1].split(",")[0].strip()[1:]
        b = line.split("=")[1].split(",")[1].strip()[:-1]
        mapping[src] = (a, b)
    steps = 0
    current = 'AAA'
    while current != 'ZZZ':
        for instruction in instructions:
            steps += 1
            current = mapping[current][instruction]
            if current == 'ZZZ':
                break
    return steps

def is_finished(current):
    return all(e[-1] == 'Z' for e in current)

def get_value_after_step(instructions, mapping, start, count):
    step = 0
    dest = start
    while step < count:
        for index, instruction in enumerate(instructions):
            step += 1
            dest = mapping[dest][instruction]
            print(step, dest)
            if step >= count:
                break
    return dest


def sol2(data):
    instructions = [0 if e == 'L' else 1 for e in data[0]]
    mapping = {}
    for line in data[2:]:
        src = line.split("=")[0].strip()
        a = line.split("=")[1].split(",")[0].strip()[1:]
        b = line.split("=")[1].split(",")[1].strip()[:-1]
        mapping[src] = (a, b)
    current = []
    for key in mapping:
        if key[-1] == 'A':
            current.append(key)
    
    steps_total = {}
    visited = {}
    for c in current:
        visited[c] = {}
        visited[c][(c, 0)] = 0
        steps = 0
        cur = c
        should_break = False
        while not should_break:
            for index, instruction in enumerate(instructions):
                steps += 1
                cur = mapping[cur][instruction]
                if cur[-1] == 'Z':
                    steps_total[c] = steps
                    should_break = True
    keys_sorted = sorted(steps_total, key=steps_total.get)
    lcm = steps_total[keys_sorted[0]]
    for key in keys_sorted[1:]:
        lcm = math.lcm(lcm, steps_total[key])
    return lcm

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
