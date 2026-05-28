import random
import numpy as np


def k_ary(x, k, n):     # k-ary conversion
    li = []
    while x > 0:
        t1 = x % k
        x = x // k
        li.append(t1)
    out = li[::-1]
    out = [0] * (n - len(out)) + out

    return out


def dct(m, n, l):
    out = {}
    for i in range(l*m**n+1):  # number of groups
        for j in range(m**n):    # number of routers in one group
            temp = k_ary(j, m, n)
            router = [i]+temp
            rid = tuple(router)
            out[rid] = 0
    return out


def config(num, k, m, n, l):
    out = []
    a = list(dct(m, n, l).keys())
    node = np.zeros(n + 2, dtype=int)
    for i in a:
        node[0:n+1] = i
        for j in range(k):
            node[n+1] = j
            out.append(node.tolist())
    random.shuffle(out)
    return out[:num]


def routing_path(s, d, L):
    path = []
    if len(s) == len(d):  # packet in source node
        s = s[0:2]
        path.append(s.copy())
    if s[0] != d[0]:   # different groups
        if s[1] != (d[0] - int(d[0] > s[0])) // L:  # not in target router
            s[1] = (d[0] - int(d[0] > s[0])) // L
            path.append(s.copy())
        # in target group
        s[1] = (s[0] - int(d[0] < s[0])) // L
        s[0] = d[0]
        path.append(s.copy())
    # the same group
    if s[1] != d[1]:   # not in destination router
        s[1] = d[1]
        path.append(s.copy())
    return path


if __name__ == "__main__":
    K = 1
    M = 11
    N = 1
    L = 1
    lam = 0.2  # load
    num = int(lam * (L*M**N+1)* M**N*K)    # number of nodes
    dict = dct(M, N, L)
    print(len(dict), dict)
    res = config(num, K, M, N, L)
    print(len(res), res)
