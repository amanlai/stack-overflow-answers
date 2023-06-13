import json
import pandas as pd


# deserialize json into a python data structure
with open('EUR_JPY_H8.json') as data_file:
    data = json.load(data_file)

# normalize the list of nested dicts
df1 = pd.json_normalize(data)


# deserialize json into a python data structure
with open('my_data.json', 'r') as f:
    data = json.load(f)

# normalize the python data structure
df2 = pd.json_normalize(data, record_path=['price', 'mid'], meta=[['price', 'time']], record_prefix='mid.')
