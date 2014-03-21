#!/usr/bin/env python

"""
Create a CSV file for each department.
"""

import argparse
import collections
import csv
import os
import sqlite3


class CsvBuilder(object):
    def __init__(self, dbname, output_dir, test=False):
        try:
            os.mkdir(output_dir)
        except OSError:
            print "Warning: directory (%s) already exists." % output_dir

        self.output_dir = output_dir

        self.con = sqlite3.connect(dbname)
        self.test = test

    def filename(self, store_id, dept_id):
        name = "%d-%d" % (store_id, dept_id)
        return os.path.join(self.output_dir, name)

    def join_tables(self):
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

        data = collections.defaultdict(list)

        cur = self.con.cursor()
        for row in cur.execute(sql):
            key = row[:2]
            line = row[2:]
            data[key].append(line)

        return data

    def build(self):
        for key, lines in self.join_tables().iteritems():
            with open(self.filename(*key), "wb") as filehandle:
                csv.writer(filehandle).writerows(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dbname", type=str,
                        help="The name of the database to extract the "
                             "data from.")
    parser.add_argument("output_dir",
                        help="CSV files generated are put here.")
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    builder = CsvBuilder(args.dbname, args.output_dir, args.test)
    builder.build()


if __name__ == "__main__":
    main()
