#!/usr/bin/env python

"""
Evaluates a model's performance.
"""

import argparse
import pickle

import numpy as np
from sklearn import cross_validation


class ModelEvaluator(object):
    def __init__(self, data, test_size, model):
        self.model = model

        (self.train_data,
         self.test_data,
         self.train_target,
         self.test_target) = cross_validation.train_test_split(
            data[:, :-1], data[:, -1], test_size=test_size)

        self.model.fit(self.train_data, self.train_target)

        # Make sure to convert back to original domain
        self.predictions = model.predict(self.test_data)
        self.test_target = self.test_target

    def mean_absolute_error(self):
        error = np.abs(self.predictions - self.test_target)
        return error.sum() / error.shape[0]

    def write_expected_and_predicted(self, output_filename):
        with open(output_filename, "wb") as filehandle:
            filehandle.write("Expected,Predicted\n")

            assert len(self.test_target) == len(self.predictions)
            for i in xrange(len(self.predictions)):
                filehandle.write("%.2f,%.2f\n" % (
                    self.test_target[i], self.predictions[i]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="The model to evaluate.")
    parser.add_argument("data", help="Labelled data used for evaluation.")
    parser.add_argument("--test-size", dest="test_size", type=float,
                        default=0.7,
                        help="The proportion of the dataset to include in "
                             "the test split.")
    parser.add_argument("--write", dest="output_file",
                        help="Write both the expected and predicted values "
                             "to a file.")

    args = parser.parse_args()

    with open(args.model) as filehandle:
        model = pickle.load(filehandle)

    with open(args.data) as filehandle:
        data = np.loadtxt(filehandle, delimiter=",")

    evaluator = ModelEvaluator(data, args.test_size, model)

    print "Mean squared error: %.5f" % evaluator.mean_absolute_error()

    if args.output_file:
        evaluator.write_expected_and_predicted(args.output_file)


if __name__ == "__main__":
    main()
