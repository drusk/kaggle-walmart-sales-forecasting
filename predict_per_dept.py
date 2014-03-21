#!/usr/bin/env python

"""
Prediction using per-department model.
"""

import argparse
import pickle
import os

import numpy as np

# Must be in namespace when loading pickled predictor
from train_per_dept import CompositePredictor


class Predictor(object):
    def __init__(self, model_filename, output_filename):
        self.model = self.load_model(model_filename)

        self.output_file = open(output_filename, "wb")
        self.output_file.write("Id,Weekly_Sales\n")

    def load_model(self, model_filename):
        with open(model_filename, "rb") as filehandle:
            return pickle.load(filehandle)

    def predict_all(self, data_dir):
        for filename in os.listdir(data_dir):
            if not filename.endswith(".num"):
                continue

            store_id, dept_id = map(int, filename.split(".")[0].split("-"))

            full_path = os.path.join(data_dir, filename)

            data = np.loadtxt(full_path, delimiter=",")
            if data.ndim == 1:
                data = data.reshape((1, -1))

            ids, predictions = self.model.predict(store_id, dept_id, data)
            self.write_predictions(ids, predictions)

    def write_predictions(self, ids, predictions):
        for index, id_ in enumerate(ids):
            self.output_file.write("%s,%.2f\n" % (id_, predictions[index]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_filename",
                        help="The pickled model.")
    parser.add_argument("data_dir",
                        help="The numerical feature data.")
    parser.add_argument("output_filename",
                        help="Output predictions to this file.")

    args = parser.parse_args()

    Predictor(args.model_filename, args.output_filename).predict_all(
        args.data_dir)


if __name__ == "__main__":
    main()
