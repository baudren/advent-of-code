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

symbols = ['*', '+', '#', '$', '/', '@', '&', '=', '%', '-']

# not 547476
def should_be_included(row, start, stop, data):
    valid = False
    if start > 0:
        if data[row][start-1] not in [str(c) for c in range(10)] and data[row][start-1] != '.':
            valid = True
    if stop < len(data[0])-1:
        if data[row][stop+1] not in [str(c) for c in range(10)] and data[row][stop+1] != '.':
            valid = True
    if row > 0:
        for i in range(start - 1 if start > 0 else start, stop + 2 if stop < len(data[0]) - 1 else stop + 1):
            if data[row-1][i] not in [str(c) for c in range(10)] and data[row-1][i] != '.':
                valid = True
                break
    if row < len(data)-1:
        for i in range(start - 1 if start > 0 else start, stop + 2 if stop < len(data[0]) - 1 else stop + 1):
            if data[row+1][i] not in [str(c) for c in range(10)] and data[row+1][i] != '.':
                valid = True
                break
    return valid

def should_be_included_2(row, start, stop, data):
    valid = False
    symbol = (0, 0)
    if start > 0:
        if data[row][start-1] not in [str(c) for c in range(10)] and data[row][start-1] != '.':
            valid = True
            symbol = (data[row][start-1], (row, start-1))
    if not valid and stop < len(data[0])-1:
        if data[row][stop+1] not in [str(c) for c in range(10)] and data[row][stop+1] != '.':
            valid = True
            symbol = (data[row][stop+1], (row, stop+1))
    if not valid and row > 0:
        for i in range(start - 1 if start > 0 else start, stop + 2 if stop < len(data[0]) - 1 else stop + 1):
            if data[row-1][i] not in [str(c) for c in range(10)] and data[row-1][i] != '.':
                valid = True
                symbol = (data[row-1][i], (row-1, i))
                break
    if not valid and row < len(data)-1:
        for i in range(start - 1 if start > 0 else start, stop + 2 if stop < len(data[0]) - 1 else stop + 1):
            if data[row+1][i] not in [str(c) for c in range(10)] and data[row+1][i] != '.':
                valid = True
                symbol = (data[row+1][i], (row+1, i))
                break
    
    return valid, symbol

def sol1(data):
    total = 0
    numbers = []
    for row, line in enumerate(data):
        number, start, stop = [], 0, 0
        for column, char in enumerate(line):
            if char in ([str(c) for c in range(10)]):
                if not number:
                    start = column
                number.append(char)
            else:
                if number:
                    stop = column - 1
                    if should_be_included(row, start, stop, data):
                        numbers.append(int(''.join(number)))
                    number, start, stop = [], 0, 0
        if number:
            stop = column - 1
            if should_be_included(row, start, stop, data):
                numbers.append(int(''.join(number)))
            number, start, stop = [], 0, 0
    return sum(numbers)


def sol2(data):
    total = 0
    gears = {}
    for row, line in enumerate(data):
        number, start, stop = [], 0, 0
        for column, char in enumerate(line):
            if char in ([str(c) for c in range(10)]):
                if not number:
                    start = column
                number.append(char)
            else:
                if number:
                    number = int(''.join(number))
                    stop = column - 1
                    should, symbol = should_be_included_2(row, start, stop, data)
                    s, loc = symbol
                    if s == '*':
                        if loc in gears:
                            gears[loc].append(number)
                        else:
                            gears[loc] = [number, ]
                    number, start, stop = [], 0, 0
        if number:
            number = int(''.join(number))
            stop = column - 1
            should, symbol = should_be_included_2(row, start, stop, data)
            s, loc = symbol
            if s == '*':
                if loc in gears:
                    gears[loc].append()
                else:
                    gears[loc] = (number)
            number, start, stop = [], 0, 0
    for gear in gears:
        if len(gears[gear]) == 2:
            total += gears[gear][0]*gears[gear][1]
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
