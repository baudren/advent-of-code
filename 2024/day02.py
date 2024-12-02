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

def sol1(data):
    total = 0
    for line in data:
        levels = [int(e) for e in line.split()]
        diffs = [levels[i+1]-levels[i] for i in range(len(levels)-1) ]
        if diffs[0] > 0:
            if max(diffs) <= 3 and min(diffs) >= 1:
                total += 1
        else:
            if max(diffs) <= -1 and min(diffs) >= -3:
                total += 1
    return total

def sol2(data):
    total = 0
    for line in data:
        levels = [int(e) for e in line.split()]
        diffs = [levels[i+1]-levels[i] for i in range(len(levels)-1) ]
        if sum(diffs) > 0:
            if max(diffs) <= 3 and min(diffs) >= 1:
                total += 1
            else:
                # iterate over all possible removals
                for i in range(len(levels)):
                    l = levels.copy()
                    l.pop(i)
                    ddiffs = [l[j+1]-l[j] for j in range(len(l)-1)]
                    if max(ddiffs) <= 3 and min(ddiffs) >= 1:
                        total += 1
                        break
        else:
            if max(diffs) <= -1 and min(diffs) >= -3:
                total += 1
            else:
                for i in range(len(levels)):
                    l = levels.copy()
                    l.pop(i)
                    ddiffs = [l[j+1]-l[j] for j in range(len(l)-1)]
                    if max(ddiffs) <= -1 and min(ddiffs) >= -3:
                        total += 1
                        break
            
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