import EDD_dict as ed
import numpy as np
import matplotlib.pyplot as plt


def routing(s, d, dct, ind, max_p=12, length=0):
    if ind == -1:   # packet in destination node
        return length, s, dct, ind
    elif ind == 0:  # packet in source node
        temp = s.copy()
        del temp[len(temp) - 1]
        rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
        if dct[rid] < max_p:
            dct[rid] += 1
            length += 1
            ind = 1
            s = temp
        return length, s, dct, ind
    elif s[0] != d[0]:  # different groups
        for i in range(1, len(s)):
            index = int(int((d[0] - int(s[0] < d[0])) / L) % (M ** i) / M ** (i - 1))  # target router ID in each dimension
            if s[i] != index:  # to the target router of ith dimension
                temp = s.copy()
                temp[i] = index
                rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
                cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
                if dct[rid] < max_p:
                    dct[cid] -= 1
                    dct[rid] += 1
                    length += 1
                    s = temp
                return length, s, dct, ind
        else:  # to the target group
            temp = s.copy()
            for i in range(1, len(s)):  # get the router ID of the target group in each dimension
                temp[i] = int(int(temp[0] - int(temp[0] > d[0] ) / L) % (M ** i) / M ** (i - 1))
            temp[0] = d[0]
            rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
            cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
            if dct[rid] < max_p:
                dct[cid] -= 1
                dct[rid] += 1
                length += 1
                s = temp
            return length, s, dct, ind
    elif s[1:len(d)-1] != d[1:len(d)-1]:  # the same group
        for i in range(1, len(s)):
            if s[i] != d[i]:
                temp = s.copy()
                temp[i] = d[i]
                rid = '0' * (len(str(L * M ** N + 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
                cid = '0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
                if dct[rid] < max_p:
                    dct[cid] -= 1
                    dct[rid] += 1
                    length += 1
                    s = temp
                return length, s, dct, ind
    else:           # in destination router
        dct['0' * (len(str(L * M ** N + 1)) - len(str(s[0]))) + "".join([str(x) for x in s])] -= 1
        s.append(d[len(d)-1])
        ind = 2
        length += 1
    return length, s, dct, ind


# def rid(y):
#     return '0' * (len(str(L * M ** N + 1)) - len(str(y[0]))) + "".join([str(x) for x in y])


def packet(lam):
    times = int(lam * (L*M**N+1)* M**N*K)
    dct = ed.dct(M, N, L)

    S = ed.config(times, K, M, N, L)
    T = ed.config(times, K, M, N, L)
    cycle = 0
    length = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    thr = N*2+3
    drop = 0
    while rec < times * 200:
        for i in range(len(mark)):
            # comment the following code to execute a lossless simulation.
            # ----------------------------------------------------------------
            if cycle - i//times > thr and mark[i] != -1:  # drop packets
                if mark[i] != 0:
                    dct['0' * (len(str(L * M ** N + 1)) - len(str(S[i][0]))) + "".join([str(x) for x in S[i]])] -= 1
                mark[i] = -1
                drop += 1
            # ----------------------------------------------------------------
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
    K = 2     # number of nodes for each router
    M = 3      # number of routers in each dimension
    N = 3     # dimension of each group
    L = 2       # number of global links for each router

    lam = np.linspace(0.05, 0.9, 18)
    number = K*(L*M**N+1)*M**N
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