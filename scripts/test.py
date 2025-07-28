"""
Author: Aidan Zhong
Date: 2025/7/17 10:16
Description:
"""
import math
from collections import Counter, defaultdict
from functools import cache

# Set S: first 75 primes (as shown in your image)
S = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 47, 53, 59, 67, 71, 73, 79, 83, 89, 97, 101, 103,
    107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
    211, 227, 229, 233, 239, 251, 257, 263, 269, 281, 293, 307, 311, 317, 337, 347, 353, 359, 367,
    373, 379, 389, 401, 409, 419, 431, 443, 449, 461, 467, 479, 487, 491, 499, 503, 509, 521, 541,
    557, 563, 569, 571
}


def prime_factorization(n):
    """Returns the prime factorization of n as a Counter with multiplicities."""
    factors = Counter()
    # Check divisibility by 2
    while n % 2 == 0:
        factors[2] += 1
        n //= 2
    # Check odd divisors
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        while n % i == 0:
            factors[i] += 1
            n //= i
    # If remaining n is a prime
    if n > 1:
        factors[n] += 1
    return factors


@cache
def score_number(n, prime_set=S):
    """Scores the number n using the prime factors that are in prime_set."""
    factors = prime_factorization(n)
    score = sum(count for p, count in factors.items() if p in prime_set)
    return score


s_dict = defaultdict(list)
total = 0
for i in range(2, 10 ** 16):
    s_dict[score_number(i)].append(i)
    total += score_number(i)
print(s_dict)
anna, bob = 0, 0

iters = 0
while True:
    temp = max(s_dict.keys())
    anna += temp
    s_dict[temp].pop()
    if not s_dict[temp]:
        s_dict.pop(temp)
    if not s_dict:
        break
    iters += 1
    if iters == 50:
        print(anna, bob)

    temp = max(s_dict.keys())
    bob += temp
    s_dict[temp].pop()
    if not s_dict[temp]:
        s_dict.pop(temp)
    if not s_dict:
        break
    iters += 1
    if iters == 50:
        print(anna, bob)
print(anna, bob)
