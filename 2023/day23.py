from rich import print
import streamlit as st
import collections
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

Location = namedtuple('Location', 'x y')

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    def empty(self) -> bool:
        return not self.elements
    def put(self, x):
        self.elements.append(x)
    def get(self):
        return self.elements.popleft()

class Graph:
    def __init__(self):
        self.elements = set([])
        self.linked = {}
        self.rev_linked = {}

def get_neighbors_down(point, points):
    n = []
    x, y = point
    if points.get((x, y-1), '') in ['^', '.']:
        n.append((x, y-1))
    if points.get((x, y+1), '') in ['v', '.']:
        n.append((x, y+1))
    if points.get((x-1, y), '') in ['<', '.']:
        n.append((x-1, y))
    if points.get((x+1, y), '') in ['>', '.']:
        n.append((x+1, y))
    return n

def get_neighbors(point, points):
    n = []
    x, y = point
    if points.get((x, y-1), ''):
        n.append((x, y-1))
    if points.get((x, y+1), ''):
        n.append((x, y+1))
    if points.get((x-1, y), ''):
        n.append((x-1, y))
    if points.get((x+1, y), ''):
        n.append((x+1, y))
    return n

from copy import deepcopy

def go_down(orig_point, point, distance, points, visited, graph, end):
    if orig_point not in graph:
        graph[orig_point] = {}
    frontier = Queue()
    frontier.put((point, distance))
    found_split = False
    while not frontier.empty():
        current, d = frontier.get()
        if current == end:
            graph[orig_point][current] = d
            break
        visited.add(current)
        neighbors = get_neighbors(current, points)
        neighbors = [n for n in neighbors if n not in visited]
        if len(neighbors) == 1:
            if neighbors[0] in get_neighbors_down(current, points):
                frontier.put((neighbors[0], d+1))
        elif len(neighbors) > 1:
            # split
            graph[orig_point][current] = d
            found_split = True
            break
        else:
            break
    if found_split:
        if current in graph: # this means we already added this point in the graph, and went downstram
            return
        for neighbor in get_neighbors_down(current, points):
            v = deepcopy(visited)
            go_down(current, neighbor, 1, points, v, graph, end)

def go(orig_point, point, distance, points, visited, graph, end, splits):
    if orig_point not in graph:
        graph[orig_point] = {}
    frontier = Queue()
    frontier.put((point, distance))
    found_split = False
    while not frontier.empty():
        current, d = frontier.get()
        if current == end:
            graph[orig_point][current] = d
            break
        visited.add(current)
        neighbors = get_neighbors(current, points)
        neighbors = [n for n in neighbors if n not in visited]
        if len(neighbors) == 1:
            frontier.put((neighbors[0], d+1))
        elif len(neighbors) > 1:
            # split
            graph[orig_point][current] = d
            if current not in graph:
                graph[current] = {}
            graph[current][orig_point] = d
            found_split = True
            break
        else:
            break
    if found_split:
        if current in splits:
            return
        splits.add(current)
        for neighbor in neighbors:
            v = deepcopy(visited)
            go(current, neighbor, 1, points, v, graph, end, splits)

def display(points, graph, bounds):
    d = []
    for y in range(bounds[1]):
        line = []
        for x in range(bounds[0]):
            if (x, y) in graph: line.append('X')
            else: line.append(points.get((x, y), '#'))
        d.append("".join(line))
    st.code("\n".join(d))

def sol1(data):
    points = {}
    graph = {}
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c != '#':
                points[(x, y)] = c
                if y == 0:
                    start = (x, y)
                elif y == len(data)-1:
                    end = (x, y)
    # Define grid of intersections between start and end
    # with a BFS
    visited = set([])
    go_down(start, start, 0, points, visited, graph, end)
    frontier = Queue()
    frontier.put((start, 0, []))
    paths = []
    while not frontier.empty():
        current, d, visited = frontier.get()
        visited.append(current)
        #st.code((current, visited))
        if current == end:
            paths.append(d)
        for neighbor, dd in graph.get(current, {}).items():
            if neighbor not in visited:
                v = deepcopy(visited)
                frontier.put((neighbor, d+dd, v))

    return max(paths)


# sol > 6674
def sol2(data):
    points = {}
    graph = {}
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c != '#':
                points[(x, y)] = c
                if y == 0:
                    start = (x, y)
                elif y == len(data)-1:
                    end = (x, y)
    # Define grid of intersections between start and end
    # with a BFS
    visited = set([])
    splits = set([])
    go(start, start, 0, points, visited, graph, end, splits)
    st.code("Found all splits")
    frontier = PriorityQueue()
    frontier.put((start, 0, frozenset()), 0)
    paths = []
    current_max = 0
    while not frontier.empty():
        current, d, visited = frontier.get()
        v = set(visited)
        v.add(current)
        #st.code((current, visited))
        if current == end:
            if d > current_max:
                current_max = d
                st.code(current_max)
        else:
            for neighbor, dd in graph.get(current, {}).items():
                if neighbor not in v:
                    frontier.put((neighbor, d+dd, frozenset(v)), -d-dd)

    return current_max


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
