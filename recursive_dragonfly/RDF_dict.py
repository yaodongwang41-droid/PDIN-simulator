import numpy as np
import random


def k_ary(x, k, n):     # k-ary conversion
    li = []
    while x > 0:
        t1 = x % k
        x = x // k
        li.append(t1)
    out = ''
    for i in li[:: -1]:
        out += str(i)
    out = '0' * (n-len(out)) + out
    return out


def group_id(gi, m, n, l):
    out = m+1
    for i in range(n-gi-1):
        out = out*(out-1)*l+1
    return out


def dct(m, n, l):
    out = {}
    g0 = group_id(0, m, n, l)
    g1 = group_id(1, m, n, l)
    for j in range(g0):  # number of groups 0
        for i in range(g1):  # number of groups 1
            for u in range(m):    # number of routers in one group
                temp = k_ary(u, m, 1)
                router = '0' * (len(str(g0-1)) - len(str(j))) + str(j) + '0' * (len(str(g1-1)) - len(str(i))) + str(i) + temp
                out[router] = 0
    return out


def config(lam, k, m, n, l):
    out = []
    a = list(dct(m, n, l).keys())  # total router IDs
    node = np.zeros(n + 2)
    for i in a:
        node[0] = int(i[0:len(str(group_id(0, m, n, l)))])   # get the length of the first label and assign its location
        # assign the locations for other labels whose occupy a bit
        r = [int(x) for x in i[len(str(group_id(0, m, n, l))):len(i)]]
        for j in range(k):
            node[1:n + 1], node[len(node) - 1] = r, j
            out.append(list([int(x) for x in node]))
    random.shuffle(out)
    nodes = m * (m * l + 1)
    nodes = int(lam * nodes * (l * nodes + 1) * k)
    out = out[0:nodes]
    return out


if __name__ == "__main__":
    K = 4
    M = 4
    N = 2
    L = 2
    dict = dct(M, N, L)
    print(len(dict), dict)
    res = config(0.2, K, M, N, L)
    print(len(res), res)