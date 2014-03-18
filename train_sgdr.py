#!/usr/bin/env python

"""
Trains a Stochastic Gradient Descent Regressor.
"""

import argparse
import pickle

import numpy as np
from sklearn.linear_model import SGDRegressor


def train_model(features_filename, iterations):
    training_data = np.loadtxt(features_filename, delimiter=",")

    model = SGDRegressor(n_iter=iterations)
    model.fit(training_data[:, :-1], training_data[:, -1])

    return model


def save_model(model, model_filename):
    with open(model_filename, "wb") as filehandle:
        pickle.dump(model, filehandle)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("features_filename",
                        help="The name of the file containing numerical "
                             "attributes which can be loaded into a Numpy "
                             "array.")
    parser.add_argument("model_filename",
                        help="The file to save the trained model to.")
    parser.add_argument("-i", dest="iterations", type=int, default=100,
                        help="Number of iterations of gradient descent "
                             "to perform.")

    args = parser.parse_args()

    model = train_model(args.features_filename, args.iterations)
    save_model(model, args.model_filename)


if __name__ == "__main__":
    main()
