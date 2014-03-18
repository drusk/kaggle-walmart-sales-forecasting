#!/usr/bin/env python

"""
Plots each feature.
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np


def plot(values):
    plt.figure()

    # num_bins = int(math.sqrt(len(values)))
    num_bins = 100
    plt.hist(values, bins=num_bins)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The features (CSV file).")

    args = parser.parse_args()

    data = np.loadtxt(args.filename, delimiter=",")

    for col_index in xrange(data.shape[1]):
        plot(data[:, col_index])

    plt.show()


if __name__ == "__main__":
    main()
