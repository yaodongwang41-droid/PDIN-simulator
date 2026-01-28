import random


def dct(n):
    out = {}
    for i in range(2**n):
        temp = bin(i).replace('0b', '')
        if len(temp) < n:
            temp = '0'*(n-len(temp)) + temp
        out[temp] = 0
    return out


def config(lam, n):
    a = list(dct(n).keys())
    for i in range(len(a)):
        a[i] = [int(x) for x in a[i]]
    random.shuffle(a)
    out = a[0:int(lam*2**n)]
    return out


def length(s, d, l=2):
    if len(s) == len(d):
        for i in range(len(s)):
            if s[i] != d[i]:
                l += 1
    else:
        print('different length')
    return l


if __name__ == "__main__":
    n = 10
    dit = dct(n)
    src = config(0.1, n)
    des = config(0.1, n)
    print(src[0], des[0])
    print(length(src[0], des[0]))
    a = "".join([str(x) for x in src[0]])     # convert the target array to string
    dit[a] += 1
    b = [1,0]
    print(a, type(a))
    print(dit)
