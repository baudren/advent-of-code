from math import factorial as f
from rich import print
import os
import itertools

from utils import *

debug = False
# Define which function to apply to parse the input data, from the text file or the text areas
# file_to_lines, file_to_ints, line_to_ints, line_to_str
basic_transform = file_to_lines


def sol1(data):
    total = 0
    for line in data:
        row = [c for c in line.split()[0]]
        clusters = [int(e) for e in line.split()[1].split(",")]
        value = count_perm_rec(row, clusters)
        print(value)
        #st.code((row, clusters, value))
        total += value
    return total

def get_nth_cluster(row, n):
    cluster = []
    count = 0
    for i, c in enumerate(row):
        if cluster:
            if c == '.':
                count += 1
                if '#' not in cluster:
                    cluster = []
                else:
                    if count == n:
                        break
                    else:
                        cluster = []
            else: 
                cluster.append(c)
        else:
            if c in ['?', '#']:
                cluster.append(c)
    if count == n:
        return cluster
    return []

def get_first_real_cluster(row):
    cluster = 0
    for i, c in enumerate(row):
        if cluster and c == '.':
            break
        elif c == '#':
            cluster += 1
    return cluster


def count_perm_cont(row, clusters):
    gaps = len(clusters)-1
    total_len = sum(clusters)+gaps
    if len(row) < total_len:
        return 0
    elif total_len == len(row):
        return 1
    k = len(row) - total_len  # number of freedom
    n = len(clusters)+1  # number of slots to put this freedom
    # count with repetitions
    return f(n+k-1)//(f(k)*f(n-1))

def get_max_cluster(row):
    clusters = []
    cluster = 0
    for i, c in enumerate(row):
        if c == '#':
            cluster += 1
        else:
            if cluster:
                clusters.append(cluster)
                cluster = 0
    if cluster:
        clusters.append(cluster)
    if clusters:
        return max(clusters)
    else:
        return 0

def get_min_cluster(row):
    clusters = []
    cluster = 0
    for i, c in enumerate(row):
        if not cluster and c in ['#', '?']:
            cluster += 1
        if cluster and c in ['?', '.']:
            clusters.append(cluster)
            if c == '?' and i > 0 and row[i-1] != '#':
                cluster = 1
            else:
                cluster = 0
    if cluster:
        clusters.append(cluster)
    return min(clusters) if clusters else 0


count_perm_rec_cache = {}
def count_perm_rec(row, clusters):
    key = (tuple(row), tuple(clusters))
    row = row.copy()
    if key in count_perm_rec_cache:
        return count_perm_rec_cache[key]
    cd, cp, ci = row.count('#'), row.count('.'), row.count('?')
    # if no more clusters, there is only one choice (all .), except if there are still # in the row
    total = 0
    if not clusters:
        if '#' in row:
            total = 0
        else:
            total = 1
    elif set(row) == set(['?']):
        total = count_perm_cont(row, clusters)
    elif cd > sum(clusters):
        total = 0
    elif cd+ci < sum(clusters):
        total = 0
    #elif row.count('#') == sum(clusters):
    #    total = 1
    else:
        if get_max_cluster(row) > max(clusters):
            total = 0
        elif get_min_cluster(row) > min(clusters):
            total = 0
        elif len(row) == clusters[0] and row.count('#') == clusters[0]:
            total = 1
        else:
            cluster = clusters[0]
            # Iterate for all positions, until finding a fixed one (not a ?)
            # TODO ignore leading . row = [c for c in "".join(row).strip('.')]
            tested = []
            for i in range(len(row)-cluster):
                if row[i] == '.':
                    continue
                row_mod = row.copy()
                for j in range(i):
                    if row[j] == '?':
                        row_mod[j] = '.'
                for j in range(cluster+1):
                    if row[i+j] == '?':
                        if j < cluster:
                            row_mod[i+j] = '#'
                        else:
                            row_mod[i+j] = '.'
                if row_mod in tested:
                    value = 0
                    break
                else:
                    tested.append(row_mod)
                if row_mod[i+cluster] == '#':
                    value = 0
                elif get_first_real_cluster(row_mod) != cluster:
                    value = 0
                else:
                    tested
                    value = count_perm_rec(row_mod[i+cluster+1:], clusters[1:])
                total += value
                #if row[i] == '#': 
                #    st.code("HERE")
                #    break
    count_perm_rec_cache[key] = total
    return total

def sol2(data):
    total = 0
    for line in data:
        row_unfolded = '?'.join(line.split()[0] for _ in range(5))
        row = [c for c in row_unfolded]
        clusters = [int(e) for e in line.split()[1].split(",")]*5
        total += count_perm_rec(row, clusters)
    return total


data = load()

data = basic_transform(data)
data_bk = data.copy()
print(sol1(data))
print(sol2(data))
