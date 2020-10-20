from __future__ import print_function, division

import math
import random
import matplotlib
from builtins import range
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIRECTORY = 'output'
INITIAL_FILE_NAME = 'data/s1.txt'


def euclidean_range(x, y, centroid):
    return math.sqrt((x - centroid[0]) ** 2 + (y - centroid[1]) ** 2)


def action(points, x_cord, y_cord, centroids, clusters):
    for i in range(len(points)):
        min_distance = euclidean_range(x_cord[i], y_cord[i], centroids[0])
        min_index = 0
        for j in range(len(centroids)):
            if euclidean_range(x_cord[i], y_cord[i], centroids[j]) < min_distance:
                min_distance = euclidean_range(x_cord[i], y_cord[i], centroids[j])
                min_index = j
        clusters.append((min_index, points[i]))


def show_plot(x_cord, y_cord, points, centroids, colors=None):
    plt.axis([min(x_cord), max(x_cord), min(y_cord), max(y_cord)])
    plt.scatter(*zip(*points), c=colors)
    plt.scatter(*zip(*centroids), c='black', s=30)
    plt.show()


def main():
    previous_clusters = []
    points = []
    x_cord = []
    y_cord = []
    centroids = []
    clusters = []

    num_of_clusters = int(input('Enter number of clusters: '))
    for line in open(INITIAL_FILE_NAME, "r"):
        n1, n2 = line.split()
        x_cord.append(int(n1))
        y_cord.append(int(n2))
        points.append((int(n1), int(n2)))

    all_colors = matplotlib.cm.rainbow(np.linspace(0, 1, num_of_clusters))

    for i in range(num_of_clusters):
        centroids.append(
            ((random.randint(np.min(x_cord), np.max(x_cord))), (random.randint(np.min(y_cord), np.max(y_cord)))))

    show_plot(x_cord, y_cord, points, centroids)
    action(points, x_cord, y_cord, centroids, previous_clusters)

    for i in range(len(centroids)):
        x_sum = 0
        y_sum = 0
        x_count = 0
        y_count = 0
        for key, value in previous_clusters:
            if key == i:
                x_sum += value[0]
                y_sum += value[1]
                x_count += 1
                y_count += 1
        centroids[i] = (x_sum / x_count, y_sum / y_count)

    while True:
        action(points, x_cord, y_cord, centroids, clusters)
        if previous_clusters == clusters:
            break

        previous_clusters = list(clusters)

        for i in range(len(centroids)):
            x_sum = 0
            y_sum = 0
            count = 0
            for key, value in clusters:
                if key == i:
                    x_sum += value[0]
                    y_sum += value[1]
                    count += 1
            centroids[i] = (x_sum / count, y_sum / count)

        clusters.clear()

    color_values = []
    for i in range(len(clusters)):
        color_values.append(all_colors[clusters[i][0]])

    show_plot(x_cord, y_cord, points, centroids, color_values)


if __name__ == '__main__':
    main()
