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

Location = namedtuple('Location', 'x y z')
Velocity = namedtuple('Velocity', 'x y z')

import numpy as np

def sol1(data):
    trajectories = []
    test_area = (200000000000000, 400000000000000)
    for line in data:
        pos, vel = line.split(" @ ")
        pos = np.array([int(e) for e in pos.split(", ")][:-1])
        vel = np.array([int(e) for e in vel.split(", ")][:-1])
        trajectories.append((pos, vel))
    total = 0
    for i, trajectory in enumerate(trajectories):
        for j in range(i+1, len(trajectories)):
            pos_a, vel_a = trajectory
            xa, ya = pos_a[0], pos_a[1]
            xap, yap = vel_a[0], vel_a[1]
            pos_b, vel_b = trajectories[j]
            xb, yb = pos_b[0], pos_b[1]
            xbp, ybp = vel_b[0], vel_b[1]
            cross = xap*ybp-xbp*yap
            if cross != 0:
                a = (ybp*(xb-xa)+xbp*(ya-yb))/cross
                b = (yap*(xb-xa)+xap*(ya-yb))/cross
                intersect_x = xa+a*xap
                intersect_y = ya+a*yap
                if a >= 0 and b >= 0:
                    if test_area[0] <= intersect_x <= test_area[1]:
                        if test_area[0] <= intersect_y <= test_area[1]:
                            total += 1

    return total

debug = False
from numpy.linalg import solve

def sol2(data):
    trajectories = []
    for line in data:
        pos, vel = line.split(" @ ")
        pos = np.array([int(e) for e in pos.split(", ")])
        vel = np.array([int(e) for e in vel.split(", ")])
        trajectories.append((pos, vel))

    a, b, c = trajectories[0], trajectories[1], trajectories[2]
    pa, va = a
    xa, ya, za = pa
    xap, yap, zap = va
    pb, vb = b
    xb, yb, zb = pb
    xbp, ybp, zbp = vb
    pc, vc = c
    xc, yc, zc = pc
    xcp, ycp, zcp = vc

    A = np.matrix([
        [0      , zap-zbp, ybp-yap, 0    , zb-za, ya-yb],
        [zbp-zap, 0      , xap-xbp, za-zb, 0    , xb-xa],
        [yap-ybp, xbp-xap, 0      , yb-ya, xa-xb, 0    ],
        [0      , zap-zcp, ycp-yap, 0    , zc-za, ya-yc],
        [zcp-zap, 0      , xap-xcp, za-zc, 0    , xc-xa],
        [yap-ycp, xcp-xap, 0      , yc-ya, xa-xc, 0    ],
        ])
    B = np.array([
        [ya*zap-yb*zbp+zb*ybp-za*yap],
        [za*xap-zb*xbp+xb*zbp-xa*zap],
        [xa*yap-xb*ybp+yb*xbp-ya*xap],
        [ya*zap-yc*zcp+zc*ycp-za*yap],
        [za*xap-zc*xcp+xc*zcp-xa*zap],
        [xa*yap-xc*ycp+yc*xcp-ya*xap],
        ])
    sol = solve(A, B)
    s = sum(sol[:3])
    return int(s)



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
