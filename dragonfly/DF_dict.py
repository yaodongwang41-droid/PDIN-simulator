import random


def dct(m, l):
    out = {}
    for i in range(l*m+1):  # number of groups
        for j in range(m):    # number of routers in one group
            router = [i, j]
            out[tuple(router)] = 0
    return out


def config(num, k, m, l):
    out = []
    a = list(dct(m, l).keys())
    for i in a:
        for j in range(k):
            out.append(list(i) + [j])
    random.shuffle(out)
    return out[:num]


if __name__ == "__main__":
    K = 1
    M = 8
    L = 2
    dict = dct(M, L)
    print(len(dict), dict)
    lam = 0.2
    nums = int(lam * (M*L+1) * M * K)
    res = config(nums, K, M, L)
    print(len(res), res)
