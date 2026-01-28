import numpy as np
import random


def routing(s, d, n, dim):
    length = 0
    dim_s = [x for x in range(dim)]
    random.shuffle(dim_s)
    for i in dim_s:
        print('Routing in', i+1, 'dimension')
        while s[i] != d[i]:  # vertical
            if 0 < s[i] - d[i] < n / 2 or d[i] - s[i] > n / 2:
                s[i] = s[i] - 1 if s[i] > 0 else n - 1
            else:
                s[i] = s[i] + 1 if s[i] < n - 1 else 0
            print(s)
            length += 1
    else:
        return length


if __name__ == "__main__":
    n = 7           # number of nodes in one dimension
    dimension = 3         # dimension
    sour = np.random.randint(0, n - 1, size=dimension)
    des = np.random.randint(0, n - 1, size=dimension)
    print(sour, des)
    print(routing(sour, des, n, dimension))