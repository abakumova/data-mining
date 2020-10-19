from __future__ import print_function, division
from future.utils import iteritems
from builtins import range, input
# from itertools import imap

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances

OUTPUT_DIRECTORY = 'output'
INITIAL_FILE_NAME = 'data/s1.txt'


def prepare_set(file):
    data_set = {}
    with open(file) as f:
        for line in f:
            (key, val) = line.split()
            data_set[int(key)] = int(val)
    return data_set


def main():
    num_of_clusters = 5  # input('Enter number of clusters: ')
    center_of_cluster = 1  # input('Enter center of cluster: ')
    data_set = prepare_set(INITIAL_FILE_NAME)
    print(list(data_set.keys()))
    print(list(data_set.values()))
    plt.scatter(list(data_set.keys()), list(data_set.values()), s=15)
    plt.show()


if __name__ == '__main__':
    main()
