import numpy as np
import DED_dict as dd
import disjoint_path as dj
import ded_routing as dr


def router_gen(m, n, l):
    out = np.zeros(n+1)
    out[0] = np.random.randint(0, l * m**n)  # group ID
    out[1:n+1] = np.random.randint(0, m - 1, size=n)  # router ID
    return [int(x) for x in out]



def sim(m, n, l, numbers, times):
    successful = 0     # number of successful routing
    total_length = 0     # total length of the whole simulation
    fault_routers = dd.router_config(m, n, l, numbers)     # generate the fault router ids randomly

    for _ in range(times):
        s, d = router_gen(m, n, l), router_gen(m, n, l)     # generate the source destination routers pair
        # total_path = dr.basic_path(s, d, l, m)            # basic routing path
        total_path = dj.neighbor_jump(m, n, l, s, d)[0]           # neighbor jump disjoint path routing algorithms
        # total_path = dj.global_jump(m, n, l, s, d, epsilon=1)[0]           # global jump disjoint path routing algorithms
        # total_path = dj.multi_jump(m, n, l, s, d)[0]           # multi jump disjoint path routing algorithms
        length = 0                              # routing length in one simulation step
        for single_path in total_path:
            mark = 1
            for router in single_path:
                if router in fault_routers:
                    mark = 0
                    break
            if mark:
                successful += 1
                length = len(single_path)
                break        # terminate the simulation step if at least one path exists
        total_length += length

    success_rate = successful / times
    avg_length = total_length / successful if successful > 0 else 0
    return success_rate, avg_length


if __name__ == "__main__":
    K = 3     # number of nodes for each router
    M = 4      # number of routers in each dimension
    N = 3     # dimension of each group
    L = 2       # number of global links for each router
    routers = M ** N * (L * M ** N + 1)
    print("number of routers:", routers)
    x = np.linspace(0, 0.8, 17)             # set range of faulty rate
    y = []
    z = []
    for lam in x:
        nums = int(lam * routers)                # Number of simulated routers
        times = 100000                        # Number of simulated times
        res = sim(M, N, L, nums, times)
        y.append(res[0])
        z.append(res[1])

    file = open('success_ratio.txt', 'w')
    for v in y:
        file.write(str(v) + '\n')
    file.close()

    file = open('distance.txt', 'w')
    for v in z:
        file.write(str(v) + '\n')
    file.close()
