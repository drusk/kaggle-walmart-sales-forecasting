#!/usr/bin/env python

"""
Extracts numerical features from the full CSV file with all data (which
contains both numerical and categorical attributes).
"""

import argparse
import csv

import numpy as np
from sklearn import preprocessing


STORE_ID = "store_id"
DEPT_ID = "dept_id"
TYPE = "type"
SIZE = "size"
YEAR = "year"
MONTH = "month"
DAY = "day"
TEMPERATURE = "temperature"
FUEL_PRICE = "fuel_price"
MARKDOWN1 = "markdown1"
MARKDOWN2 = "markdown2"
MARKDOWN3 = "markdown3"
MARKDOWN4 = "markdown4"
MARKDOWN5 = "markdown5"
CPI = "cpi"
UNEMPLOYMENT = "unemployment"
IS_HOLIDAY = "is_holiday"
WEEKLY_SALES = "weekly_sales"

TEST_FEATURES = [STORE_ID, DEPT_ID, TYPE, SIZE, YEAR, MONTH, DAY, TEMPERATURE,
                 FUEL_PRICE, MARKDOWN1, MARKDOWN2, MARKDOWN3, MARKDOWN4,
                 MARKDOWN5, CPI, UNEMPLOYMENT, IS_HOLIDAY]

# Includes the target attribute
TRAIN_FEATURES = TEST_FEATURES + [WEEKLY_SALES]


class NumericalFeatureExtractor(object):
    def __init__(self, input_filename, normalize=False):
        self.records, self.train = self.read_records(input_filename)

        self.categorical_transformer = OneHotEncoder(normalize=normalize)
        self.markdown_transformer = MarkdownTransformer(normalize=normalize)
        self.month_transformer = MonthTransformer(normalize=normalize)
        self.day_transformer = DayTransformer(normalize=normalize)
        self.num_transformer = NumberTransformer(fill_value=0, normalize=normalize)
        self.nonzeronum_transformer = NonZeroNumTransformer(fill_value=0, normalize=normalize)
        self.boolean_encoder = BooleanEncoder(normalize=normalize)
        self.target_transformer = NumberTransformer(normalize=False)

    def read_records(self, filename):
        records = []
        with open(filename, "rb") as filehandle:
            num_fields = len(filehandle.readline().split(","))

            # reset filehandle to beginning of file
            filehandle.seek(0)

            if num_fields == len(TEST_FEATURES):
                train = False
            elif num_fields == len(TRAIN_FEATURES):
                train = True
            else:
                raise ValueError(
                    "Unexpected number of fields: %d" % num_fields)

            field_names = TRAIN_FEATURES if train else TEST_FEATURES

            for record in csv.DictReader(filehandle, fieldnames=field_names):
                records.append(record)

        return records, train

    def extract_features(self):
        def get_column(column_name):
            return [record[column_name] for record in self.records]

        store_ids = self.num_transformer.transform(get_column(STORE_ID))
        dept_ids = self.num_transformer.transform(get_column(DEPT_ID))
        types = self.categorical_transformer.transform(get_column(TYPE))
        sizes = self.num_transformer.transform(get_column(SIZE))
        years = self.num_transformer.transform(get_column(YEAR))
        months = self.month_transformer.transform(get_column(MONTH))
        days = self.day_transformer.transform(get_column(DAY))
        temps = self.num_transformer.transform(get_column(TEMPERATURE))
        fuel_prices = self.num_transformer.transform(get_column(FUEL_PRICE))
        markdown1 = self.markdown_transformer.transform(get_column(MARKDOWN1))
        markdown2 = self.markdown_transformer.transform(get_column(MARKDOWN2))
        markdown3 = self.markdown_transformer.transform(get_column(MARKDOWN3))
        markdown4 = self.markdown_transformer.transform(get_column(MARKDOWN4))
        markdown5 = self.markdown_transformer.transform(get_column(MARKDOWN5))
        cpis = self.nonzeronum_transformer.transform(get_column(CPI))
        unemployment = self.nonzeronum_transformer.transform(get_column(UNEMPLOYMENT))
        is_holiday = self.boolean_encoder.transform(get_column(IS_HOLIDAY))

        feature_vectors = [
            store_ids,
            dept_ids,
            sizes,
            years,
            months,
            days,
            temps,
            fuel_prices,
            markdown1,
            markdown2,
            markdown3,
            markdown4,
            markdown5,
            cpis,
            unemployment,
            is_holiday
        ]

        for i in xrange(types.shape[1]):
            feature_vectors.insert(2 + i, types[:, i])

        if self.train:
            weekly_sales = self.target_transformer.transform(
                get_column(WEEKLY_SALES))
            feature_vectors.append(weekly_sales)

        return np.column_stack(feature_vectors)


