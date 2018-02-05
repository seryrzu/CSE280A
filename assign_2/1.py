import numpy as np
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


### TODO Yates
def DprimeFast(df, Yates=False):
    p1 = np.mean(df, axis=0)
    p0 = 1-p1
    nrow, ncol = df.shape
    Dprimes = np.zeros((ncol, ncol), dtype=float)
    Chi2sStat = np.zeros((ncol, ncol), dtype=float)
    Chi2sPv = np.zeros((ncol, ncol), dtype=float)
    zeros = df == 0
    print("DprimeFast started")
    for i in range(ncol):
        if i % 500 == 0:
            print(i, ncol)
        pair_zeros = np.mean(zeros[:, i] * zeros.T, axis=1)
        D = pair_zeros - p0[i] * p0
        Dmax = np.zeros(ncol)
        Dmax[D > 0] = np.min([p0[i] * p1, p1[i] * p0], axis=0)[D > 0]
        Dmax[D <= 0] = -np.min([p0[i] * p0, p1[i] * p1], axis=0)[D <= 0]
        Dprimes[i, :] = D / Dmax
        Chi2sStat[i, :] = nrow * D**2 / (p0[i] * p1[i] * p0 * p1)
        Chi2sPv[i, :] = \
            -np.log(1 - sp.stats.chi2.cdf(Chi2sStat[i, :], 1))
    Chi2sPv += 1e-10
    print("DprimeFast done")
    return Dprimes, Chi2sStat, Chi2sPv


def FilterInput(df):
    n1 = np.sum(df, axis=0)
    nrow = df.shape[0]
    return df[:, (15 <= n1) * (n1 <= nrow - 15)]


def main():
    inp = "pop2.txt"
    with open(inp, 'r') as f:
        df = np.array([list(x.strip()) for x in f.readlines()]).astype(int)
    print(df.shape)
    df = FilterInput(df)
    print(df.shape)
    Dprimes, Chi2sStat, Chi2sPv = DprimeFast(df)
    Chi2sPv[Chi2sPv == np.inf] = 1

    mask = np.tril(np.ones_like(Dprimes))
    print(np.min(Chi2sPv))
    sns.heatmap(Chi2sPv, xticklabels=False, yticklabels=False, mask=mask,
                cmap="YlGnBu",
                vmin=np.min(Chi2sPv), vmax=np.max(Chi2sPv) / 6)
    plt.show()
    pass
    # plt.savefig('1.pdf', format='pdf')
    nrow, ncol = df.shape
    print("Dprime exporting")
    with open("1_dprime.tsv", "w") as f:
        for i in range(ncol - 1):
            for j in range(i + 1, ncol):
                print("%d\t%d\t%f\t%f\t%f" % (i, j, Dprimes[i, j], Chi2sStat[i, j], Chi2sPv[i, j]),
                      file=f)


if __name__ == "__main__":
    main()
