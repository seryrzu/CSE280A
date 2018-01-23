import numpy as np
from collections import Counter


class PerfTree(object):
    def __init__(self, m):
        self.m = np.array(m)
        cols = []
        for a in self.m.T:
            cols.append(-int(''.join(a), 2))
        self.cols_sort = np.argsort(cols)
        self.m = self.m[:,self.cols_sort].astype(int)
        self.mut_ind = [0] * self.m.shape[1]

    def Size(self):
        return self.m.shape

    def CheckPerf(self, r_i=None, c_i=0):
        if r_i is None:
            r_i = range(self.m.shape[0])

        if c_i == self.m.shape[1]:
            return True

        r_i_0, r_i_1 = [], []
        for r in r_i:
            if self.m[r, c_i] == 0:
                r_i_0.append(r)
            else:
                r_i_1.append(r)

        if len(r_i_1) and self.mut_ind[c_i]:
            return False
        if len(r_i_1):
            self.mut_ind[c_i] = 1

        print(c_i + 1, r_i_1, r_i_0)
        res1 = self.CheckPerf(r_i_1, c_i + 1) if len(r_i_1) else True
        res0 = self.CheckPerf(r_i_0, c_i + 1) if len(r_i_0) else True
        return res0 * res1


class PerfUnrootedTree(object):
    def __init__(self, m):
        self.m = np.array(m).astype(int)
        self.inv = [0] * self.m.shape[1]
        for i in range(self.m.shape[1]):
            if np.mean(self.m[:,i]) > 0.5:
                self.m[:,i] = 1 - self.m[:,i]
                self.inv[i] = 1
        cols = []
        for a in self.m.T:
            cols.append(-int(''.join(a.astype(str)), 2))
        self.cols_sort = np.argsort(cols)
        self.m = self.m[:,self.cols_sort].astype(int)
        self.inv = np.array(self.inv)[self.cols_sort]
        print(self.inv)
        print(self.cols_sort + 1)
        self.mut_ind = [0] * self.m.shape[1]

with open('4.txt', 'r') as f:
    m = [list(x.strip()) for x in f.readlines()]

# print(PerfTree(m).CheckPerf())
PerfUnrootedTree(m)
