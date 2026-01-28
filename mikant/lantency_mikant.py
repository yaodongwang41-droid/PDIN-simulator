import numpy as np
import switch_dict as sd
import math


def routing_la(sg, sw, sl, tg, tw, tl, k, n, upward, downward, mark, distance=0, max_p=8):
    if mark == -1:            # packet in destination node
        return sg, sw, sl, distance, upward, downward, mark

    elif mark == 0:          # in source node
        if upward[switch_id(sg, 0, sw)] < max_p:
            sl = 0  # To the source switch
            upward[switch_id(sg, sl, sw)] += 1
            distance += 1
            mark = 1
        return sg, sw, sl, distance, upward, downward, mark
    elif sg != tg:             # not source node
        if sl != n-2:
            temp = sw.copy()
            temp[sl] = np.random.randint(0, k)
            if upward[switch_id(sg, sl + 1, temp)] < max_p:
                upward[switch_id(sg, sl, sw)] -= 1
                sl += 1
                sw = temp
                distance += 1
                upward[switch_id(sg, sl, sw)] += 1
            return sg, sw, sl, distance, upward, downward, mark
        else:        # downward
            if mark == 1:
                if downward[switch_id(sg, sl, sw)] < max_p:
                    upward[switch_id(sg, sl, sw)] -= 1
                    downward[switch_id(sg, sl, sw)] += 1
                    mark = 2
                return sg, sw, sl, distance, upward, downward, mark
            else:
                temp = sw.copy()
                temp[sl] = tw[sl]
                if downward[switch_id(tg, sl, temp)] < max_p:
                    downward[switch_id(sg, sl, sw)] -= 1
                    sg, sw = tg, temp
                    downward[switch_id(sg, sl, sw)] += 1
                    distance += 1
                return sg, sw, sl, distance, upward, downward, mark

    else:
        if list(sw[sl:n-1]) != list(tw[sl:n-1]):
            if sl != n - 2:
                temp = sw.copy()
                temp[sl] = np.random.randint(0, k)
                if upward[switch_id(sg, sl + 1, temp)] < max_p:
                    upward[switch_id(sg, sl, sw)] -= 1
                    sl += 1
                    sw = temp
                    distance += 1
                    upward[switch_id(sg, sl, sw)] += 1
                return sg, sw, sl, distance, upward, downward, mark
            else:
                temp = sw.copy()
                temp[sl] = np.random.randint(0, k)
                if upward[switch_id(int(math.fabs(sg-1)), sl, temp)] < max_p:
                    upward[switch_id(sg, sl, sw)] -= 1
                    sg, sw = int(math.fabs(sg-1)), temp
                    upward[switch_id(sg, sl, sw)] += 1
                    distance += 1
                return sg, sw, sl, distance, upward, downward, mark

        # Reached NCA
        elif mark == 1:
            if downward[switch_id(sg, sl, sw)] < max_p:
                upward[switch_id(sg, sl, sw)] -= 1
                downward[switch_id(sg, sl, sw)] += 1
                mark = 2
                if mark != 2:
                    return sg, sw, sl, distance, upward, downward, mark

        if sl > 0:
            temp = sw.copy()
            temp[sl - 1] = tw[sl - 1]
            if downward[switch_id(sg, sl - 1, temp)] < max_p:
                downward[switch_id(sg, sl, sw)] -= 1
                sl -= 1
                sw = temp
                downward[switch_id(sg, sl, sw)] += 1
                distance += 1
            return sg, sw, sl, distance, upward, downward, mark

        # Reached destination switch
        else:
            downward[switch_id(sg, sl, sw)] -= 1
            sl, mark = tl, 3                # mark the packet which reached the destination node
            distance += 1
            return sg, sw, sl, distance, upward, downward, mark


def switch_id(g, l, w):
    out = str(g) + str(l)
    for element in w[::-1]:
        out += str(element)
    return out


def packet(lam, k, n):
    times = lam
    switch_dct_upward = sd.switch_dct(k, n)
    switch_dct_downward = switch_dct_upward.copy()

    S.G, S.L, S.W = sd.config(k, n, lam)
    T.G, T.L, T.W = sd.config(k, n, lam)

    cycle = 0
    length = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    sgb, slb, swb, tgb, tlb, twb = S.G.copy(), S.L.copy(), S.W.copy(), T.G.copy(), T.L.copy(), T.W.copy()
    while rec < times*200:
        for i in range(len(mark)):
            res = routing_la(S.G[i], S.W[i], S.L[i], T.G[i], T.W[i], T.L[i], k, n, switch_dct_upward, switch_dct_downward, mark[i])
            switch_dct_upward, switch_dct_downward, S.W[i], S.L[i], mark[i], S.G[i] = res[4], res[5], res[1], res[2], res[6], res[0]
            length = length + res[3]
            if mark[i] == 3:
                rec += 1
                mark[i] = -1
        if sum(list(switch_dct_downward.values())) < 0.55 * max_p*n*k**(n-1):
            S.G += sgb
            S.W += swb
            S.L += slb
            T.G += tgb
            T.W += twb
            T.L += tlb
            mark += list(np.zeros(times, int))
        cycle += 1
        if cycle > 600:
            break
    length = length / rec
    return length, cycle, rec


if __name__ == "__main__":
    k, n = 3, 6
    max_p = 8

    class S:
        G, W, L = 0, 0, 0

    class T:
        G, W, L = 0, 0, 0


    number = 2 * k ** n
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



