from fasthtml.common import *
import os
from rich import print
from utils import *

app, rt = fast_app(live=True)

app.context = {
    # Define which function to apply to parse the input data, from the text file or the text areas
    # file_to_lines, file_to_ints, line_to_ints, line_to_str
    "basic_transform": file_to_lines,
}

dir_order = ['^', '>', 'v', '<']

def explore(obstacles, dir_index, pos, size):
    dir_ = dir_order[dir_index]
    x, y = pos
    exited = True
    if dir_ == '^':
        potential_obstacles = [i for (i, j) in obstacles if j == y and i < x]
        if potential_obstacles:
            exited = False
            stop = (max(potential_obstacles)+1, y)
        else:
            stop = (0, y)
        visited = set((i, y) for i in range(stop[0], x))
    elif dir_ == '>':
        potential_obstacles = [j for (i, j) in obstacles if i == x and j > y]
        if potential_obstacles:
            exited = False
            stop = (x, min(potential_obstacles)-1)
        else:
            stop = (x, size[1]-1)
        visited = set((x, j) for j in range(y, stop[1]+1))
    elif dir_ == 'v':
        potential_obstacles = [i for (i, j) in obstacles if j == y and i > x]
        if potential_obstacles:
            exited = False
            stop = (min(potential_obstacles)-1, y)
        else:
            stop = (size[0]-1, y)
        visited = set((i, y) for i in range(x, stop[0]+1))
    elif dir_ == '<':
        potential_obstacles = [j for (i, j) in obstacles if i == x and j < y]
        if potential_obstacles:
            exited = False
            stop = (x, max(potential_obstacles)+1)
        else:
            stop = (x, size[1]-1)
        visited = set((x, j) for j in range(stop[1], y))
    return visited, exited, stop

def sol1(data):
    obstacles = {}
    dir_index = 0
    for i, line in enumerate(data):
        for j, char in enumerate(line.strip()):
            if char == "^": pos = (i, j)
            if char == '#': obstacles[(i, j)] = char
    size = (len(data), len(data[0]))
    visited = set([pos])
    while True:
        new_visited, exited, new_pos = explore(obstacles, dir_index, pos, size)
        visited.update(new_visited)
        if exited:
            break
        else:
            pos = new_pos
            dir_index = (dir_index + 1) % 4
    return len(visited)

def loops(added, obstacles, pos, size):
    debug = added == (6, 3)
    x, y = pos
    dir_index = 0
    turns = set([(x, y, dir_index)])
    if debug: print(f"{turns=}")
    is_looping = True
    while True:
        _, exited, new_pos = explore(obstacles, dir_index, pos, size)
        if debug: print(f"{new_pos=}")
        if exited:
            is_looping = False
            if debug: print(f"{added=} exits")
            break
        else:
            pos = new_pos
            dir_index = (dir_index + 1) % 4
            new_turn = (*pos, dir_index)
            if debug: print(f"{new_turn=}")
            if new_turn in turns:
                if debug: print(f"{added=} loops")
                if debug: print(turns)
                break
            else:
                turns.add(new_turn)
    return is_looping

# not 2263
def sol2(data):
    obstacles = set()
    dir_index = 0
    for i, line in enumerate(data):
        for j, char in enumerate(line.strip()):
            if char == "^":
                start = (i, j)
                pos = (i, j)
            if char == '#': obstacles.add((i, j))
    size = (len(data), len(data[0]))

    # It's only useful to test the points that were visited, the others we already know that they will not change the outcome
    visited = set([pos])
    while True:
        new_visited, exited, new_pos = explore(obstacles, dir_index, pos, size)
        visited.update(new_visited)
        if exited:
            break
        else:
            pos = new_pos
            dir_index = (dir_index + 1) % 4

    total = 0
    for obstacle in visited:
        if obstacle != start:
            obstacles.add(obstacle)
            if loops(obstacle, obstacles, start, size):
                total += 1
            obstacles.remove(obstacle)
    return total

#----- DONT TOUCH ------#

app.context.update({
    "file_exists": os.path.exists(get_data_filename()),
    "ex": [True, True],
    "data": [None, None],
    "sol": [None, None],
})

def build_main_page():
    app.context["file_exists"] = os.path.exists(get_data_filename())
    if not app.context["file_exists"]:
        data_file_form = Form(Textarea(name='data', type="text", placeholder='input from advent of code'), Button('Save', type="submit"), hx_post="/data", target_id="full")
        return Titled(get_day(), data_file_form, id="full")
    else:
        p1 = Div(H2("Part 1"), build_part(1))
        p2 = Div(H2("Part 2"), build_part(2))
        return Titled(get_day(), p1, p2, id="full")

@app.get("/")
def main():
    return build_main_page()

@app.post("/data")
def write_data(data: str):
    if data:
        write_to_file(data)
        return build_main_page()

def build_part(part):
    ex, d, s = app.context["ex"][part-1], app.context["data"][part-1], app.context["sol"][part-1]
    id_ = f"part{part}"
    switch_label = "Use Real Data" if ex else "Use Example"
    switch = Button(switch_label, type="Submit", hx_post=f"/switch/{part}", target_id=id_)
    if not ex:
        data = load()
        data = app.context["basic_transform"](data)
        if not data:
            return Div(P("Could not find data"), switch, id=id_)
        else:
            if part == 1:
                return Div(P(f"Solution: {sol1(data)}"), switch, id=id_)
            else:
                return Div(P(f"Solution: {sol2(data)}"), switch, id=id_)
    else:
        input_ = Div(
            Group(Label("Example: "), Textarea(d, name='data', rows=5, hx_post=f'/ex/{part}', target_id=id_)),
            Group(Label("Solution: "), Input(value=s, name='data', hx_post=f'/sol/{part}', target_id=id_))
        )
        info = P()
        if d:
            data = app.context["basic_transform"](d)
            if part == 1:
                info = Div(P(f"Example {part}: {data}"), P(f"sol{part}(data) = {sol1(data)}"))
            else:
                info = Div(P(f"Example {part}: {data}"), P(f"sol{part}(data) = {sol2(data)}"))
            if s:
                answer = int(s)
                correct = sol1(data) == answer if part == 1 else sol2(data) == answer
                if correct:
                    info = Div(info, B("All good"))
                else:
                    info = Div(info, B(f"Example failing: {sol1(data)=} != {answer}" if part == 1 else f"Example failing: {sol2(data)=} != {answer}"))
        return Div(input_, info, switch, id=id_)


@app.post("/switch/{tid}")
def switch(tid: int):
    app.context["ex"][tid-1] = not app.context["ex"][tid-1]
    return build_part(tid)

@app.post("/ex/{tid}")
def example(data: str, tid: int):
    app.context["data"][tid-1] = data
    return build_part(tid)

@app.post("/sol/{tid}")
def solution(data: str, tid: int):
    app.context["sol"][tid-1] = data
    return build_part(tid)


serve()