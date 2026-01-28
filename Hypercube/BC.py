import numpy as np
import cube_dict as cd
import matplotlib.pyplot as plt


def routing(s, d, dct, mark, max_p=6):
    distance = 0
    if mark == -2:  # stop sending packet in this cycle
        mark = 0
        return distance, s, dct, mark
    elif mark == -1:  # packet in destination node
        return distance, s, dct, mark

    elif mark == 0:  # packet in source node
        if dct["".join([str(x) for x in s])] < max_p:
            mark = 1
            dct["".join([str(x) for x in s])] += 1
        return distance, s, dct, mark
    else:
        a = []
        for i in range(len(s)):
            if s[i] != d[i]:
                a.append(i)  # save the different bits of source node and destination node

        if 0 != len(a):
            temp = s.copy()
            # temping = np.random.randint(0, len(a))
            # temp[a[temping]] = d[a[temping]]    # randomly
            temp[a[0]] = d[a[0]]         # basic
            if dct["".join([str(x) for x in temp])] < max_p:
                dct["".join([str(x) for x in s])] -= 1
                s = temp
                dct["".join([str(x) for x in s])] += 1
                distance += 1

            return distance, s, dct, mark
        else:
            mark = 2
            dct["".join([str(x) for x in s])] -= 1
            return distance, s, dct, mark


def packet(lam, n):
    times = int(lam * (2 ** n))
    dct = cd.dct(n)

    S = cd.config(lam, n)
    T = cd.config(lam, n)
    rl = np.zeros(times, int)
    for var in range(len(S)):
        rl[var] = cd.length(S[var], T[var])
    aver = n/2+2
    thr = n-2
    max_cycle = 500
    length = 0
    cycle = 0
    rec = 0  # the number of received packets
    mark = list(np.zeros(times, int))
    sb, tb = S.copy(), T.copy()
    # while cycle < max_cycle:
    while rec < times * 200:
        pre = []
        for i in range(len(mark)):
            if i > rl[i%times] * times and mark[i] == 0:
                mark[i] = -2 if mark[i - rl[i%times] * times] != -1 else mark[i]
            res = routing(S[i], T[i], dct, mark[i])
            dct, S[i], mark[i] = res[2], res[1], res[3]
            length = length + res[0]
            if mark[i] == 2:
                rec += 1
                mark[i] = -1
                # real = int(len(mark)/times) - int(i/times)
                # if real > thr+aver:
                #     pre.append(i+real*times)
        S += sb
        T += tb
        mark += list(np.zeros(times, int))
        cycle += 1
        # if len(pre) != 0:
        #     for var in pre:
        #         mark[var] = -2 if mark[var] == 0 else mark[var]
        if cycle > 500:
            break
    length = length / rec
    return length, cycle, rec


if __name__ == "__main__":
    n = 10

    class S:
        S = 0


    class T:
        T = 0

    lam = np.linspace(0.05, 1.0, 20)

    number = 2**n
    y = np.zeros(len(lam))  # save the result of the packet latency
    z = np.zeros(len(lam))  # save the result of the throughput
    w = np.zeros(len(lam))  # save the result of the received ratio
    num = 25  # repeat the simulation for num times
    for j in range(num):
        for i in range(len(lam)):
            res = packet(lam[i], n)
            y[i] = y[i] + res[1]
            z[i] = z[i] + res[2] / res[1]
            w[i] = w[i] + res[2] / (res[1] * number * lam[i])
            # print(res[1], res[2] / res[1], res[2] / (res[1] * number * lam[i])) # midway result
        # print(j)  # execution progress

    y = y / num
    z = z / num
    w = w / num


    # plt.plot(lam, y, lw=2)
    # plt.xlabel(r'Traffic load $\lambda$')
    # plt.ylabel('Cycles')
    # plt.show()

    file = open('cycles_brc.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()

    file = open('Throughput_brc.txt', 'w')
    for v in z:
        file.write(str(v) + '\n')
    file.close()

    file = open('Received_brc.txt', 'w')
    for v in w:
        file.write(str(v) + '\n')
    file.close()

