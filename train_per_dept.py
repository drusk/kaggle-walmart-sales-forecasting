#!/usr/bin/env python

"""
Train an algorithm to process each department.
"""

import argparse
import pickle
import os

import numpy as np
from sklearn.linear_model import BayesianRidge, ElasticNet, SGDRegressor
from sklearn import preprocessing
from sklearn.svm import SVR


class CompositePredictor(object):
    def __init__(self, per_dept_regressor_class):
        self.per_dept_regressor_class = per_dept_regressor_class

        self.predictors = {}
        self.scalers = {}

    def train(self, store_id, dept_id, data):
        scaler = preprocessing.StandardScaler()
        predictor = self.per_dept_regressor_class()

        feature_data = data[:, :-1]
        target_data = data[:, -1]

        scaler.fit(feature_data)
        predictor.fit(scaler.transform(feature_data), target_data)

        self.scalers[(store_id, dept_id)] = scaler
        self.predictors[(store_id, dept_id)] = predictor

    def generate_id(self, store_id, dept_id, record):
        def intstr(float_num):
            return str(int(float_num))

        return (str(store_id) + "_" + str(dept_id) + "_" +
                intstr(record[0]) + "-" + intstr(record[1]).zfill(2) +
                "-" + intstr(record[2]).zfill(2))

    def predict(self, store_id, dept_id, data):
        ids = []
        for i in xrange(data.shape[0]):
            ids.append(self.generate_id(store_id, dept_id, data[i, :]))

        try:
            scaled_data = self.scalers[(store_id, dept_id)].transform(data)
            predictions = self.predictors[(store_id, dept_id)].predict(scaled_data)
        except KeyError:
            # TODO: find similar store/dept and use their models
            predictions = np.zeros((len(ids), 1))

        return ids, predictions


def train_model(data_dir, model):
    for filename in os.listdir(data_dir):
        if not filename.endswith(".num"):
            continue

        store_id, dept_id = map(int, filename.split(".")[0].split("-"))

        full_path = os.path.join(data_dir, filename)

        data = np.loadtxt(full_path, delimiter=",")
        if data.ndim == 1:
            data = data.reshape((1, -1))

        model.train(store_id, dept_id, data)


def save_model(model, model_filename):
    with open(model_filename, "wb") as filehandle:
        pickle.dump(model, filehandle)


def get_algorithm(name):
    algs = {
        "sgdr": SGDRegressor,
        "svr": SVR,
        "bayes": BayesianRidge,
        "elastic": ElasticNet
    }

    return algs[name]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir",
                        help="Directory containing data files.")
    parser.add_argument("model_filename",
                        help="The file to save the trained model to.")
    parser.add_argument("--alg", choices=["sgdr", "svr", "bayes", "elastic"],
                        default="sgdr",
                        help="The algorithm for the model being trained.")

    args = parser.parse_args()

    model = CompositePredictor(get_algorithm(args.alg))

    train_model(args.data_dir, model)
    save_model(model, args.model_filename)


if __name__ == "__main__":
    main()
