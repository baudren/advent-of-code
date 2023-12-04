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
    total = 0
    for line in data:
        score = 0
        winning_str = line.split(" | ")[0].split(": ")[1]
        winning = [int(e) for e in winning_str.split()]
        own = [int(e) for e in line.split(" | ")[1].split()]
        for number in winning:
            if number in own:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        total += score
    return total


def sol2(data):
    cards = {}
    for n in range(len(data)):
        cards[n+1] = 1
    print("wh")
    for line in data:
        score = 0

        card_number = int(line.split(":")[0].split()[1])
        winning_str = line.split(" | ")[0].split(": ")[1]
        winning = [int(e) for e in winning_str.split()]
        own = [int(e) for e in line.split(" | ")[1].split()]
        for number in winning:
            if number in own:
                if score == 0:
                    score = 1
                else:
                    score += 1
        st.markdown(card_number)
        if score > 0:
            for _ in range(cards[card_number]):
                for i in range(int(card_number)+1, int(card_number)+score+1):
                    cards[i] += 1
    total = 0
    for v in cards.values():
        total += v
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
