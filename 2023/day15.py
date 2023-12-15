from rich import print
import streamlit as st
import os

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = line_to_str

answer = None
st.session_state.file_exists = os.path.exists(get_filename())


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

def hash_(string):
    total = 0
    for i, c in enumerate(string):
        total += ord(c)
        total *= 17
        total = total % 256
    return total

def sol1(data):
    total = 0
    for elem in data:
        total += hash_(elem)
    return total


def sol2(data):
    total = 0
    hashmap = {}
    for elem in data:
        if '=' in elem:
            label, focal = elem.split('=')
            focal = int(focal)
            box = hash_(label)
            if box not in hashmap:
                hashmap[box] = {label: (focal, 1)}
            else:
                if label in hashmap[box]:
                    _, position = hashmap[box][label]
                    hashmap[box][label] = (focal, position)
                else:
                    hashmap[box][label] = (focal, len(hashmap[box])+1)
        else:
            label = elem[:-1]
            box = hash_(label)
            if box in hashmap:
                if label in hashmap[box]:
                    toto = hashmap[box].pop(label)
                    _, position = toto
                    new_hashmap_box = {}
                    for k, v in hashmap[box].items():
                        focal, pos = v
                        if pos > position:
                            new_hashmap_box[k] = (focal, pos-1)
                        else:
                            new_hashmap_box[k] = (focal, pos)
                    if not new_hashmap_box:
                        hashmap.pop(box)
                    else:
                        hashmap[box] = new_hashmap_box
    total = 0
    for k, v in hashmap.items():
        for vv in v.values():
            total += (k+1)*vv[0]*vv[1]
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
