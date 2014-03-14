#!/usr/bin/env python

"""
Builds an SQLite database from the raw data provided.
"""

import argparse
import csv
import os
import sqlite3

SALES_TRAINING_FILE = "train.csv"
SALES_TESTING_FILE = "test.csv"
STORES_FILE = "stores.csv"
FEATURES_FILE = "features.csv"


class TableBuilder(object):
    def __init__(self, dbname, data_dir, filename):
        self._data_dir = data_dir
        self.con = sqlite3.connect(dbname)
        self.filename = filename

    def insert_data(self):
        with open(os.path.join(self._data_dir, self.filename),
                  "rb") as filehandle:
            reader = csv.reader(filehandle)

            # Skip header
            next(reader)

            for record in reader:
                self.process_record(record)

        self.con.commit()

    def create_table(self):
        raise NotImplementedError()

    def process_record(self, record):
        raise NotImplementedError()


class StoresTableBuilder(TableBuilder):
    def __init__(self, dbname, data_dir):
        super(StoresTableBuilder, self).__init__(dbname, data_dir, STORES_FILE)

    def create_table(self):
        self.con.execute(
            """
            CREATE TABLE Stores (
              store_id INT PRIMARY KEY,
              type TEXT,
              size INT
            )
            """
        )

        self.con.commit()

    def process_record(self, record):
        self.con.execute(
            "INSERT INTO Stores VALUES (?, ?, ?)", record)


class FeaturesTableBuilder(TableBuilder):
    def __init__(self, dbname, data_dir):
        super(FeaturesTableBuilder, self).__init__(dbname, data_dir,
                                                   FEATURES_FILE)

    def create_table(self):
        self.con.execute(
            """
            CREATE TABLE Features (
              store_id INT,
              date TEXT,
              temperature REAL,
              fuel_price REAL,
              markdown1 REAL,
              markdown2 REAL,
              markdown3 REAL,
              markdown4 REAL,
              markdown5 REAL,
              cpi REAL,
              unemployment REAL,
              is_holiday TEXT,
              PRIMARY KEY (store_id, date)
            )
            """
        )

        self.con.commit()

    def process_record(self, record):
        self.con.execute(
            "INSERT INTO Features VALUES "
            "  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            record)


class SalesTrainTableBuilder(TableBuilder):
    def __init__(self, dbname, data_dir):
        super(SalesTrainTableBuilder, self).__init__(dbname, data_dir,
                                                     SALES_TRAINING_FILE)

    def create_table(self):
        self.con.execute(
            """
            CREATE TABLE SalesTrain (
              store_id INT,
              dept_id INT,
              date TEXT,
              weekly_sales REAL,
              is_holiday TEXT,
              PRIMARY KEY (store_id, dept_id, date)
            )
            """
        )

        self.con.commit()

    def process_record(self, record):
        self.con.execute(
            "INSERT INTO SalesTrain VALUES (?, ?, ?, ?, ?)", record)


class SalesTestTableBuilder(TableBuilder):
    def __init__(self, dbname, data_dir):
        super(SalesTestTableBuilder, self).__init__(dbname, data_dir,
                                                    SALES_TESTING_FILE)

    def create_table(self):
        self.con.execute(
            """
            CREATE TABLE SalesTest (
              store_id INT,
              dept_id INT,
              date TEXT,
              is_holiday TEXT,
              PRIMARY KEY (store_id, dept_id, date)
            )
            """
        )

        self.con.commit()

    def process_record(self, record):
        self.con.execute(
            "INSERT INTO SalesTest VALUES (?, ?, ?, ?)", record)


class DatabaseBuilder(object):
    def __init__(self, dbname, data_dir):
        self.table_builders = []

        builder_classes = (StoresTableBuilder,
                           FeaturesTableBuilder,
                           SalesTrainTableBuilder,
                           SalesTestTableBuilder)

        for builder_class in builder_classes:
            self.table_builders.append(builder_class(dbname, data_dir))

    def build(self):
        for table_builder in self.table_builders:
            table_builder.create_table()
            table_builder.insert_data()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", type=str,
                        help="Directory containing the data.")
    parser.add_argument("--dbname", type=str, default="sales.db",
                        help="Name of the database to create.")

    args = parser.parse_args()

    db_builder = DatabaseBuilder(args.dbname, args.data_dir)
    db_builder.build()


if __name__ == "__main__":
    main()