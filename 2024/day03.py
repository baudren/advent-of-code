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
import regex as re

def apply_mul(string):
    a, b = (int(e) for e in string.replace('mul(', '').replace(')', '').split(','))
    return a*b

def sol1(data):
    r = 'mul\(\d{1,3},\d{1,3}\)'
    total = 0
    for line in data:
        total += sum([apply_mul(x.group()) for x in re.finditer(r, line)])
    return total

def is_valid(valid, pos):
    for range_ in valid:
        if pos <= range_[1] and pos >= range_[0]:
            return True
    return False

def sol2(data):
    r = 'mul\(\d{1,3},\d{1,3}\)'
    rd = 'do'
    rdn = 'don\'t'
    total = 0
    line = "".join(data)

    rd_index = [x.start() for x in re.finditer(rd, line)]
    rdn_index = [x.start() for x in re.finditer(rdn, line)]
    rd_index = [e for e in rd_index if e not in rdn_index]
    valid = []
    current_range = [0, 0]
    for dont in rdn_index:
            if dont < current_range[0]:
                continue
            current_range[1] = dont
            valid.append(tuple(current_range))
            if rd_index:
                while rd_index and rd_index[0] < dont:
                        rd_index.pop(0)
                if rd_index:
                        current_range = [rd_index.pop(0), 0]
            else:
                break
    if current_range[1] == 0:
            current_range[1] = len(line)
            valid.append(tuple(current_range))
    total += sum(
            [apply_mul(x.group()) for x in re.finditer(r, line) if is_valid(valid, x.start())])
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