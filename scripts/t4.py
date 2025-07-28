"""
Author: Aidan Zhong
Date: 2025/7/17 14:34
Description:
"""


def and_list(X):
    try:
        ans = X[0]
        for i in range(1, len(X)):
            ans &= X[i]
        return ans
    except:
        print("error")


def xor_list(X):
    try:
        ans = X[0]
        for i in range(1, len(X)):
            ans ^= X[i]
        return ans
    except:
        print("error")


X = [3, 5, 1]
print(and_list(X))
print(xor_list(X))


def f(X):
    if not X:
        return 0

    temp_list = []
    # find all contiguous sublists of X by traverse the start and end point
    for start in range(len(X)):
        for end in range(start + 1, len(X) + 1):
            # temporarily store the xor result into a list
            temp_list.append(xor_list(X[start:end]))
    return and_list(temp_list)


print(f(X))


def f_eff(X):
    # The first function f which has a time complexity of O(n^3),
    # The idea of pre_sum list came into my mind, but this time I will design a pre_xor list
    # Since a ^ b ^ b = a, so define pre_xor[i] = x[0] ^ x[1] ^ ... ^ x[i]
    # xor_list(X[l:r]) = pre_xor[r] ^ pre_xor[l-1], if l > 0, or pre_xor[r] which is a O(1) calculation
    # Then we do the O(n) and_list, we got the f in O(n^2)
    if not X:
        return 0
    pre_xor_list = [X[0]]
    # init the ans as all bit 1, which is ~0 in python
    ans = ~0

    # construct the pre_xor_list
    for i in range(1, len(X)):
        pre_xor_list.append(pre_xor_list[-1] ^ X[i])
    # traverse the start and end
    for start in range(len(X)):
        for end in range(start, len(X)):
            if start == 0:
                ans &= pre_xor_list[end]
            else:
                ans &= (pre_xor_list[end] ^ X[start - 1])
    return ans
print(f_eff(X))
