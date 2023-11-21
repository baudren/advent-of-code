from rich import print
import streamlit as st
import os

from utils import *


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

def sol1(data):
    position = [0, 0]
    steps = {0: (0, 1), 1: (-1, 0), 2: (0, -1), 3: (1, 0)}
    direction = 0
    for step in data:
        if step[0] == 'L':
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
        position[0] = position[0] + steps[direction][0]*int(step[1:])
        position[1] = position[1] + steps[direction][1]*int(step[1:])
    return abs(position[0])+abs(position[1])


def sol2(data):
    position = [0, 0]
    visited = set()
    steps = {0: (0, 1), 1: (-1, 0), 2: (0, -1), 3: (1, 0)}
    direction = 0
    target = None
    for step in data:
        if target:
            break
        if step[0] == 'L':
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
        for i in range(int(step[1:])):
            position[0] += steps[direction][0]
            position[1] += steps[direction][1]
            if tuple(position) in visited:
                st.markdown("broke")
                target = position
                break
            else:
                visited.add(tuple(position))
    position = target
    return abs(position[0])+abs(position[1])


answer = None
st.session_state.file_exists = os.path.exists(get_filename())

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

basic_transform = line_to_str
st.markdown(data)
data = basic_transform(data)
st.markdown(data)
data_bk = data.copy()

st.markdown("### Part 1")
if select1 == 'data':
    st.markdown("#### Final answer")
else:
    st.markdown("#### Example")
    c1, c2 = st.columns(2)
    with c1:
        data = st.text_area('example 1')
        data = basic_transform(data)
    with c2:
        answer = st.text_input('answer 1')

if data:
    if answer:
        answer = int(answer)
        if sol1(data) != answer:
            st.markdown(f"**:red[Example failing: {sol1(data)=} != {answer}]**")
        else:
            st.markdown("**:green[All good]**")
    st.markdown(f"{data[:10]=}...")
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
        data = st.text_area('example 2')
        data = basic_transform(data)
    with c2:
        answer = st.text_input('answer 2')

if data:
    if answer:
        answer = int(answer)
        if sol2(data) != answer:
            st.markdown(f"**:red[Example failing: {sol2(data)=} != {answer}]**")
        else:
            st.markdown(":green[All good]")
    st.markdown(f"{sol2(data)=}")
