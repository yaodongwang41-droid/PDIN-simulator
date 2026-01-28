import RDF_dict as rd
import numpy as np


def drouting(s, d, dct, max_p, key):
    temp = s.copy()
    if type(s[0]) != type(d[0]):
        print(type(s[0]), type(d[0]))
    if s[0] != d[0]:  # different groups
        if s[0] < d[0]:
            index = (d[0]-1) // L
            tar = s[0] // L
        else:
            index = d[0] // L
            tar = (s[0]-1) // L
        if s[1] != index:
            temp[1] = index
        else:    # to the target group
            temp[0] = d[0]
            temp[1] = tar
    else:    # the same group
        temp[1] = d[1]
    rid = key + "".join([str(x) for x in temp])
    cid = key + "".join([str(x) for x in s])
    if dct[rid] < max_p:
        dct[cid] -= 1
        dct[rid] += 1
        s = temp
    if type(temp) != type(d):
        print(type(temp) )
    return s, dct


def routing(s, d, dct, ind, max_p=16, length=0):
    # "ind = 0" in source node, "ind = 1" in router, "ind = 2" in destination node
    temp = s.copy()
    if ind == -1:  # packet in destination node
        return length, s, dct, ind
    elif ind == 0: # packet in source node
        del temp[len(temp) - 1]
        rid = '0' * (len(str(rd.group_id(0, M, N, L) - 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
        if dct[rid] < max_p:
            dct[rid] += 1
            s = temp
            ind = 1
    elif s[:len(d)-1] != d[:len(d)-1]:
        key = '0' * (len(str(rd.group_id(0, M, N, L) - 1)) - len(str(temp[0]))) + str(s[0])
        if s[0] != d[0]:  # different groups
            # build the target router
            if d[0] > s[0]:
                tar_r = [(d[0]-1)//L //M, (d[0]-1)//L % M]
                s2 = s[0]//L % M
                s1 = s[0]//L //M
            else:
                tar_r = [d[0] //L // M, d[0]//L % M]
                s2 = (s[0]-1) // L % M
                s1 = (s[0]-1) // L // M
            if temp[1:3] != tar_r:
                temp[1:3], dct = drouting(temp[1:3], tar_r, dct, max_p, key)
                s = temp
                length += 1
            else:    # route from s[0] to d[0]
                temp[2] = s2
                temp[1] = s1
                temp[0] = d[0]
                rid = '0' * (len(str(rd.group_id(0, M, N, L) - 1)) - len(str(temp[0]))) + "".join([str(x) for x in temp])
                cid = '0' * (len(str(rd.group_id(0, M, N, L) - 1)) - len(str(s[0]))) + "".join([str(x) for x in s])
                if dct[rid] < max_p:
                    dct[cid] -= 1
                    dct[rid] += 1
                    s = temp
        elif temp[1:3] != d[1:3]:  # different groups
            temp[1:3], dct = drouting(temp[1:3], d[1:3], dct, max_p, key)
            s = temp
            length += 1
    else:           # in destination router
        dct['0' * (len(str(rd.group_id(0, M, N, L) - 1)) - len(str(s[0]))) + "".join([str(x) for x in s])] -= 1
        s.append(d[len(d)-1])
        ind = 2
        length += 1
    return length, s, dct, ind


def packet(lam):
    times = M*(M*L+1)
    times = int(lam*times*(L*times +1)*K)
    dct = rd.dct(M, N, L)
    S = rd.config(lam, K, M, N, L)
    T = rd.config(lam, K, M, N, L)
    cycle = 0
    length = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    thr = 2**(N+1) + 1
    drop = 0
    while rec < times * 200:
        for i in range(len(mark)):
            # comment the following code to execute a lossless simulation.
            # ----------------------------------------------------------------
            if cycle - i // times > thr and mark[i] != -1:  # drop packets
                if mark[i] != 0:
                    dct['0' * (len(str(rd.group_id(0, M, N, L)-1)) - len(str(S[i][0]))) + "".join([str(x) for x in S[i]])] -= 1
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
        if cycle > 700:
            break
    length = length / rec
    return length, cycle, rec, drop


if __name__ == "__main__":
    M = 4      # number of routers in minimum unit
    L = 2       # number of global links for each router
    K = 4       # number of nodes for each router
    N = 2     # Number of recursions
    lam = np.linspace(0.05, 0.8, 16)
    number = M * (M * L + 1)
    number = number * (L * number + 1)*K
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
            print(lam[i], res[1], res[2] / res[1], res[2] / (res[1] * number * lam[i]),
                  res[3] / (res[1] * number * lam[i]))
        print(j)

    y = y / num
    z = z / num
    w = w / num
    u = u / num

    # file = open('cycles.txt', 'w')
    # for v in y:
    #     file.write(str(v) + '\n')
    # file.close()
    #
    # file = open('Throughput.txt', 'w')
    # for v in z:
    #     file.write(str(v) + '\n')
    # file.close()
    #
    # file = open('Received.txt', 'w')
    # for v in w:
    #     file.write(str(v) + '\n')
    # file.close()
    #
    # file = open('Drop.txt', 'w')
    # for v in u:
    #     file.write(str(v) + '\n')
    # file.close()
