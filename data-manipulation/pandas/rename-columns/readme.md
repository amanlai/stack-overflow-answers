## How to rename dataframe columns

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75784571/19123103).</sup>


#### How to rename a column without knowing the label

To change a column name by index, one could alter the underlying array of `df.columns` by index. So
```python
df.columns.array[1] = 'col_1_new_name'
# or
df.columns.values[1] = 'col_1_new_name'
# or 
df.columns.to_numpy()[1] = 'col_1_new_name'
```
They all perform the following transformation (without referencing `B`, it is changed):

[![result][1]][1]
    
However, if a new dataframe copy needs to be returned, `rename` method is the way to go:
```python
df1 = df.rename(columns={list(df)[1]: 'col_1_new_name'})
```
If `df` has many columns, instead of `list(df)`, it might be worth it to call `islice()` from the standard `itertools` library to efficiently select a column label (e.g. the second column name):
```python
from itertools import islice
df1 = df.rename(columns={next(islice(df, 1, 2)): 'col_1_new_name'})
```

  [1]: https://i.stack.imgur.com/ePcBk.png
  [2]: https://stackoverflow.com/a/26336314/19123103