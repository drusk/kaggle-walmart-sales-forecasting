#!/usr/bin/env python

"""
Trains an Elastic Net Regressor.
"""

import argparse
import pickle

import numpy as np
from sklearn.linear_model import ElasticNet


def train_model(features_filename):
    training_data = np.loadtxt(features_filename, delimiter=",")

    X = training_data[:, :-1]
    y = training_data[:, -1]

    model = ElasticNet(alpha=1.0, l1_ratio=0.5, fit_intercept=True,
                       precompute='auto', rho=None)
    model.fit(X, y)

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

    args = parser.parse_args()

    model = train_model(args.features_filename)
    save_model(model, args.model_filename)


if __name__ == "__main__":
    main()
