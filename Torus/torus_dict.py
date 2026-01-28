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


def dct(n, dim):
    out = {}
    for i in range(n**dim):
        temp = k_ary(i, n, dim)
        if len(temp) < n:
            temp = '0'*(dim-len(temp)) + temp
        out[temp] = 0
    return out


def config(lam, n, dim):
    a = list(dct(n, dim).keys())
    for i in range(len(a)):
        a[i] = [int(x) for x in a[i]]
    random.shuffle(a)
    out = a[0:int(lam*n**dim)]
    return out


def length(s, d, n, l=2):
    temp = s.copy()
    for i in range(len(s)):
        while temp[i] != d[i]:
            if 0 < temp[i] - d[i] < n / 2 or d[i] - temp[i] > n / 2:
                temp[i] = temp[i] - 1 if temp[i] > 0 else n - 1
            else:
                temp[i] = temp[i] + 1 if temp[i] < n - 1 else 0
            l += 1
    else:
        return l


if __name__ == "__main__":
    n = 8
    dimension = 3
    dit = dct(n, dimension)
    print(dit)
    print(len(dit))
    lam = 0.1
    sour = config(lam, n, dimension)
    des = config(lam, n, dimension)
    print(sour[:10])
    print(des[:10])
    print(len(sour), len(des))
