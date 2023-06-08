It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/75358566/19123103

## How to normalize json correctly by Python Pandas

> I want to do is load a json file of forex historical price data by Pandas and do statistic with the data. I have go through many topics on Pandas and parsing json file. I want to pass a json file with extra value and nested list to a pandas dataframe.
> 
> I got a json file `'EUR_JPY_H8.json'`
> 
> First I import the lib that required,
> ```python
> import pandas as pd
> import json
> from pandas.io.json import json_normalize
> ```
> Then load the json file,
> ```python
> with open('EUR_JPY_H8.json') as data_file:    
>     data = json.load(data_file)
> ```
> I got a list below:
> ```none
> [{u'complete': True,
> u'mid': {u'c': u'119.743',
>   u'h': u'119.891',
>   u'l': u'119.249',
>   u'o': u'119.341'},
> u'time': u'1488319200.000000000',
> u'volume': 14651},
> {u'complete': True,
> u'mid': {u'c': u'119.893',
>   u'h': u'119.954',
>   u'l': u'119.552',
>   u'o': u'119.738'},
> u'time': u'1488348000.000000000',
> u'volume': 10738},
> {u'complete': True,
> u'mid': {u'c': u'119.946',
>   u'h': u'120.221',
>   u'l': u'119.840',
>   u'o': u'119.888'},
> u'time': u'1488376800.000000000',
> u'volume': 10041}]
> ```
> Then I pass the list to `json_normalize`. Try to get price which is in the nested list under 'mid'
> ```python
> result = json_normalize(data,'time',['time','volume','complete',['mid','h'],['mid','l'],['mid','c'],['mid','o']])
> ```
> which broke down 'time' data into each integer row by row.
> 
> I have checked related document. I have to pass a string or list object to the 2nd parameter of `json_normalize`. How can I pass the timestamp there without breaking down?
> 
> The columns of my expected output are:
> 
> ```none
>   index  |  time  | volumn  |  completed  |  mid.h  |  mid.l  |  mid.c  |  mid.o 
> ```




The data in the OP (after deserialized from a json string preferably using `json.load()`) is a list of nested dictionaries, which is an ideal data structure for `pd.json_normalize()` because it converts a list of dictionaries and flattens each dictionary into a single row. So the length of the list determines the number of rows and the total number of key-value pairs in the dictionaries determine the number of columns.

```python
with open('EUR_JPY_H8.json') as data_file:
    data = json.load(data_file)
df = pd.json_normalize(data)
```

However, if a value under some key is a list, then that no longer is true because presumably the items in the those lists need to be in their separate rows. For example, if `my_data.json` file is like:
```python
# my_data.json
[
    {'price': {'mid': ['119.743', '119.891', '119.341'], 'time': '123'}},
    {'price': {'mid': ['119.893', '119.954', '119.552'], 'time': '456'}},
    {'price': {'mid': ['119.946', '120.221', '119.840'], 'time': '789'}}
]
```
and then you'll want to put each value in the list as its own row. In that case, you can pass the path to these lists as `record_path=` argument. Also, you can make each record have its accompanying metadata, whose path you can also pass as `meta=` argument.
```python
# deserialize json into a python data structure
import json
with open('my_data.json', 'r') as f:
    data = json.load(f)

# normalize the python data structure
df = pd.json_normalize(data, record_path=['price', 'mid'], meta=[['price', 'time']], record_prefix='mid.')
```
[![res][1]][1]

Ultimately, `pd.json_normalize()` cannot handle anything more complex than this kind of structure. For example, it cannot add another metadata to the above example if it's nested inside another dictionary. Depending on the data, you'll most probably need a recursive function to parse it (FYI, `pd.json_normalize()` is a recursive function as well but it's for a general case and won't work for a lot of specific objects).

Often times, you'll need a combination of `explode()`, `pd.DataFrame(col.tolist())` etc. to completely parse the data.

Pandas also has a convenience function `pd.read_json()` as well but it's even more limited than `pd.json_normalize()` in that it can only correctly parse a json array of one nesting level. Unlike `pd.json_normalize()` however, it deserializes a json string under the hood so you can directly pass the path to a json file to it (no need for `json.load()`). In other words, the following two produce the same output:
```python
df1 = pd.read_json("my_data.json") 
df2 = pd.json_normalize(data, max_level=0)  # here, `data` is deserialized `my_data.json`
df1.equals(df2)  # True
```


  [1]: https://i.stack.imgur.com/z0pLj.png