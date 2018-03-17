import numpy as np

import matplotlib.pyplot as plt


def __MaxCol(M, f):
    means = np.mean(M, axis=0)
    feasible_cols = np.mean(M, axis=0) > f

    inters = np.ones(M.shape[0]).astype(bool)
    ids = np.arange((M.shape[1]))
    unused_cols = np.ones(M.shape[1]).astype(bool)
    while True:
        means = np.mean(M[inters, :], axis=0)
        means = means[unused_cols * feasible_cols]
        means **= 2
        means /= sum(means)
        if len(means) == 0:
            return ~unused_cols
        col_ind = np.random.choice(ids[unused_cols * feasible_cols],
                                   size = 1,
                                   p = means)[0]
        if np.mean(inters * M[:, col_ind]) > f:
            inters *= M[:, col_ind]
            unused_cols[col_ind] = False
        else:
            break
    # print(np.mean(inters))
    # print(np.mean(np.prod(M[:, ~unused_cols], axis=1)))
    return ~unused_cols


def MaxCol(M, f, N=10000):
    best_col_n, best_cols = 0, []
    for _ in range(N):
        cols = __MaxCol(M, f)
        col_n = sum(cols)
        if col_n > best_col_n:
            best_col_n = col_n
            best_cols = cols
    return best_cols


if __name__ == '__main__':
    M_fn = 'a3data2.txt'
    with open(M_fn, 'r') as f:
        M = [list(x.strip()) for x in f.readlines()]
        M = np.array(M).astype(bool)

    ncols = []
    fs = [0.1, 0.3, 0.5, 0.7, 0.9]
    for f in fs:
        cols = MaxCol(M, f=f)
        print(f)
        print(np.mean(np.prod(M[:, cols], axis=1)))
        print(np.sum(cols))
        print(np.where(cols)[0])
        print("")
        ncols.append(np.sum(cols))


    plt.plot(fs, ncols)
    plt.title("# Columns of Randomized Greedy Approach ")
    plt.xlabel("fraction")
    plt.ylabel("# columns")
    plt.savefig("pr4.pdf")
    plt.close()
