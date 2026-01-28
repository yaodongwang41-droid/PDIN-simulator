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
    if len(out) < n-1:
        out = '0' * (n-1-len(out)) + out
    return out


def switch_dct(k, n):   # generate all the switch IDs
    out = {}
    for l in range(n):
        for i in range(k**(n-1)):
            temp = str(l) + k_ary(i, k, n)
            out[temp] = 0
    return out


def node_dct(k, n, w=[], l=[]):  # generate all the node IDs
    for level in range(k):
        for i in range(k ** (n - 1)):
            l.append(level)
            w.append([int(x) for x in list(k_ary(i, k, n))])
    return l, w


def config(k, n, lam):        # select switch IDs
    l, w = node_dct(k, n)
    random.shuffle(l)
    random.shuffle(w)
    l = l[0:int(k**n*lam)]
    w = w[0:int(k**n*lam)]
    return l, w


if __name__ == "__main__":
    k, n = 4, 4
    dicts = switch_dct(k, n)
    print(len(dicts))

    print(len(config(k, n, 0.5)[0]), len(config(k, n, 0.5)[1]))
    print(config(k, n, 0.1))

    file = open('switch_dict.txt', 'w')
    for k, v in dicts.items():
        file.write(str(k) + ' ' + str(v) + '\n')
    file.close()


