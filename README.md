kaggle-walmart-sales-forecasting
================================

See competition description at https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

Pipeline
--------

```
./build_db.py data/  # output: sales.db
./build_full_csv.py sales.db  # output: sales.csv
./extract_features.py sales.csv train.num.csv  # output: train.num.csv
./train_svr.py train.num.csv svr.model  # output: svr.model
./extract_features.py test.csv test.num.csv  # output: test.num.csv
./build_full_csv.py --test sales.db  # output: test.csv
./extract_features.py test.csv test.num.csv  # output: test.num.csv
./predict.py svr.model test.num.csv predictions  # output: predictions
```
