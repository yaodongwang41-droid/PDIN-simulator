import numpy as np


def router_gen(l, m, n):
    out = np.zeros(n+2)
    out[0] = np.random.randint(0, l * m**n)  # group ID
    out[1:n+1] = np.random.randint(0, m, size=n)  # router ID
    return [int(x) for x in out]


def routing(s, d, L, M):
    if s[0] != d[0]:  # different groups
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
    return s


def basic_path(s, d, L, M):
    path = [s.copy()]
    while s!= d:
        temp = routing(s, d, L, M)
        path.append(temp.copy())
    return path




if __name__ == "__main__":
    M = 3      # number of routers in each dimension
    L = 2       # number of global links for each router
    K = 2       # number of nodes for each router
    N = 2     # dimension of each group
    sour = router_gen(L, M, N)
    des = router_gen(L, M, N)
    # sour = [4, 0, 0]
    # des = [3, 0, 0, 0]
    print("source node ID:", sour, "destination node ID:", des)
    res = basic_path(sour, des, L, M)
    print(res)