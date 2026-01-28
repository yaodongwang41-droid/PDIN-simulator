import operator
import numpy as np


def routing(s, d, n):
    a = []
    for i in range(len(s)):
        if s[i] != d[i]:
            a.append(i)  # save the dimensions where the current switch is different with the destination node
    if 0 != len(a):
        temping = a[np.random.randint(0, len(a))]
        if 0 < s[temping] - d[temping] < n / 2 or d[temping] - s[temping] > n / 2:
            s[temping] = s[temping] - 1 if s[temping] > 0 else n - 1
        else:
            s[temping] = s[temping] + 1 if s[temping] < n - 1 else 0
        return s


def routing_rf(s, d, n, distance=0):
    while list(s) != list(d):
        s =routing(s, d, n)
        distance += 1
        print(s)
    else:
        return distance


if __name__ == "__main__":
    n = 7           # number of nodes in one dimension
    dimension = 3         # dimension
    sour = np.random.randint(0, n - 1, size=dimension)
    des = np.random.randint(0, n - 1, size=dimension)
    print(sour, des)
    print(routing_rf(sour, des, n))