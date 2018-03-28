import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from scipy.stats import ttest_1samp

import matplotlib.pyplot as plt
import seaborn as sns


def read_ms(fn):
    with open(fn, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
        i = 0
        lines = lines[2:-1]
        inds = [i for i, line in enumerate(lines) if line == ""]

        samples = []
        for i1, i2 in zip(inds[:-1], inds[1:]):
            sample = lines[i1+4:i2]
            sample = np.array([list(line) for line in sample]).astype(int)
            samples.append(sample)
        return samples


def classify(s):
    lchunk = len(s) / 3
    y = np.arange(len(s)) // lchunk
    s = np.hstack( (s, y[:, np.newaxis]) )
    np.random.shuffle(s)
    X, y = s[:, :-1], s[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=42)
    y_pred = LinearSVC(multi_class="crammer_singer").fit(X_train, y_train).predict(X_test)
    return np.mean(y_pred != y_test)


def main():
    samp_fn = '4.txt'
    samps = read_ms(samp_fn)
    scores = []
    for samp in samps:
        scores.append(classify(samp))
    print(ttest_1samp(scores, 2/3))

    random_scores = []
    for samp in samps:
        np.random.shuffle(samp)
        random_scores.append(classify(samp))
    print(ttest_1samp(random_scores, 2/3))


if __name__ == "__main__":
    main()
