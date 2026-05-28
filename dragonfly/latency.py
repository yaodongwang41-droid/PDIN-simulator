import DF_dict as dd
import numpy as np


def routing(s, d, dct, ind, length=0):
    if ind == -1:   # packet in destination node
        return length, s, dct, ind
    elif ind == 0:  # packet in source node
        temp = s.copy()
        del temp[len(temp) - 1]
        rid = tuple(temp)
        if dct[rid] < max_p:
            dct[rid] += 1
            length += 1
            ind = 1
            s = temp
        return length, s, dct, ind
    elif s[0] != d[0]:  # different groups
        index = (d[0]-int(d[0] > s[0]))// L  # target router ID
        if s[1] != index:  # to the target router of ith dimension
            temp = [s[0], index]
            rid = tuple(temp)
            cid = tuple(s)
            if dct[rid] < max_p:
                dct[cid] -= 1
                dct[rid] += 1
                length += 1
                s = temp
            return length, s, dct, ind
        else:  # to the target group
            temp = [d[0], (s[0]-int(d[0] < s[0]))// L]
            rid = tuple(temp)
            cid = tuple(s)
            if dct[rid] < max_p:
                dct[cid] -= 1
                dct[rid] += 1
                length += 1
                s = temp
            return length, s, dct, ind
    elif s[1] != d[1]:  # the same group but not destination router
            temp = [s[0], d[1]]
            rid = tuple(temp)
            cid = tuple(s)
            if dct[rid] < max_p:
                dct[cid] -= 1
                dct[rid] += 1
                length += 1
                s = temp
            return length, s, dct, ind
    else:           # in destination router
        dct[tuple(s)] -= 1
        s.append(d[len(d)-1])
        ind = 2
        length += 1
    return length, s, dct, ind


def packet(lam):
    times = int(lam * (L*M+1)* M*K)
    dct = dd.dct(M, L)

    S = dd.config(times, K, M, L)
    T = dd.config(times, K, M, L)
    cycle = 0
    length = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    thr = 5
    drop = 0
    while rec < times * 200:
        for i in range(len(mark)):
            # comment the following code to execute a lossless simulation.
            # ----------------------------------------------------------------
            if cycle - i//times > thr and mark[i] != -1:  # drop packets
                if mark[i] != 0:
                    dct[tuple(S[i])] -= 1
                mark[i] = -1
                drop += 1
            # ---------------------------------------------------------------

            res = routing(S[i], T[i], dct, mark[i])
            dct, S[i], mark[i] = res[2], res[1], res[3]
            length = length + res[0]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
        if cycle > 650:
            break
    length = length / rec
    return length, cycle, rec, drop


if __name__ == "__main__":
    K = 4     # number of nodes for each router
    M = 8      # number of routers in each group
    L = 5       # number of global links for each router
    max_p = 12    # maximum buffer slots

    lam = np.linspace(0.05, 0.9, 18)
    number = K*(L*M+1)*M
    y = np.zeros(len(lam))  # save the result of the packet latency
    z = np.zeros(len(lam))  # save the result of the throughput
    w = np.zeros(len(lam))  # save the result of the received ratio
    u = np.zeros(len(lam))  # save the result of drop packet ratio
    num = 25  # repeat the simulation for num times
    for j in range(num):
        for i in range(len(lam)):
            res = packet(lam[i])
            y[i] = y[i] + res[1]
            z[i] = z[i] + res[2] / res[1]
            w[i] = w[i] + res[2] / (res[1] * number * lam[i])
            u[i] = u[i] + res[3] / (res[1] * number * lam[i])
            print(lam[i], res[1], res[2] / res[1], res[2] / (res[1] * number * lam[i]), res[3] / (res[1] * number * lam[i]))
        print(j)

    y = y / num
    z = z / num
    w = w / num
    u = u / num

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

    file = open('Drop.txt', 'w')
    for v in u:
        file.write(str(v) + '\n')
    file.close()
