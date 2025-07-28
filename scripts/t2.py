"""
Author: Aidan Zhong
Date: 2025/7/17 11:47
Description:
"""
from collections import defaultdict

adj_dict = defaultdict(list)
adj_dict['A'] = ['B', 'C']
adj_dict['B'] = ['H']
adj_dict['C'] = ['F', 'G']
adj_dict['D'] = ['E', 'F']
adj_dict['E'] = ['F', 'G', 'I']
adj_dict['F'] = ['H']
adj_dict['G'] = ['I']

prev_dict = defaultdict(list)
for k in adj_dict.keys():
    for v in adj_dict[k]:
        prev_dict[v].append(k)

min_duration = defaultdict(int)
min_duration['A'] = 5
min_duration['B'] = 10
min_duration['C'] = 15
min_duration['D'] = 10
min_duration['E'] = 15
min_duration['F'] = 10
min_duration['G'] = 20
min_duration['H'] = 5
min_duration['I'] = 5

max_duration = defaultdict(int)
max_duration['A'] = 15
max_duration['B'] = 15
max_duration['C'] = 20
max_duration['D'] = 15
max_duration['E'] = 20
max_duration['F'] = 20
max_duration['G'] = 20
max_duration['H'] = 5
max_duration['I'] = 10

print(prev_dict)
earliest_start = defaultdict(int)
latest_start = defaultdict(int)
earliest_start['A'] = 0
latest_start['A'] = 0
earliest_start['B'] = 0
latest_start['B'] = 0

q = ['A', 'D']
earliest_finish = -1
latest_finish = -1
while q:
    v = q.pop()
    e_s = earliest_start[v] + min_duration[v]
    l_s = latest_start[v] + max_duration[v]
    earliest_finish = max(earliest_finish, e_s)
    latest_finish = max(latest_finish, l_s)
    for nn in adj_dict[v]:
        earliest_start[nn] = e_s
        latest_start[nn] = l_s
        q.append(nn)
earliest_start['F'] = 25
earliest_start['G'] = 25
earliest_start['H'] = 35
earliest_start['I'] = 45

# worst
w1 = 0
w2 = 0
q = ['A', 'D']
while q:
    v = q.pop()
    if w1 <= w2:
        # give it to w1
        w1 += max_duration[v]
    else:
        w2 += max_duration[v]
    for nn in adj_dict[v]:
        q.append(nn)
print(w1, w2)
print(earliest_start, latest_start)