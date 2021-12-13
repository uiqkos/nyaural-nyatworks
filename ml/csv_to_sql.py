import pandas as pd
from sqlite3 import connect

con = connect('data/data')

# train = pd.read_csv('./data/train.csv', index_col='id', header=0, error_bad_lines=False, engine="python")
test = pd.read_csv('toxic/data/test.csv', index_col='id', header=0, error_bad_lines=False, engine="python")

