# deserialize json into a python data structure
import json
import pandas as pd

with open('my_data.json', 'r') as f:
    data = json.load(f)

# normalize the python data structure
df = pd.json_normalize(data, record_path=['price', 'mid'], meta=[['price', 'time']], record_prefix='mid.')
