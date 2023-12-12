from math import factorial as f
from rich import print
import streamlit as st
import os
import itertools

from utils import *

debug = False
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
    for i, line in enumerate(data):
        row = [c for c in line.split()[0]]
        clusters = [int(e) for e in line.split()[1].split(",")]
        value = count_perm_rec(row, clusters)
        total += value
    return total

def get_first_real_cluster(row):
    cluster = 0
    for i, c in enumerate(row):
        if cluster and c == '.':
            break
        elif c == '#':
            cluster += 1
    return cluster


def count_perm_cont(row, clusters):
    gaps = len(clusters)-1
    total_len = sum(clusters)+gaps
    if len(row) < total_len:
        return 0
    elif total_len == len(row):
        return 1
    k = len(row) - total_len  # number of freedom
    n = len(clusters)+1  # number of slots to put this freedom
    # count with repetitions
    return f(n+k-1)//(f(k)*f(n-1))


def get_max_cluster(row):
    clusters = []
    cluster = 0
    for i, c in enumerate(row):
        if c == '#':
            cluster += 1
        else:
            if cluster:
                clusters.append(cluster)
                cluster = 0
    if cluster:
        clusters.append(cluster)
    if clusters:
        return max(clusters)
    else:
        return 0

def get_min_cluster(row):
    clusters = []
    cluster = 0
    for i, c in enumerate(row):
        if not cluster and c in ['#', '?']:
            cluster += 1
        if cluster and c in ['?', '.']:
            clusters.append(cluster)
            if c == '?' and i > 0 and row[i-1] != '#':
                cluster = 1
            else:
                cluster = 0
    if cluster:
        clusters.append(cluster)
    return min(clusters) if clusters else 0


count_perm_rec_cache = {}
def count_perm_rec(row, clusters):
    key = (tuple(row), tuple(clusters))
    row = row.copy()
    if debug: st.code(("".join(row), clusters))
    if key in count_perm_rec_cache:
        return count_perm_rec_cache[key]
    cd, cp, ci = row.count('#'), row.count('.'), row.count('?')
    # if no more clusters, there is only one choice (all .), except if there are still # in the row
    total = 0
    if not clusters:
        if '#' in row:
            total = 0
        else:
            total = 1
    elif set(row) == set(['?']):
        total = count_perm_cont(row, clusters)
    elif cd > sum(clusters):
        total = 0
    elif cd+ci < sum(clusters):
        total = 0
    else:
        if get_max_cluster(row) > max(clusters):
            total = 0
        elif get_min_cluster(row) > min(clusters):
            total = 0
        elif len(row) == clusters[0] and cd+ci == clusters[0]:
            total = 1
        else:
            cluster = clusters[0]
            tested = []
            for i in range(len(row)+1-cluster):
                if row[i] == '.':
                    continue
                row_mod = row.copy()
                if debug: st.code("".join(row_mod))
                for j in range(i):
                    if row[j] == '?':
                        row_mod[j] = '.'
                for j in range(cluster+1):
                    if i+j < len(row) and row[i+j] == '?':
                        if j < cluster:
                            row_mod[i+j] = '#'
                        else:
                            row_mod[i+j] = '.'
                if debug: st.code(f"Testing index {i}: {''.join(row_mod)}, {cluster}({clusters})")
                if row_mod in tested:
                    value = 0
                    break
                else:
                    tested.append(row_mod)
                # count the # until i, if > cluster, break
                if debug: st.code(("".join(row_mod[i:i+cluster+1]), row_mod[i:i+cluster+1].count('#')))
                if row_mod[i:i+cluster].count('#') != cluster:
                    value = 0
                elif row_mod[:i+cluster].count('#') > cluster:
                    value = 0
                    break
                elif get_first_real_cluster(row_mod) != cluster:
                    value = 0
                else:
                    if debug: st.code("tested: "+"\n        ".join(["".join(t) for t in tested]))
                    value = count_perm_rec(row_mod[i+cluster+1:], clusters[1:])
                if debug: st.code(f"Finished testing index {i}: {''.join(row_mod)}, {cluster}({clusters}) -> {value}")
                total += value
                #if row[i] == '#': 
                #    st.code("HERE")
                #    break
    if debug: st.code(("".join(row), clusters, total))
    count_perm_rec_cache[key] = total
    return total

def sol2(data):
    total = 0
    for i, line in enumerate(data):
        row_unfolded = '?'.join(line.split()[0] for _ in range(5))
        row = [c for c in row_unfolded]
        clusters = [int(e) for e in line.split()[1].split(",")]*5
        value = count_perm_rec(row, clusters)
        total += value
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
