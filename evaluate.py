#!/usr/bin/env python

"""
Evaluates a model's performance.
"""

import argparse
import pickle

import numpy as np
from sklearn import cross_validation


class ModelEvaluator(object):
    def __init__(self, data):
        (self.train_data,
         self.test_data,
         self.train_target,
         self.test_target) = cross_validation.train_test_split(
            data[:, :-1], data[:, -1])

    def mean_absolute_error(self, model):
        model.fit(self.train_data, self.train_target)
        predictions = model.predict(self.test_data)

        error = np.abs(predictions - self.test_target)
        return error.sum() / error.shape[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="The model to evaluate.")
    parser.add_argument("data", help="Labelled data used for evaluation.")

    args = parser.parse_args()

    with open(args.model) as filehandle:
        model = pickle.load(filehandle)

    with open(args.data) as filehandle:
        data = np.loadtxt(filehandle, delimiter=",")

    evaluator = ModelEvaluator(data)

    print "Mean squared error: %.5f" % evaluator.mean_absolute_error(model)


if __name__ == "__main__":
    main()
