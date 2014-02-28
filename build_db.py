#!/usr/bin/env python

"""
Builds an SQLite database from the raw data provided.
"""

import argparse
import csv
import os
import sqlite3

SALES_TRAINING_FILE = "train.csv"
STORES_FILE = "stores.csv"
FEATURES_FILE = "features.csv"


class DatabaseBuilder(object):
    def __init__(self, dbname, data_dir):
        self._data_dir = data_dir
        self.con = sqlite3.connect(dbname)

    def _process_file(self, filename, process_record):
        with open(os.path.join(self._data_dir, filename), "rb") as filehandle:
            reader = csv.reader(filehandle)

            # Skip header
            next(reader)

            for record in reader:
                process_record(record)

    def create_tables(self):
        self.con.execute(
            """
            CREATE TABLE Stores (
              store_id INT PRIMARY KEY,
              type TEXT,
              size INT
            )
            """
        )

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

    def insert_stores_data(self):
        def process_record(record):
            self.con.execute(
                "INSERT INTO Stores VALUES (?, ?, ?)", record)

        self._process_file(STORES_FILE, process_record)
        self.con.commit()

    def insert_features_data(self):
        def process_record(record):
            self.con.execute(
                "INSERT INTO Features VALUES "
                "  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                record)

        self._process_file(FEATURES_FILE, process_record)
        self.con.commit()

    def insert_sales_train_data(self):
        def process_record(record):
            self.con.execute(
                "INSERT INTO SalesTrain VALUES (?, ?, ?, ?, ?)", record)

        self._process_file(SALES_TRAINING_FILE, process_record)
        self.con.commit()

    def build_all(self):
        """
        Builds all components of the database.
        """
        self.create_tables()
        self.insert_stores_data()
        self.insert_features_data()
        self.insert_sales_train_data()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", type=str,
                        help="Directory containing the data.")
    parser.add_argument("--dbname", type=str, default="sales.db",
                        help="Name of the database to create.")

    args = parser.parse_args()

    db_builder = DatabaseBuilder(args.dbname, args.data_dir)
    db_builder.build_all()


if __name__ == "__main__":
    main()