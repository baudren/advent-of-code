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


def get_in(mapping, value):
    new_value = value
    for k in mapping:
        if value >= k and value < k + mapping[k][1]:
            new_value = mapping[k][0] + value - k
            break
    return new_value

def get_loc(mappings, seed):
    soil = get_in(mappings[0], seed)
    fert = get_in(mappings[1], soil)
    water = get_in(mappings[2], fert)
    light = get_in(mappings[3], water)
    temp = get_in(mappings[4], light)
    hum = get_in(mappings[5], temp)
    return get_in(mappings[6], hum)



def sol1(data):
    seeds = [int(e) for e in data[0].split(": ")[1].split()]
    for i, line in enumerate(data):
        if 'seed-to-soil' in line:
            seed_to_soil = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                seed_to_soil[src] = (dest, length)
        if 'soil-to-fertilizer' in line:
            soil_to_fert = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                soil_to_fert[src] = (dest, length)
        if 'fertilizer-to-water' in line:
            fert_to_water = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                fert_to_water[src] = (dest, length)
        if 'water-to-light' in line:
            water_to_light = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                water_to_light[src] = (dest, length)
        if 'light-to-temperature' in line:
            light_to_temp = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                light_to_temp[src] = (dest, length)
        if 'temperature-to-humidity' in line:
            temp_to_hum = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                temp_to_hum[src] = (dest, length)
        if 'humidity-to-location' in line:
            hum_to_loc = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                hum_to_loc[src] = (dest, length)
    locs = []
    for seed in seeds:
        soil = get_in(seed_to_soil, seed)
        fert = get_in(soil_to_fert, soil)
        water = get_in(fert_to_water, fert)
        light = get_in(water_to_light, water)
        temp = get_in(light_to_temp, light)
        hum = get_in(temp_to_hum, temp)
        loc = get_in(hum_to_loc, hum)
        locs.append(loc)
    return min(locs)


def sol2(data):
    seed_ranges = [int(e) for e in data[0].split(": ")[1].split()]
    seeds = []
    for i in range(0, len(seed_ranges), 2):
        seeds.append((seed_ranges[i], seed_ranges[i+1]))
    for i, line in enumerate(data):
        if 'seed-to-soil' in line:
            seed_to_soil = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                seed_to_soil[src] = (dest, length)
        if 'soil-to-fertilizer' in line:
            soil_to_fert = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                soil_to_fert[src] = (dest, length)
        if 'fertilizer-to-water' in line:
            fert_to_water = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                fert_to_water[src] = (dest, length)
        if 'water-to-light' in line:
            water_to_light = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                water_to_light[src] = (dest, length)
        if 'light-to-temperature' in line:
            light_to_temp = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                light_to_temp[src] = (dest, length)
        if 'temperature-to-humidity' in line:
            temp_to_hum = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                temp_to_hum[src] = (dest, length)
        if 'humidity-to-location' in line:
            hum_to_loc = {}
            j = i
            while True and j < len(data) - 1:
                j += 1
                if not data[j]:
                    break
                dest, src, length = [int(e) for e in data[j].split()]
                hum_to_loc[src] = (dest, length)
    mappings = [
        seed_to_soil,
        soil_to_fert,
        fert_to_water,
        water_to_light,
        light_to_temp,
        temp_to_hum,
        hum_to_loc
    ]
    locs = []
    for pair in seeds:
        loc = find_min_rec(mappings, pair[0], pair[0]+pair[1])
        locs.append(loc)
    return min(locs)

def find_min_rec(mappings, a, b):
    val_a = get_loc(mappings, a)
    val_b = get_loc(mappings, b)
    if val_a <= val_b:
        if a == a+(b-a)//2:
            return val_a
        return find_min_rec(mappings, a, a+(b-a)//2)
    else:
        return min(find_min_rec(mappings, a, a+(b-a)//2), find_min_rec(mappings, a+(b-a)//2+1, b))

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
