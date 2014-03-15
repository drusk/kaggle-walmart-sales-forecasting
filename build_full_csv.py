#!/usr/bin/env python

"""
Puts all the available data together into a single CSV file.
"""

import argparse
import csv
import os
import sqlite3


class CsvBuilder(object):
    def __init__(self, dbname, output_filename, test=False):
        if output_filename is None:
            if not test:
                self.filename = os.path.splitext(dbname)[0] + ".csv"
            else:
                self.filename = "test.csv"
        else:
            self.filename = output_filename

        self.con = sqlite3.connect(dbname)
        self.test = test

    def join_tables(self):
        cur = self.con.cursor()

        if self.test:
            sql = """
                  SELECT S.store_id, ST.dept_id, S.type, S.size, F.year,
                         F.month, F.day, F.temperature, F.fuel_price,
                         F.markdown1, F.markdown2, F.markdown3, F.markdown4,
                         F.markdown5, F.cpi, F.unemployment, F.is_holiday
                  FROM Stores S, Features F, SalesTest ST
                  WHERE S.store_id = F.store_id AND
                        F.store_id = ST.store_id AND
                        F.year = ST.year AND
                        F.month = ST.month AND
                        F.day = ST.day
                  """

        else:
            sql = """
                  SELECT S.store_id, ST.dept_id, S.type, S.size, F.year,
                         F.month, F.day, F.temperature, F.fuel_price,
                         F.markdown1, F.markdown2, F.markdown3, F.markdown4,
                         F.markdown5, F.cpi, F.unemployment, F.is_holiday,
                         ST.weekly_sales
                  FROM Stores S, Features F, SalesTrain ST
                  WHERE S.store_id = F.store_id AND
                        F.store_id = ST.store_id AND
                        F.year = ST.year AND
                        F.month = ST.month AND
                        F.day = ST.day
                  """

        cur.execute(sql)

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
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    builder = CsvBuilder(args.dbname, args.output_filename, args.test)
    builder.build()


if __name__ == "__main__":
    main()
