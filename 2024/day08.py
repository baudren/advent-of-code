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

def is_in(size, point):
    x, y = point
    return 0 <= x < size[0] and 0 <= y < size[1]


def sol1(data):
    nodes = {}
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char not in ['.', '#']:
                nodes[char] = nodes.get(char, []) + [(i, j)]
    size = len(data), len(data[0])
    antinodes = set()
    for node, positions in nodes.items():
        if len(positions) > 1:
            for i, a in enumerate(positions):
                for b in positions[i+1:]:
                    d = b[0]-a[0], b[1]-a[1]
                    l1 = a[0]-d[0],a[1]-d[1]
                    l2 = b[0]+d[0],b[1]+d[1]
                    if is_in(size, l1): antinodes.add(l1)
                    if is_in(size, l2): antinodes.add(l2)
    return len(antinodes)


def sol2(data):
    nodes = {}
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char not in ['.', '#']:
                nodes[char] = nodes.get(char, []) + [(i, j)]
    size = len(data), len(data[0])
    antinodes = set()
    for node, positions in nodes.items():
        if len(positions) > 1:
            for i, a in enumerate(positions):
                for b in positions[i+1:]:
                    d = b[0]-a[0], b[1]-a[1]
                    # Test all the points starting from a and below
                    n = 0
                    while True:
                        l1 = a[0]-n*d[0],a[1]-n*d[1]
                        if is_in(size, l1):
                            antinodes.add(l1)
                            n += 1
                        else: break
                    # test all the points starting from b and after
                    n = 0
                    while True:
                        l2 = b[0]+n*d[0],b[1]+n*d[1]
                        if is_in(size, l2):
                            antinodes.add(l2)
                            n += 1
                        else: break
    print(antinodes)
    return len(antinodes)

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