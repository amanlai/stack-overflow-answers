## Selecting columns from a dataframe via a list of column names

<sup> It's a post that was first posted as an answer to a Stack Overflow question that can be found [here](https://stackoverflow.com/a/75901708/19123103). </sup>

> I have a dataframe with a lot of columns in it. Now I want to select only certain columns. I have saved all the names of the columns that I want to select into a Python list and now I want to filter my dataframe according to this list. 
> 
> I've been trying to do:
> ```python
> df_new = df[[list]]
> ```
> where `list` includes all the column names that I want to select.
> 
> However I get the error:
> ```none
> TypeError: unhashable type: 'list'
> ```
> 
> When I do:
> ```python
> df_new = df[list]
> ```
> I get the error 
> ```none
> KeyError: not in index
> ```
> Any help on this one?


#### 1. `[]` aka `__getitem__()`

The canonical way to select a list of columns from a dataframe is via `[]`.
```python
df = pd.DataFrame({'a': [1, 1, 1, 1], 'b': [2, 2, 1, 0], 'c': [3, 3, 1, 0]})
cols = ['a', 'b']

df1 = df[cols]
```
Note that all column labels in `cols` have to also be `df` (otherwise `KeyError: "... not in index"` will be raised).

One thing to note is that when you want to assign new columns to `df1` as filtered above (e.g. `df1['new'] = 0`), a `SettingWithCopyWarning` will be raised. To silence it, explicitly make a new copy:
```python
df1 = df[cols].copy()
```

#### 2. Handle `KeyError: "... not in index"`
To ensure `cols` contains only column labels that are in `df`, you can call `isin` on the columns and then filter `df`.
```python
cols = ['a', 'b', 'f']
df1 = df[cols]                           # <----- error
df1 = df.loc[:, df.columns.isin(cols)]   # <----- OK
```


#### 3. `filter()`

Another way to select a list of columns from a dataframe is via `filter()`. A nice thing about it is that it creates a copy (so no `SettingWithCopyWarning`) and only selects the column labels in `cols` that exist in the dataframe, so handles the `KeyError` under the hood.
```python
cols = ['a', 'b', 'f']
df1 = df.filter(cols)
```
As can be seen from the output below, `f` in `cols` is ignored because it doesn't exist as a column label in `df`.

[![res][1]][1]


  [1]: https://i.stack.imgur.com/8NGFh.png