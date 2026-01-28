import numpy as np


def routing(s, d, n, dim):
    length = 0
    for i in range(dim):
        print('Routing in', i+1, 'dimension')
        while s[i] != d[i]:
            if 0 < s[i] - d[i] < n / 2 or d[i] - s[i] > n / 2:
                s[i] = (s[i] - 1) % n
            else:
                s[i] = (s[i] + 1) % n
            print(s)
            length += 1
    else:
        print('current switch in destination switch ID', s)
        return length


if __name__ == "__main__":
    n = 8           # number of nodes in one dimension
    dimension = 4         # dimension
    sour = np.random.randint(0, n - 1, size=dimension)    # source node ID
    des = np.random.randint(0, n - 1, size=dimension)     # destination node ID
    print(sour, des)
    print(routing(sour, des, n, dimension))