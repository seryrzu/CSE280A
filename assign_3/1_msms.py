import numpy as np
from collections import Counter
import seaborn
import matplotlib.pyplot as plt


def main():
    alpha_0 = "1_msms_alpha_0_AFS.txt"
    alpha_small = "1_msms_alpha_small_AFS.txt"
    with open(alpha_0, 'r') as f:
        afs_0 = [int(x) for x in f.readlines()[0].split(' ')]
    with open(alpha_small, 'r') as f:
        afs_small = [int(x) for x in f.readlines()[0].split(' ')]

    afs_0, afs_small = np.array(afs_0), np.array(afs_small)
    print(afs_0)
    print(afs_small)
    right_max = 25

    plt.bar(range(1, right_max + 1),
            afs_0[:right_max],
            alpha=0.5,
            label='alpha = 0',
            color='g')
    width = 0.5
    plt.bar([x + .4 - width/2 for x in range(1, right_max + 1)],
            afs_small[:right_max],
            alpha=0.5,
            label='alpha = 1',
            color='r',
            width=width)
    plt.legend(loc='upper right')
    plt.title('AFS unnormalized')
    plt.savefig('1_AFS_unnormalized.pdf', format='pdf')
    plt.close()

    plt.bar(range(1, right_max + 1),
            afs_0[:right_max] / sum(afs_0),
            alpha=0.5,
            label='alpha = 0',
            color='g')
    width = 0.5
    plt.bar([x + .4 - width/2 for x in range(1, right_max + 1)],
            afs_small[:right_max] / sum(afs_small),
            alpha=0.5,
            label='alpha = 1',
            color='r',
            width=width)
    plt.legend(loc='upper right')
    plt.title('AFS normalized')
    plt.savefig('1_AFS_normalized.pdf', format='pdf')
    plt.close()


    right_max = 80
    N = 1000
    plt.bar(range(1, right_max + 1),
            afs_0[:right_max] / N * np.arange(1, right_max + 1),
            alpha=0.5,
            label='alpha = 0',
            color='g')
    width = 0.5
    plt.bar([x + .4 - width/2 for x in range(1, right_max + 1)],
            afs_small[:right_max] / N * np.arange(1, right_max + 1),
            alpha=0.5,
            label='alpha = 1',
            color='r',
            width=width)
    plt.legend(loc='upper right')
    plt.title('Theta estimate')
    plt.savefig('1_AFS_theta estimate.pdf', format='pdf')


if __name__ == "__main__":
    main()
