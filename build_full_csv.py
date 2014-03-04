#!/usr/bin/env python

"""
Puts all the available data together into a single CSV file.
"""

import argparse
import csv
import os
import sqlite3


class CsvBuilder(object):
    def __init__(self, dbname, output_filename):
        if output_filename is None:
            self.filename = os.path.splitext(dbname)[0] + ".csv"
        else:
            self.filename = output_filename

        self.con = sqlite3.connect(dbname)

    def join_tables(self):
        cur = self.con.cursor()

        cur.execute(
            """
            SELECT S.store_id, S.type, S.size, F.date, F.temperature,
                   F.fuel_price, F.markdown1, F.markdown2, F.markdown3,
                   F.markdown4, F.markdown5, F.cpi, F.unemployment,
                   F.is_holiday, ST.weekly_sales
            FROM Stores S, Features F, SalesTrain ST
            WHERE S.store_id = F.store_id AND
                  F.store_id = ST.store_id AND
                  F.date = ST.date
            """
        )

        return cur

    def build(self):
        with open(self.filename, "w") as filehandle:
            writer = csv.writer(filehandle)

            for row in self.join_tables():
                writer.writerow(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dbname", type=str,
                        help="The name of the database to extract the "
                             "data from.")
    parser.add_argument("--o", dest="output_filename", type=str, default=None,
                        help="The name of the output file.  "
                             "Defaults to the input filename with its "
                             "extension replaced by .csv")

    args = parser.parse_args()

    builder = CsvBuilder(args.dbname, args.output_filename)
    builder.build()


if __name__ == "__main__":
    main()
