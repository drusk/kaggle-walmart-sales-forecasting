#!/usr/bin/env python

"""
Generates IDs for the records in the format required by Kaggle.
"""

import argparse


def generate_id(record):
    return "_".join([record[0], record[1], "-".join(record[4:7])])


def generate_ids(features_filename):
    with open(features_filename, "rb") as filehandle:
        return [generate_id(line.split(",")) for line in filehandle]


def write_ids(output_filename, ids):
    with open(output_filename, "wb") as filehandle:
        for id_ in ids:
            filehandle.write(id_ + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("features_filename",
                        help="The CSV file with unprocessed features.")
    parser.add_argument("output_filename",
                        help="The file to output IDs to.")

    args = parser.parse_args()

    write_ids(args.output_filename, generate_ids(args.features_filename))


if __name__ == "__main__":
    main()
