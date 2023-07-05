## Selecting columns from a dataframe via a list of column names

<sup> This repo is based on my answers to Stack Overflow questions that can be found [here](https://stackoverflow.com/a/75901708/19123103) and [here](https://stackoverflow.com/a/75974729/19123103). </sup>




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


To select columns by index, `take()` could be used.
```python
# select the first and third columns
df1 = df.take([0,2], axis=1)
```
Since this creates a copy by default, you won't get the pesky `SettingWithCopyWarning` with this.

---

Also `xs()` could be used to select columns by label (must pass Series/array/Index).
```python
# select columns A and B
df1 = df.xs(pd.Index(['A', 'B']), axis=1)
```
[![res1][2]][2]

The most useful aspect of `xs` is that it could be used to select MultiIndex columns by level.
```python
df2 = df.xs('col1', level=1, axis=1)

# can select specific columns as well
df3 = df.xs(pd.MultiIndex.from_tuples([('A', 'col1'), ('B', 'col2')]), axis=1)
```
[![res2][3]][3]




  [1]: https://i.stack.imgur.com/8NGFh.png
  [2]: https://i.stack.imgur.com/vRMeO.png
  [3]: https://i.stack.imgur.com/TLU13.png
