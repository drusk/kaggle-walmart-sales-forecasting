#!/usr/bin/env python

"""
Script description.
"""

import argparse
import csv
import os

import numpy as np


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

TEST_FEATURES = [TYPE, SIZE, YEAR, MONTH, DAY, TEMPERATURE,
                 FUEL_PRICE, MARKDOWN1, MARKDOWN2, MARKDOWN3, MARKDOWN4,
                 MARKDOWN5, CPI, UNEMPLOYMENT, IS_HOLIDAY]

# Includes the target attribute
TRAIN_FEATURES = TEST_FEATURES + [WEEKLY_SALES]


class NumericalFeatureExtractor(object):
    def __init__(self, normalize=False):
        self.markdown_transformer = MarkdownTransformer(normalize=normalize)
        self.num_transformer = NumberTransformer(fill_value=0, normalize=normalize)
        self.nonzeronum_transformer = NonZeroNumTransformer(fill_value=0, normalize=normalize)
        self.boolean_encoder = BooleanEncoder(normalize=normalize)

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

    def extract_features(self, filename):
        records, train = self.read_records(filename)

        def get_column(column_name):
            return [record[column_name] for record in records]

        years = self.num_transformer.transform(get_column(YEAR))
        months = self.num_transformer.transform(get_column(MONTH))
        days = self.num_transformer.transform(get_column(DAY))
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

        if train:
            weekly_sales = self.num_transformer.transform(
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


def write_feature_vectors(feature_vectors, output_filename):
    np.savetxt(output_filename, feature_vectors, delimiter=",")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")

    args = parser.parse_args()

    extractor = NumericalFeatureExtractor()
    for filename in os.listdir(args.directory):
        full_name = os.path.join(args.directory, filename)
        feature_vectors = extractor.extract_features(full_name)
        write_feature_vectors(feature_vectors, full_name + ".num")


if __name__ == "__main__":
    main()
