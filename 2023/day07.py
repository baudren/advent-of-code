from rich import print
import streamlit as st
from collections import Counter
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

group_values = ['H', '1P', '2P', '3K', 'FH', '4K', '5K']

def get_group(hand):
    counter = Counter(hand)
    group = ''
    if max(counter.values()) == 5:
        group = '5K'
    elif max(counter.values()) == 4:
        group = '4K'
    elif 2 in counter.values() and 3 in counter.values():
        group = 'FH'
    elif max(counter.values()) == 3:
        group = '3K'
    elif list(counter.values()).count(2) == 2:
        group = '2P'
    elif max(counter.values()) == 2:
        group = '1P'
    else:
        group = 'H'
    return group


def get_ordered_keys(dict):
    keys = []
    for i in range(5,0,-1):
        for k,v in dict.items():
            if v == i:
                keys.append(k)
    return keys


def get_group2(hand):
    counter = Counter(hand)
    group = ''
    js = hand.count('J')
    if js:
        ordered_keys = get_ordered_keys(counter)
        if ordered_keys[0] != 'J':
            counter[ordered_keys[0]] += js
            counter["J"] -= js
        elif len(counter) > 1:
            counter[ordered_keys[1]] += js
            counter["J"] -= js
    if max(counter.values()) == 5:
        group = '5K'
    elif max(counter.values()) == 4:
        group = '4K'
    if not group:
        if 2 in counter.values() and 3 in counter.values():
            group = 'FH'
        elif max(counter.values()) == 3:
            group = '3K'
        elif list(counter.values()).count(2) == 2:
            group = '2P'
        elif max(counter.values()) == 2:
            group = '1P'
        else:
            group = 'H'
    return group

import functools
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
card_values_2 = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

def compare(x, y):
    for i in range(len(x)):
        a, b = card_values.index(x[i]), card_values.index(y[i])
        if a != b:
            return a - b
    return 0


def compare2(x, y):
    for i in range(len(x)):
        a, b = card_values_2.index(x[i]), card_values_2.index(y[i])
        if a != b:
            return a - b
    return 0

def order_group(hands):
    return sorted(hands, key=functools.cmp_to_key(compare))

def order_group2(hands):
    return sorted(hands, key=functools.cmp_to_key(compare2))


def sol1(data):
    bids = {}
    ranks = {}
    groups = {}

    for line in data:
        hand, bid = line.split()
        bid = int(bid)
        bids[hand] = bid
        ranks[hand] = 0
        group = get_group(hand)
        if group in groups:
            groups[group].append(hand)
        else:
            groups[group] = [hand, ]
    rank = 1
    for group in group_values:
        if group in groups:
            hands_in_group = order_group(groups[group])
            for i, hand in enumerate(hands_in_group):
                ranks[hand] = rank + i
            rank += i + 1
    total = 0
    for hand in ranks:
        total += ranks[hand]*bids[hand]
    return total

def sol2(data):
    bids = {}
    ranks = {}
    groups = {}

    for line in data:
        hand, bid = line.split()
        bid = int(bid)
        bids[hand] = bid
        ranks[hand] = 0
        group = get_group2(hand)
        if group in groups:
            groups[group].append(hand)
        else:
            groups[group] = [hand, ]
    rank = 1
    for group in group_values:
        if group in groups:
            hands_in_group = order_group2(groups[group])
            for i, hand in enumerate(hands_in_group):
                ranks[hand] = rank + i
            rank += i + 1
    st.code(ranks)
    total = 0
    for hand in ranks:
        total += ranks[hand]*bids[hand]
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
