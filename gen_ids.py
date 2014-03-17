#!/usr/bin/env python

"""
Generates IDs for the records in the format required by Kaggle.
"""

import argparse
import os


def generate_id(record):
    return (record[0] + "_" + record[1] + "_" +
            record[4] + "-" + record[5].zfill(2) + "-" + record[6].zfill(2))


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
    parser.add_argument("-o", dest="output_filename",
                        help="The file to output IDs to.")

    args = parser.parse_args()

    if args.output_filename is None:
        output_filename = os.path.splitext(args.features_filename)[0] + ".ids"
    else:
        output_filename = args.output_filename

    write_ids(output_filename, generate_ids(args.features_filename))


if __name__ == "__main__":
    main()
