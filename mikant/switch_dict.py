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


def switch_dct(k, n):
    out = {}
    for g in range(2):
        for l in range(n - 1):
            for i in range(k ** (n - 1)):
                out[str(g) + str(l) + k_ary(i, k, n)] = 0
    return out


def node_dct(k, n, g=[], w=[], l=[]):
    for group in range(2):
        for level in range(k):
            for i in range(k ** (n - 1)):
                g.append(group)
                l.append(level)
                w.append([int(x) for x in list(k_ary(i, k, n))])
    return g, l, w


def config(k, n, lam):
    g, l, w = node_dct(k, n)
    random.shuffle(g)
    random.shuffle(l)
    random.shuffle(w)
    g = g[0:lam]
    l = l[0:lam]
    w = w[0:lam]
    return g, l, w


if __name__ == "__main__":
    k, n = 3, 4
    dicts = switch_dct(k, n)
    print(len(dicts))

    print(len(config(k, n, 0.5)[0]))
    print(len(config(k, n, 0.5)[1]))
    print(len(config(k, n, 0.5)[2]))
    print(config(k, n, 0.1)[0])
    print(config(k, n, 0.1)[1])
    print(config(k, n, 0.1)[2])
    # file = open('dict.csv', 'w')
    # for k, v in dicts.items():
    #     file.write(str(k) + ',' + str(v) + '\n')
    # file.close()

    file = open('switch_dict.txt', 'w')
    for k, v in dicts.items():
        file.write(str(k) + ' ' + str(v) + '\n')
    file.close()


