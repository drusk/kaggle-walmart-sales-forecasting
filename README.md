kaggle-walmart-sales-forecasting
================================

See competition description at https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

Pipeline
--------

```
./build_db.py data/
    # output: sales.db

./build_full_csv.py sales.db
    # output: sales.csv

./build_full_csv.py sales.db --test
    # output: test.csv

./gen_ids test.csv
    # output: test.ids

./extract_features.py sales.csv test.csv train.num.csv test.num.csv
    # output: train.num.csv, test.num.csv

./train_sgdr.py train.num.csv sgdr.model
    # output: sgdr.model

./predict.py sgdr.model test.num.csv test.ids predictions
    # output: predictions
```


Evaluating a Model
------------------
```
./preprocess.sh

./train_sgdr.py train.num.csv sgdr.model

./evaluate.py sgdr.model train.num.csv
```
