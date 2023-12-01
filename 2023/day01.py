from rich import print
import streamlit as st
import os

from utils import *

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())

digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')


def sol1(data):
    total = 0
    for line in data:
        start, stop = 0, 0
        for c in line:
            try:
                start = int(c)
                break
            except:
                pass
        for c in line[::-1]:
            try:
                stop = int(c)
                break
            except:
                pass
        total += int(f"{start}{stop}")
    return total


def sol2(data):
    new_data = []
    for line in data:
        line = line.replace("twone", "twoone")
        line = line.replace("eightwo", "eighttwo")
        line = line.replace("oneight", "oneeight")
        modified = True
        while modified:
            modified = False
            digit_places = {}
            for k, v in digits.items():
                digit_places[k] = line.find(k)
            digit_places = {k: v for k, v in sorted(digit_places.items(), key=lambda item: item[1])}
            for k, v in digit_places.items():
                if v != -1:
                    line = line.replace(k, digits[k], 1)
                    modified = True
        new_data.append(line)
    return sol1(new_data)


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