class Transformer(object):
    def __init__(self, normalize=False):
        self.normalize = normalize

    def transform(self, values):
        new_values = self._transform(values)

        if self.normalize:
            return self.do_normalize(new_values)

        return new_values

    def do_normalize(self, values):
        values = np.asarray(values, dtype=np.float64)

        if values.max() == values.min():
            return np.zeros_like(values)

        return (values - values.min()) / (values.max() - values.min())

    def _transform(self, values):
        raise NotImplementedError()


class OneHotEncoder(Transformer):
    def _transform(self, values):
        encodings = {}
        index = 0

        for value in values:
            if value not in encodings:
                encodings[value] = index
                index += 1

        numerical = np.zeros((len(values), index))

        for i, value in enumerate(values):
            numerical[i][encodings[value]] = 1

        return numerical


class MarkdownTransformer(Transformer):
    def _transform(self, values):
        new_values = np.zeros(len(values))

        for i, value in enumerate(values):
            if value == "NA":
                new_values[i] = 0
            else:
                new_values[i] = value

        return new_values


class NumberTransformer(Transformer):
    def __init__(self, fill_value=0, normalize=False):
        super(NumberTransformer, self).__init__(normalize=normalize)
        self.fill_val = fill_value

    def _transform(self, values):
        new_values = np.zeros(len(values))

        for i, value in enumerate(values):
            try:
                new_values[i] = float(value)
            except ValueError:
                new_values[i] = self.fill_val

        return new_values


class NonZeroNumTransformer(Transformer):
    def __init__(self, fill_value=0, normalize=False):
        super(NonZeroNumTransformer, self).__init__(normalize=normalize)
        self.fill_val = fill_value

    def _transform(self, values):
        new_values = np.zeros(len(values))
        temp = 0;
        for i, value in enumerate(values):
            try:
                new_values[i] = float(value)
                self.fill_val = float(value)
            except ValueError:
                #for now, need to get this on a curve.. but where to do it
                new_values[i] = self.fill_val

        return new_values


class MonthTransformer(NumberTransformer):
    def do_normalize(self, values):
        values = np.asarray(values, dtype=np.float64)

        return values / 12


class DayTransformer(NumberTransformer):
    def do_normalize(self, values):
        values = np.asarray(values, dtype=np.float64)

        # TODO: take into account different days in month
        return values / 31


class BooleanEncoder(Transformer):
    def _transform(self, values):
        new_values = np.zeros(len(values))

        for i, value in enumerate(values):
            if value == "TRUE":
                new_values[i] = 1
            elif value == "FALSE":
                new_values[i] = 0
            else:
                raise ValueError("Must be TRUE or FALSE, but was %s" % value)

        return new_values


class LogarithmicTransformer(Transformer):
    def _transform(self, values):
        new_values = np.zeros(len(values))

        for i, value in enumerate(values):
            num = float(value)
            if num <= 0:
                new_values[i] = 0
            else:
                new_values[i] = np.log2(num)

        return new_values


def write_feature_vectors(feature_vectors, output_filename):
    np.savetxt(output_filename, feature_vectors, delimiter=",")


def scale_data(training_data, testing_data):
    scaler = preprocessing.StandardScaler()

    # Don't scale target attribute
    feature_data = training_data[:, :-1]
    target_data = training_data[:, -1]

    scaler.fit(feature_data)

    scaled_training = scaler.transform(feature_data)
    scaled_training = np.column_stack((scaled_training, target_data))

    scaled_testing = scaler.transform(testing_data)

    return scaled_training, scaled_testing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("training_filename")
    parser.add_argument("testing_filename")
    parser.add_argument("training_output_filename")
    parser.add_argument("testing_output_filename")

    args = parser.parse_args()

    print "Extracting training features..."
    training_data = NumericalFeatureExtractor(
        args.training_filename).extract_features()

    print "Extracting testing features..."
    testing_data = NumericalFeatureExtractor(
        args.testing_filename).extract_features()

    print "Scaling..."
    scaled_training, scaled_testing = scale_data(training_data, testing_data)

    print "Writing training output..."
    write_feature_vectors(scaled_training, args.training_output_filename)

    print "Writing testing output..."
    write_feature_vectors(scaled_testing, args.testing_output_filename)


if __name__ == "__main__":
    main()
