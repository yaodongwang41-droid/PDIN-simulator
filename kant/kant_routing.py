import numpy as np


def routing(sw, sl, tw, tl, k, n):
    print('Source node ID >>', sl, sw[:: -1], 'Destination node ID >>', tl, tw[:: -1])

    # To the source switch
    sl = 0
    print('Current switch ID >>', sl, sw[:: -1])
    distance = 1
    for i in range(n-1)[:: -1]:    # To the NCA
        if sw[i] != tw[i]:
            for j in range(i+1):
                sl += 1
                sw[j] = np.random.randint(0, k)
                print('Current switch ID >>', sl, sw[:: -1])
                distance += 1
            break

    # Reached NCA
    while sl > 0:
        sl -= 1
        sw[sl] = tw[sl]
        print('Current switch ID >>', sl, sw[:: -1])
        distance += 1

    # Reached destination switch
    sl = tl
    print('Current switch ID >>', sl, sw[:: -1])
    return distance+1


if __name__ == "__main__":
    k, n = 4, 5

    class S:
        W, L = np.zeros(n-1, int), 0

    class T:
        W, L = np.zeros(n-1, int), 0

    S.W, S.L = np.random.randint(0, k, size=len(S.W)), np.random.randint(0, n)
    T.W, T.L = np.random.randint(0, k, size=len(T.W)), np.random.randint(0, n)

    print('distance >>', routing(S.W, S.L, T.W, T.L, k, n))

