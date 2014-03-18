#!/usr/bin/env python

"""
Plots the target attribute (assumed to be the last column).
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np


def plot(values):
    plt.figure()

    plt.hist(values, 100)
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        help="Data file with target in last column.")

    args = parser.parse_args()

    data = np.loadtxt(args.filename, delimiter=",")
    target = data[:, -1]

    print "Min:   %f" % target.min()
    print "Max:   %f" % target.max()
    print "Mean:  %f" % target.mean()
    print "Stdev: %f" % target.std()

    plot(target)


if __name__ == "__main__":
    main()
