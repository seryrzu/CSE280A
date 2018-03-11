import argparse
import os
import errno
import itertools
from collections import defaultdict, OrderedDict

import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 15, 10
rcParams.update({'figure.autolayout': True})


def smart_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc


def smart_makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Q matrix",
                        dest="inp", required=True)
    parser.add_argument("-a", "--answer", help="Ground Truth",
                        dest="answer", required=True)
    parser.add_argument('-o', "--outdir", help="Output dir",
                        dest="outdir", required=True)
    parser.add_argument('--tool-name', help="Tool name",
                        dest='tool_name', required=True)
    params = parser.parse_args()
    return params


def parse_ground_truth(params):
    datasets = OrderedDict()
    label_ind = defaultdict(list)
    with open(params.answer, 'r') as f:
        for i, line in enumerate(f):
            name, label = line.strip().split(' ')
            datasets.setdefault(label, []).append(name)
            label_ind[label].append(i)
    return datasets, label_ind


def max_llhd_assigment(datasets, label_ind, q_matrix):
    cost_matrix = []
    for label in datasets:
        cost_matrix.append(np.sum(-np.log(q_matrix[label_ind[label]]),
                                  axis=0))
    cost_matrix = np.array(cost_matrix)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    label_column_id = []
    for i, label in enumerate(datasets):
        label_column_id.append((label, col_ind[i]))
    label_column_id.sort()
    return label_column_id


def get_y_true_pred(q_matrix, column_assignment, label_ind):
    y_true, y_pred = np.zeros(len(q_matrix)), np.zeros(len(q_matrix))
    for label in column_assignment:
        q_submatrix = q_matrix[label_ind[label[0]]]
        q_argmax = np.argmax(q_submatrix, axis=1)
        y_pred[label_ind[label[0]]] = q_argmax
        y_true[label_ind[label[0]]] = label[1]
    return y_true, y_pred


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    Seryrzu: taken from http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    """
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    # if normalize:
    #     cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #     print("Normalized confusion matrix")
    # else:
    #     print('Confusion matrix, without normalization')

    # print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def main():
    params = parse_command_line()
    datasets, label_ind = parse_ground_truth(params)
    q_matrix = np.loadtxt(params.inp)
    smart_makedirs(params.outdir)

    column_assignment = max_llhd_assigment(datasets, label_ind, q_matrix)
    y_true, y_pred = get_y_true_pred(q_matrix, column_assignment, label_ind)

    conf_m = confusion_matrix(y_true, y_pred)
    classes = [x[0] for x in column_assignment]
    plot_confusion_matrix(conf_m, classes=classes,
                          title='Confusion matrix, w/o normalization. ' + params.tool_name)
    plt.savefig(os.path.join(params.outdir, 'conf_matrix_wo_norm.pdf'),
                format='pdf')
    plt.close()
    plot_confusion_matrix(conf_m, classes=classes, normalize=True,
                          title='Confusion matrix, with normalization. ' + params.tool_name)
    plt.savefig(os.path.join(params.outdir, 'conf_matrix_with_norm.pdf'),
                format='pdf')
    plt.close()


if __name__ == "__main__":
    main()
