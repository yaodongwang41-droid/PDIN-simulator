import numpy as np


def node_gen(k, l, m, n):
    out = np.zeros(n+2)
    out[0] = np.random.randint(0, l * m**n)  # group ID
    out[1:n+1] = np.random.randint(0, m, size=n)  # router ID
    out[len(out)-1] = np.random.randint(0, k - 1)  # node ID
    return [int(x) for x in out]


def routing(s, d, L, M):
    if s[:len(d)-1] != d[:len(d)-1]:
        if len(s) == len(d):
            del s[len(s)-1]
        elif s[0] != d[0]:  # different groups
            for i in range(1, len(s)):
                index = int(int((d[0]-int(s[0] < d[0]))/L) % (M ** i) / M**(i-1))        # target router ID in each dimension
                if s[i] != index:
                    s[i] = index      # to the target router of ith dimension
                    return s
            else:    # to the target group
                for i in range(1, len(s)):     # get the router ID of the target group in each dimension
                    s[i] = int(int((s[0]-int(s[0] > d[0])) / L) % (M ** i) / M ** (i - 1))
                s[0] = d[0]
        else:    # the same group
            for i in range(1, len(s)):
                if s[i] != d[i]:
                    s[i] = d[i]
                    return s
    else:           # in destination router
        s.append(d[len(d)-1])
    return s


def RoutingLength(X, Y, L, M):
    out = 0
    while X != Y:
        X = routing(X, Y, L, M)
        out += 1
    else:
        return out


if __name__ == "__main__":
    M = 3      # number of routers in each dimension
    L = 2       # number of global links for each router
    K = 2       # number of nodes for each router
    N = 2     # dimension of each group
    sour = node_gen(K, L, M, N)
    des = node_gen(K, L, M, N)
    # sour = [4, 0, 0]
    # des = [3, 0, 0, 0]
    print("source node ID:", sour, "destination node ID:", des)
    temp = sour.copy()
    while sour != des:
        sour = routing(sour, des, L, M)
        print('current router ID:', sour)
    print(RoutingLength(temp, des, L, M))
    print(temp)





