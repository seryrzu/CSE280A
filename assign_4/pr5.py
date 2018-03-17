from pr4 import MaxCol

import numpy as np

import matplotlib.pyplot as plt

neutral_fn='5/neutral.txt'
hard_fn='5/hard.txt'

def read_msms(fn):
    matrices= []
    with open(fn, 'r') as f:
        matrix = []
        [f.readline() for _ in range(3)]
        for line in f:
            line = line.strip()
            if line == "":
                matrices.append(matrix)
                matrix = []
            else:
                matrix.append(line)

    matrices = [np.array([list(y) for y in x[3:]]).astype(bool) \
                for x in matrices]
    return matrices


def apply_max_col(matrices, filename, title):
    fs = [0.1, 0.2, 0.3, 0.5, 0.7]
    for i, matrix in enumerate(matrices):
        ncols = []
        print(i + 1, len(matrices))
        for f in fs:
            cols = MaxCol(matrix, f=f, N=1000)
            ncols.append(np.sum(cols))
        plt.plot(fs, ncols)
        plt.title(title + '. Matrix # %d' % (i + 1))
        plt.xlabel("fraction")
        plt.ylabel("# columns")
        plt.savefig(filename + "%d.pdf" % (i + 1))
        plt.close()


neutral = read_msms(neutral_fn)
hard = read_msms(hard_fn)

apply_max_col(neutral, '5/neutral', 'Neutral')
apply_max_col(hard, '5/hard', 'Hard')
