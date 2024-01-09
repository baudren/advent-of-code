from rich import print
import streamlit as st
import os

from utils import *

import networkx as nx

# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines

answer = None
st.session_state.file_exists = os.path.exists(get_filename())


with st.sidebar:
    select1 = st.selectbox("Part 1", ['examples', 'data'], key='select1')
    select2 = st.selectbox("Part 2", ['examples', 'data'], key='select2')

from copy import deepcopy
import random as rd

def shrink(links):
    new_links = {}
    # pop one element
    a = list(links.keys())[rd.randint(0,len(links)-1)]
    # add it to its most connected neighbor
    nn, ns = '', len(links[a])
    nnn, nns = '', len([a])
    for n in links[a]:
        if len(links[n]) > ns:
            nn, ns = n, len(links[n])
        if len(links[n]) < nns:
            nnn, nns = n, len(links[n])
    if not nn and not nnn: # all its neighbors are less connected, so doing it the other way around
        return links
    if not nn:
        nn = a
        ns = len(links[a])
        a = nnn
    for l, t in links.items():
        if l != a:
            if l == nn:
                ll = f"{nn}-{a}"
            else: ll = l
            if ll not in new_links:
                new_links[ll] = set([])
            for target in t:
                if target in [a, nn]:
                    tt = f"{nn}-{a}"
                else: tt = target
                if tt not in new_links:
                    new_links[tt] = set([])
                new_links[ll].add(tt)
                new_links[tt].add(ll)
    return new_links

def sol1(data):
    links = {}
    G = nx.Graph()
    for line in data:
        l, r = line.split(": ")
        for t in r.split():
            if l not in links:
                links[l] = set([])
            if t not in links:
                links[t] = set([])
            G.add_edge(t, l)
            links[l].add(t)
            links[t].add(l)

    cut_value, partition = nx.stoer_wagner(G)
    return len(partition[0])*len(partition[1])



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
st.markdown("Enjoy your rest!")
