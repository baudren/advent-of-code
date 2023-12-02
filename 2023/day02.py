from rich import print
import streamlit as st
import os
from functools import reduce
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
    rules = {'red': 12, 'green': 13, 'blue': 14}
    total = 0
    for line in data:
        game_nb = int(line.split(":")[0].split(" ")[1])
        possible = True
        for game in line.split(": ")[1].split("; "):
            for pair in game.split(", "):
                nb, color = pair.split()
                if int(nb) > rules[color]:
                    possible = False
                    break
        if possible:
            total += game_nb
    return total


def sol2(data):
    power = 0
    for line in data:
        powers = {'red': 0, 'green': 0, 'blue': 0}
        for game in line.split(": ")[1].split("; "):
            for pair in game.split(", "):
                nb, color = pair.split()
                if int(nb) > powers[color]:
                    powers[color] = int(nb)
        power += reduce(lambda x, y: x*y, powers.values())
    return power


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
