"""
Author: Aidan Zhong
Date: 2025/7/17 12:31
Description:
"""
from collections import defaultdict


def get_code(s):
    s = sorted(s)
    t = min(s)
    ans = []
    for i in s:
        ans.append(ord(i) - ord(t))
    return ans, ord(t) - ord('a')


def get_shagram(s, k):
    code, i = get_code(s)
    i += k
    ans = ''
    for c in code:
        ans += chr((c + i) % 26 + ord('a'))
    return ans


print(get_code('bdc'))
print(get_code('abc'))

print(get_code('abz'))
print(get_code('bac'))

print(get_shagram('abba', 1))

s = set()
for i in range(26):
    s.add(get_shagram('abcdefg', i))
print(s)


# -------------------------------------------------
def w(s):
    ans = 0
    for i in s:
        ans += ord(i) - ord('a')
    return ans


print(w('jazz'))


def read_file_lines(filepath):
    lines = []
    with open(filepath, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))
    return lines


# Example usage
file_path = 'selected_strings.txt'  # Replace with your actual file path
selected_strings = read_file_lines(file_path)
selected_strings.sort(key=lambda s: len(s))
# Print result
# print(selected_strings)

# ---------------------------------------------------
print(get_code('urgent'))
print(get_code('gather'))

print(get_code('accepts'))
print(get_code('courage'))

cc, ii = get_code('while')
count = 0

highest_weight = 0
highest_weight_s = ''
for s in selected_strings:
    c, i = get_code(s)
    if c == cc:
        count += 1
        print(s, i, c)
    if s.__len__() == 10:
        if w(s) > highest_weight:
            highest_weight = w(s)
            highest_weight_s = s

print(count)
print(highest_weight)
print(highest_weight_s)
print(w('supporters'), w('popularity'))


# ---------------------------
def shift(s, i):
    ans = ''
    for c in s:
        ans += chr((ord(c) - ord('a') + i) % 26 + ord('a'))
    return ans
print(shift('abn', -1))

def f(strings):
    s1 = set()
    s2 = set()

    for s in strings:
        sorted_s = ''.join(sorted(s))
        shifted_s = shift(s, -1)
        s1.add(sorted_s)
        s2.add(''.join(sorted(shifted_s)))
    s3 = s1.intersection(s2)
    return s3

print(f(['jut', 'sit', 'tuj']))
print(f(['abc', 'bcd']))
print(f(['abc', 'bcd', 'cde']))

#------------------------------------
k_shagram_dict = defaultdict(list)
for s in selected_strings:
    c, i = get_code(s)
    c = tuple(c)
    k_shagram_dict[c].append(s)
maxi_weight = 0
for v in k_shagram_dict.values():
    if v.__len__() > 1:
        for item in v:
            maxi_weight = max(maxi_weight, w(item))
print(maxi_weight)