import dragonfly_dict as ed
import numpy as np


def remove_duplicates(arr):
    hash_table = {}
    result = []
    for item in arr:
        item.sort()
        key = tuple(map(tuple, item))
        if key not in hash_table:
            hash_table[key] = True
            result.append(item)
    return result


def routing(s, d, dct, ind, length=0):
    if ind == -1:   # packet in destination node
        return length, s, dct, ind
    elif ind == 0:  # packet in source node
        temp = s.copy()
        del temp[-1]
        rid = tuple(temp)
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
                rid = tuple(temp)
                cid = tuple(s)
                if dct[rid] < max_p:
                    dct[cid] -= 1
                    dct[rid] += 1
                    length += 1
                    s = temp
                return length, s, dct, ind
        else:  # to the target group
            temp = s.copy()
            for i in range(1, len(s)):  # get the router ID of the target group in each dimension
                temp[i] = int(int((temp[0] - int(temp[0] > d[0])) / L) % (M ** i) / M ** (i - 1))
            temp[0] = d[0]
            rid = tuple(temp)
            cid = tuple(s)
            if dct[rid] < max_p:
                dct[cid] -= 1
                dct[rid] += 1
                length += 1
                s = temp
            return length, s, dct, ind
    elif s[1:len(d)-1] != d[1:-1]:  # the same group
        for i in range(1, len(s)):
            if s[i] != d[i]:
                temp = s.copy()
                temp[i] = d[i]
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
        s.append(d[-1])
        ind = 2
        length += 1
    return length, s, dct, ind


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
    link_label=[]

    congestion_cycles = 50
    thi = [5] * times
    congested_path = []
    n_congested = 0

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
            if S[i] != res[1]:
                link_label.append([S[i].copy(), res[1].copy()])
            dct, S[i], mark[i] = res[2], res[1], res[3]
            length = length + res[0]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
                if cycle > congestion_cycles:   # the congested path imply the destination node does not receive any packets in the last 10 cycles
                    if cycle <= thi[i%times] + congestion_cycles:
                        thi[i%times] = cycle
                    else:
                        if i%times not in congested_path:
                            congested_path.append(i%times)
                            n_congested += 1

        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
        if cycle > 650 or n_congested >= times:
            break
    for var in range(len(thi)):
        if var not in congested_path:
            if cycle - thi[var] > congestion_cycles:
                congested_path.append(var)
                n_congested += 1
    length = length / rec
    link_label = remove_duplicates(link_label)
    link_rate = len(link_label)/((L*M+1)*M*((L+M-1)/2+K))
    return length, cycle, rec, link_rate, n_congested


if __name__ == "__main__":
    K = 4     # number of nodes for each router
    M = 4      # number of routers in each dimension
    N = 2     # dimension of each group
    L = 6       # number of global links for each router
    max_p = 12  # maximum buffer slots

    lam = np.linspace(0.05, 1.0, 20)
    number = K*(L*M**N+1)*M**N
    y = np.zeros(len(lam))  # save the result of the packet latency
    z = np.zeros(len(lam))  # save the result of the throughput
    w = np.zeros(len(lam))  # save the result of the received ratio
    lu = np.zeros(len(lam))  # save the result of link utilized rate
    u = np.zeros(len(lam))  # save the result of congested paths
    num = 20  # repeat the simulation for num times

    for j in range(num):
        for i in range(len(lam)):
            res = packet(lam[i])
            y[i] += res[1]
            z[i] += res[2] / res[1]
            w[i] += res[2] / (res[1] * number * lam[i])
            lu[i] += res[3]
            u[i] += res[4]
            print(lam[i], res[1], res[2] / res[1], res[2] / (res[1] * number * lam[i]), res[3], res[4])
        print(j)

    y /= num
    z /= num
    w /= num
    lu /= num
    u /= num

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

    file = open('link_utilized_rate.txt', 'w')
    for v in lu:
        file.write(str(v) + '\n')
    file.close()

    file = open('congested_path.txt', 'w')
    for v in u:
        file.write(str(v) + '\n')
    file.close()
