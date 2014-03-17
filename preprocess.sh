#!/bin/bash

function remove_file {
  echo Removing $1...
  rm $1
}

remove_file sales.db
remove_file sales.csv
remove_file test.csv
remove_file test.ids
remove_file train.num.csv
remove_file test.num.csv

echo Building database...
./build_db.py data/

echo Building training CSV file...
./build_full_csv.py sales.db

echo Building testing CSV file...
./build_full_csv.py --test sales.db

echo Building IDs file...
./gen_ids.py test.csv 

./extract_features.py sales.csv test.csv train.num.csv test.num.csv

echo Done.
