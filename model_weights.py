#!/usr/bin/env python

"""
Examine feature weights in models.
"""

import argparse
import collections
import pickle

import matplotlib.pyplot as plt

# Must be in namespace when loading pickled predictor
from train_per_dept import CompositePredictor


def load_model(model_filename):
    with open(model_filename, "rb") as filehandle:
        return pickle.load(filehandle)


def mean(values):
    return sum(values) / len(values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_filename", help="the pickled model.")

    args = parser.parse_args()

    coefficients = collections.defaultdict(list)

    model = load_model(args.model_filename)
    for department_model in model.predictors.values():
        coef_ = department_model.coef_
        for i in xrange(coef_.shape[0]):
            coefficients[i].append(coef_[i])

    print "Index\tMean"
    for index, values in coefficients.iteritems():
        print "%d\t%f" % (index, mean(values))
        plt.plot(values)

    plt.show()


if __name__ == "__main__":
    main()
