import numpy as np
import kant_dict as kd
import matplotlib.pyplot as plt


def routing_la(sw, sl, tw, tl, k, n, upward, downward, mark, distance=0, max_p=8):
    if mark == -1:            # packet in destination node
        return sw, sl, distance, upward, downward, mark

    elif mark == 0:          # in source node
        if upward[switch_id(0, sw)] < max_p:
            sl = 0  # To the source switch
            upward[switch_id(sl, sw)] += 1
            distance += 1
            mark = 1
        return sw, sl, distance, upward, downward, mark
    else:             # not source node
        if list(sw[sl:n-1]) != list(tw[sl:n-1]):
            temp = sw.copy()
            temp[sl] = np.random.randint(0, k)
            if upward[switch_id(sl + 1, temp)] < max_p:
                upward[switch_id(sl, sw)] -= 1
                sl += 1
                sw = temp
                distance += 1
                upward[switch_id(sl, sw)] += 1
            return sw, sl, distance, upward, downward, mark

        # Reached NCA
        elif mark == 1:
            if downward[switch_id(sl, sw)] < max_p:
                upward[switch_id(sl, sw)] -= 1
                downward[switch_id(sl, sw)] += 1
                mark = 2
            return sw, sl, distance, upward, downward, mark

        elif sl > 0:
            temp = sw.copy()
            temp[sl - 1] = tw[sl - 1]
            if downward[switch_id(sl - 1, temp)] < max_p:
                downward[switch_id(sl, sw)] -= 1
                sl -= 1
                sw = temp
                downward[switch_id(sl, sw)] += 1
                distance += 1
            return sw, sl, distance, upward, downward, mark

        # Reached destination switch
        else:
            downward[switch_id(sl, sw)] -= 1
            sl, mark = tl, 3                # mark the packet which reached the destination node
            distance += 1
            return sw, sl, distance, upward, downward, mark


def switch_id(l, w):
    out = str(l)
    for element in w[::-1]:
        out += str(element)
    return out


def packet(lam, k, n):
    times = lam
    switch_dct_upward = kd.switch_dct(k, n)
    switch_dct_downward = switch_dct_upward.copy()

    S.L, S.W = kd.config(k, n, lam)
    T.L, T.W = kd.config(k, n, lam)

    max_cycle = 300
    cycle = 0
    length = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    slb, swb, tlb, twb = S.L.copy(), S.W.copy(), T.L.copy(), T.W.copy()
    while rec < times * 200:
        for i in range(times*(cycle+1)):
            res = routing_la(S.W[i], S.L[i], T.W[i], T.L[i], k, n, switch_dct_upward, switch_dct_downward, mark[i])
            switch_dct_upward, switch_dct_downward, S.W[i], S.L[i], mark[i] = res[3], res[4], res[0], res[1], res[5]
            length = length + res[2]
            if mark[i] == 3:
                rec += 1
                mark[i] = -1
        S.W += swb
        S.L += slb
        T.W += twb
        T.L += tlb
        mark += list(np.zeros(times, int))
        cycle += 1

    length = length / rec
    return length, cycle, rec


if __name__ == "__main__":
    k, n = 4, 6

    class S:
        W, L = 0, 0

    class T:
        W, L = 0, 0


    number = k ** n
    lam = np.arange(25, 525, 25)
    y = np.zeros(len(lam))  # save the result of the packet latency
    z = np.zeros(len(lam))  # save the result of the throughput
    w = np.zeros(len(lam))  # save the result of the received ratio
    num = 20  # repeat the simulation for num times
    for j in range(num):
        for i in range(len(lam)):
            res = packet(lam[i], k, n)
            y[i] = y[i] + res[1]
            z[i] = z[i] + res[2] / res[1]
            w[i] = w[i] + res[2] / (res[1] * lam[i])
            print(lam[i], res[1], res[2] / res[1], res[2] / (res[1] * lam[i]))
        print(j)
    y = y / num
    z = z / num
    w = w / num

    file = open('cycles.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()

    file = open('Throughput.txt', 'w')
    for v in z:
        file.write(str(v) + '\n')
    file.close()

    file = open('Received.txt', 'w')
    for v in w:
        file.write(str(v) + '\n')
    file.close()





