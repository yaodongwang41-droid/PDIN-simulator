import random
import numpy as np


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


def dct(m, n, l):
    out = {}
    for i in range(l*m**n+1):  # number of groups
        for j in range(m**n):    # number of routers in one group
            temp = k_ary(j, m, n)
            router ='0' * (len(str(l*m**n+1)) - len(str(i))) + str(i) + temp
            out[router] = 0
    return out


def config(nodes, k, m, n, l):
    out = []
    a = list(dct(m, n, l).keys())    # total router IDs
    node = np.zeros(n+2)
    for i in a:
        temp = int(i[:len(str(l*m**n+1))])
        r = [int(x) for x in i[len(str(l*m**n+1)):len(i)]]
        for j in range(k):
            node[0], node[1:n+1], node[len(node)-1] = temp, r, j
            out.append(list([int(x) for x in node]))
    random.shuffle(out)
    return out[:nodes]


def router_config(m, n, l, num):
    out = []
    for i in range(l * m ** n + 1):  # number of groups
        for j in range(m ** n):  # number of routers in one group
            router = [i]
            router.extend([int(x) for x in k_ary(j, m, n)])
            out.append(router)
    random.shuffle(out)
    return out[:num]


if __name__ == "__main__":
    K = 2
    M = 3
    N = 3
    L = 1
    dict = dct(M, N, L)
    print(len(dict), dict)
    res = config(20, K, M, N, L)
    print(len(res), res)
    print(router_config(M, N, L, 10))