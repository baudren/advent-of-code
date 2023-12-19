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

Part = namedtuple('Part', 'x m a s')
debug = False
def apply_workflow(workflows, part, workflow):
    if debug: st.code((part, workflow))
    for rule in workflows[workflow]:
        if debug: st.code(rule)
        if rule == 'A':
            return True
        elif rule == 'R':
            return False
        elif '>' not in rule and '<' not in rule:
            return apply_workflow(workflows, part, rule)
        else:
            cond, target = rule.split(":")
            if eval(f"part.{cond}"):
                if target == 'A':
                    return True
                elif target == 'R':
                    return False
                else:
                    return apply_workflow(workflows, part, target)
            else:
                continue


def sol1(data):
    workflows = {}
    workflow_data, parts_data = "\n".join(data).split("\n\n")
    for line in workflow_data.split("\n"):
        name, rule = line.split("{")
        workflows[name] = rule[:-1].split(",")
    parts = []
    for line in parts_data.split("\n"):
        xp, mp, ap, sp = line[1:-1].split(",")
        x = int(xp.split("=")[1])
        m = int(mp.split("=")[1])
        a = int(ap.split("=")[1])
        s = int(sp.split("=")[1])
        parts.append(Part(x,m,a,s))
    accepted_parts = []
    for part in parts:
        accepted = apply_workflow(workflows, part, "in")
        if accepted:
            accepted_parts.append(part)
    st.code(accepted_parts)
    total = 0
    for part in accepted_parts:
        total += part.x+part.m+part.a+part.s
    return total

from copy import deepcopy

def split_shape(shape, cond):
    # return a, b where a is the shape where cond is true, b is the shape False
    key = cond.split("<")[0] if "<" in cond else cond.split(">")[0]
    accepted = []
    refused = []
    value = int(cond.split("<")[1] if "<" in cond else cond.split(">")[1])
    for elem in shape[key]:
        if '<' in cond:
            if elem[0] < value and elem[1] < value:
                accepted.append((elem[0], elem[1]))
            elif elem[0] < value and elem[1] >= value:
                accepted.append((elem[0], value-1))
                refused.append((value, elem[1]))
            else:
                refused.append((elem[0], elem[1]))
        else:
            if elem[0] > value and elem[1] > value:
                accepted.append((elem[0], elem[1]))
            elif elem[1] > value and elem[0] < value:
                refused.append((elem[0], value))
                accepted.append((value+1, elem[1]))
            else:
                refused.append((elem[0], elem[1]))
    accepted_shape = deepcopy(shape)
    accepted_shape[key] = tuple(accepted)
    refused_shape = deepcopy(shape)
    refused_shape[key] = tuple(refused)
    return accepted_shape, refused_shape


def process_shapes(workflows, shapes, workflow):
    valid_shapes = []
    for shape in shapes:
        current_shape = deepcopy(shape)
        for rule in workflows[workflow]:
            if debug: st.code(rule)
            # must split current_shape
            if '<' in rule or '>' in rule:
                cond, target = rule.split(":")
                a, current_shape = split_shape(current_shape, cond)
                if target == 'A':
                    valid_shapes.append(a)
                elif target == 'R':
                    pass
                else:
                    valid_shapes.extend(process_shapes(workflows, [a,], target))
            elif rule == 'A':
                valid_shapes.append(current_shape)
                break
            elif rule == 'R':
                break
            else:
                valid_shapes.extend(process_shapes(workflows, [current_shape,], rule))
    return valid_shapes


def sol2(data):
    workflows = {}
    workflow_data, parts_data = "\n".join(data).split("\n\n")
    for line in workflow_data.split("\n"):
        name, rule = line.split("{")
        workflows[name] = rule[:-1].split(",")
    total = 0
    max_ = 4000
    shapes = [{
        "x": ((1, max_), ),
        "m": ((1, max_), ),
        "a": ((1, max_), ),
        "s": ((1, max_), ),
    }, ]
    accepted_shapes = process_shapes(workflows, shapes, 'in')
    total = 1
    for shape in accepted_shapes:
        shape_total = 1
        for v in shape.values():
            dir_total = 0
            for e in v:
                dir_total += e[1]+1-e[0]
            shape_total *= dir_total
        total += shape_total
    return total-1


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
