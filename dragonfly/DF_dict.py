import random
import numpy as np


def dct(m, l):
    out = {}
    for i in range(l*m+1):  # number of groups
        for j in range(m):    # number of routers in one group
            router ='0' * (len(str(l*m+1)) - len(str(i))) + str(i) + str(j)
            out[router] = 0
    return out


def config(lam, k, m, l):
    out = []
    a = list(dct(m, l).keys())    # total router IDs
    node = np.zeros(3)
    for i in a:
        node[0] = int(i[0:len(str(l*m+1))])
        r = [int(x) for x in i[len(str(l*m+1)):len(i)]]
        for j in range(k):
            node[1:2], node[len(node)-1] = r, j
            out.append(list([int(x) for x in node]))
    random.shuffle(out)
    out = out[0:int(lam * (l*m+1)* m)*k]
    return out


if __name__ == "__main__":
    K = 1
    M = 8
    L = 2
    dict = dct(M, L)
    print(len(dict), dict)
    res = config(0.2, K, M, L)
    print(len(res), res)