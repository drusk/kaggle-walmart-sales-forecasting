#!/usr/bin/env python

"""
Script description.
"""

import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np


def load_data(filename):
    expected = []
    predicted = []

    with open(filename, "rb") as filehandle:
        for record in csv.DictReader(filehandle):
            expected.append(float(record["Expected"]))
            predicted.append(float(record["Predicted"]))

    return expected, predicted


def plot(expected, predicted, num_bins):
    max_val = max(max(expected), max(predicted))
    min_val = min(min(expected), min(predicted))

    bins = np.linspace(min_val, max_val, num_bins)

    plt.hist(expected, bins=bins, alpha=0.5)
    plt.hist(predicted, bins=bins, alpha=0.5)

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("comparison_file",
                        help="File containing both expected and predicted "
                             "values.")
    parser.add_argument("-n", dest="num_bins", type=int, default=100,
                        help="Number of bins to use in histograms.")

    args = parser.parse_args()

    expected, predicted = load_data(args.comparison_file)

    print "Max expected: %f" % max(expected)
    print "Min expected: %f" % min(expected)
    print "Max predicted: %f" % max(predicted)
    print "Min predicted: %f" % min(predicted)

    plot(expected, predicted, args.num_bins)


if __name__ == "__main__":
    main()
