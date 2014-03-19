#!/usr/bin/env python

"""
Script description.
"""

import argparse
import datetime
import sqlite3

import matplotlib.pyplot as plt


def query_dept_sales(dbname, store_id, dept_id):
    con = sqlite3.connect(dbname)

    cur = con.cursor()
    cur.execute(
        """
        SELECT year, month, day, weekly_sales
        FROM SalesTrain
        WHERE store_id = ? AND dept_id = ?
        """,
        (store_id, dept_id)
    )

    dates = []
    sales = []
    for year, month, day, weekly_sales in cur:
        dates.append(datetime.datetime(year, month, day))
        sales.append(weekly_sales)

    return sales, dates


def plot(sales, dates):
    plt.plot(dates, sales)
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dbname")
    parser.add_argument("store_id")
    parser.add_argument("dept_id")

    args = parser.parse_args()

    sales, dates = query_dept_sales(args.dbname, args.store_id, args.dept_id)
    plot(sales, dates)


if __name__ == "__main__":
    main()
