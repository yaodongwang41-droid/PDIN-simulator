import numpy as np


def node_gen(k, l, m):
    out = np.zeros(3)
    out[0] = np.random.randint(0, l * m)  # group ID
    out[1] = np.random.randint(0, m - 1)  # router ID
    out[2] = np.random.randint(0, k - 1)  # node ID
    return [int(x) for x in out]


def routing(s, d):
    if s[:len(d)-1] != d[:len(d)-1]:
        if len(s) == len(d):
            del s[len(s)-1]
        elif s[0] != d[0]:  # different groups
            if s[1] != (d[0]-int(d[0] > s[0]))// L:
                s[1] = (d[0]-int(d[0] > s[0]))// L      # to the target router of this group
            else:    # to the target group
                s[1] = (s[0]-int(d[0] < s[0]))// L
                s[0] = d[0]
        else:    # the same group
            s[1] = d[1]
    else:           # in destination router
        s.append(d[len(d)-1])
    return s


def routing_length(s, d):
    length = 0
    if len(s) == len(d) and s != d:  # packet in source node
        s = s[0:2]
        length += 1
    if s[0] != d[0]:   # different groups
        if s[1] != (d[0] - int(d[0] > s[0])) // L:  # not in target router
            s[1] = (d[0] - int(d[0] > s[0])) // L
            length += 1
        # in target group
        s[1] = (s[0] - int(d[0] < s[0])) // L
        s[0] = d[0]
        length += 1
    # the same group
    if s[1] != d[1]:   # not in destination router
        s[1] = d[1]
        length += 1
    if s != d:     # destination router
        length += 1
    return length


if __name__ == "__main__":
    M = 5      # routers per group
    L = 2      # global links per router
    K = 2      # nodes per router

    src = node_gen(K, L, M)
    dst = node_gen(K, L, M)

    print("source:", src)
    print("dest:", dst)

    temp = src.copy()
    while src != dst:
        src = routing(src, dst)
        print("current:", src)

