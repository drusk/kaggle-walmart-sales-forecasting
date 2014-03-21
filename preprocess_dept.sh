#!/bin/bash

function remove {
  echo Removing $1...
  rm -rf $1
}

remove sales.db
remove train_dept
remove test_dept

echo Building database...
./build_db.py data/

echo Building training CSV files...
./build_dept_csv.py sales.db train_dept

echo Building testing CSV file...
./build_dept_csv.py --test sales.db test_dept

echo Extracting training features...
./extract_dept_features.py train_dept

echo Extracting testing features...
./extract_dept_features.py test_dept

echo Training model...
./train_per_dept.py train_dept/ pd.model

echo Done.
echo Predict using ./predict_per_dept.py pd.model test_dept/ output_filename

