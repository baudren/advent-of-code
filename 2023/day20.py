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

def compute_state(modules):
    total = 0
    for i, key in enumerate(list(modules.keys())):
        if len(modules[key]) > 1:
            pass#total += 2**(i+1) * modules[key]["state"]

    return total

def handle_signal(modules, f, c, module, signal, source):
    if module in modules:
        if module in f:
            if signal == 0:
                modules[module]["state"] = 0 if modules[module]["state"] else 1
                return 1 if modules[module]["state"] else -1
            else:
                return 0
        elif module in c:
            modules[module]["state"][source] = signal
            if sum(modules[module]["state"].values()) == len(modules[module]["state"]):
                return -1
            else:
                return 1
        else: # broadcaster
            return 1 if signal else -1
    return 0


def propagate(modules, flip_flops, conjunctions):
    lows, highs = 0, 0
    found = False
    to_process = [("broadcaster", 0, "button")]
    while to_process:
        new_process = []
        for elem in to_process:
            module, pulse, source = elem
            #st.code((source, '-high' if pulse else '-low', '->', module))
            if pulse:
                highs += 1
            else:
                lows += 1
            signal = handle_signal(modules, flip_flops, conjunctions, module, pulse, source)
            if signal != 0:
                for target in modules[module]["targets"]:
                    if signal == -1 and target == 'rx':
                        found = True
                    new_process.append((target, 0 if signal == -1 else 1, module))
        to_process = new_process
    return lows, highs, found

def sol1(data):
    modules = {}
    flip_flops = set([])
    connects = {}
    conjunctions = set([])
    for line in data:
        name, target = line.split(" -> ")
        if '%' in name:
            # start off state
            modules[name[1:]] = {"targets": target.split(", "), "state": 0}
            flip_flops.add(name[1:])
            for e in target.split(", "):
                if e in connects:
                    connects[e].append(name[1:])
                else:
                    connects[e] = [name[1:], ]
        elif '&' in name:
            # initialize
            conjunctions.add(name[1:])
            modules[name[1:]] = {"targets": target.split(", "), "state": {}}
            for e in target.split(", "):
                if e in connects:
                    connects[e].append(name[1:])
                else:
                    connects[e] = [name[1:], ]
        else:
            modules[name] = {"targets": target.split(", ")}
    for c in conjunctions:
        for in_ in connects[c]:
            modules[c]["state"][in_] = 0
    total = 0
    lows, highs = 0, 0
    for _ in range(1000):
        l, h, _ = propagate(modules, flip_flops, conjunctions)
        lows += l
        highs += h
    return lows*highs


def sol2(data):
    modules = {}
    flip_flops = set([])
    connects = {}
    conjunctions = set([])
    for line in data:
        name, target = line.split(" -> ")
        if '%' in name:
            # start off state
            modules[name[1:]] = {"targets": target.split(", "), "state": 0}
            flip_flops.add(name[1:])
            for e in target.split(", "):
                if e in connects:
                    connects[e].append(name[1:])
                else:
                    connects[e] = [name[1:], ]
        elif '&' in name:
            # initialize
            conjunctions.add(name[1:])
            modules[name[1:]] = {"targets": target.split(", "), "state": {}}
            for e in target.split(", "):
                if e in connects:
                    connects[e].append(name[1:])
                else:
                    connects[e] = [name[1:], ]
        else:
            modules[name] = {"targets": target.split(", ")}
    for c in conjunctions:
        for in_ in connects[c]:
            modules[c]["state"][in_] = 0
    chain = {}
    current = "rx"
    count = 0
    while current is not None and count < 100:
        st.code((f"parents of {current}", connects[current]))
        for parent in connects[current]:
            chain[parent] = modules[parent].get("state", {})
            if parent == 'broadcast':
                break
        new_current = None
        for parent in connects[current]:
            if parent not in chain:
                new_current = parrent
        #current = connects[current][0]
        count += 1
        current = new_current

        #break
    button_presses = 0
    while True:
        l, h, found = propagate(modules, flip_flops, conjunctions)
        button_presses += 1
        break
        #if button_presses % 100000 == 0:
        #    st.code(button_presses)
        if found:
            break
    return button_presses


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
