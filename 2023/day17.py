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

Location2D = namedtuple('Location2D', 'x y')

class Graph(BaseGraph):
    def __init__(self, grid, bounds):
        self.grid = grid
        self.width = bounds[0]
        self.height = bounds[1]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def neighbors(self, node, direction):
        x, y = node
        dx, dy = direction
        neighbors = []
        if dx > 0:
            if dx < 3:
                neighbors.append(Location2D(x+1, y))
            neighbors.extend([Location2D(x, y+1), Location2D(x, y-1)])
        elif dx < 0:
            if dx > -3:
                neighbors.append(Location2D(x-1, y))
            neighbors.extend([Location2D(x, y+1), Location2D(x, y-1)])
        elif dy > 0:
            if dy < 3:
                neighbors.append(Location2D(x, y+1))
            neighbors.extend([Location2D(x+1, y), Location2D(x-1, y)])
        elif dy < 0:
            if dy > -3:
                neighbors.append(Location2D(x, y-1))
            neighbors.extend([Location2D(x+1, y), Location2D(x-1, y)])
        else:
            neighbors.extend([Location2D(1, 0), Location2D(0, 1)])
        results = filter(self.in_bounds, neighbors)
        return results

    def cost(self, node):
        return self.grid[node]    


class UltraGraph(BaseGraph):
    def __init__(self, grid, bounds):
        self.grid = grid
        self.width = bounds[0]
        self.height = bounds[1]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def neighbors(self, node, direction):
        x, y = node
        dx, dy = direction
        neighbors = []
        if dx > 0:
            if dx < 10:
                neighbors.append(Location2D(x+1, y))
            if dx > 3:
                neighbors.extend([Location2D(x, y+1), Location2D(x, y-1)])
        elif dx < 0:
            if dx > -10:
                neighbors.append(Location2D(x-1, y))
            if dx < -3:
                neighbors.extend([Location2D(x, y+1), Location2D(x, y-1)])
        elif dy > 0:
            if dy < 10:
                neighbors.append(Location2D(x, y+1))
            if dy > 3:
                neighbors.extend([Location2D(x+1, y), Location2D(x-1, y)])
        elif dy < 0:
            if dy > -10:
                neighbors.append(Location2D(x, y-1))
            if dy < -3:
                neighbors.extend([Location2D(x+1, y), Location2D(x-1, y)])
        else:
            neighbors.extend([Location2D(1, 0), Location2D(0, 1)])
        results = filter(self.in_bounds, neighbors)
        return results

    def cost(self, node):
        return self.grid[node]    

def heuristic(a, b):
    return abs(a.x-b.x)+abs(a.y-b.y)

# heuristic is a function that takes two arguments, returns a value to estimate the distance to the goal
def a_star_search(graph , start, goal, heuristic):
    frontier = PriorityQueue()
    frontier.put((start, (0, 0)), 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = {start: None}
    cost_so_far[start] = {start: 0}

    while not frontier.empty():
        current, direction = frontier.get()
        if current == goal:
            break
        for next in graph.neighbors(current, direction):
            new_direction = (next.x-current.x, next.y-current.y)
            if direction[0]*new_direction[0] != 0 or direction[1]*new_direction[1] != 0:
                new_direction = (direction[0]+new_direction[0], direction[1]+new_direction[1])
            new_cost = cost_so_far[current][direction] + graph.cost(next)
            if next not in cost_so_far or new_direction not in cost_so_far[next]: # or new_cost < max(cost_so_far[next].values()):
                if next not in cost_so_far:
                    cost_so_far[next] = {}
                cost_so_far[next][new_direction] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put((next, new_direction), priority)
                if next not in came_from:
                    came_from[next] = {}
                came_from[next][current] = new_direction

    return came_from, cost_so_far

def sol1(data):
    grid = {}
    display = []
    for y, line in enumerate(data):
        display_line = []
        for x, char in enumerate(line):
            loc = Location2D(x, y)
            display_line.append(char)
            grid[loc] = int(char)
        display.append(display_line)
    bounds = (len(data[0]), len(data))
    graph = Graph(grid, bounds)
    start, goal = Location2D(0, 0), Location2D(bounds[0]-1, bounds[1]-1)
    came_from, cost_so_far = a_star_search(graph, start, goal, heuristic)
    return min(cost_so_far[goal].values())


def sol2(data):
    grid = {}
    display = []
    for y, line in enumerate(data):
        display_line = []
        for x, char in enumerate(line):
            loc = Location2D(x, y)
            display_line.append(char)
            grid[loc] = int(char)
        display.append(display_line)
    bounds = (len(data[0]), len(data))
    graph = UltraGraph(grid, bounds)
    start, goal = Location2D(0, 0), Location2D(bounds[0]-1, bounds[1]-1)
    came_from, cost_so_far = a_star_search(graph, start, goal, heuristic)
    return min(cost_so_far[goal].values())


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
