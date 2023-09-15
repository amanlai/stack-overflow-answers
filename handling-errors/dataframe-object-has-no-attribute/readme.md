## How to handle `AttributeError: 'DataFrame' object has no attribute ...`?

<sup>This post is copied from my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75316885/19123103).</sup>

You get `AttributeError: 'DataFrame' object has no attribute ...` when you try to access an attribute your dataframe doesn't have.

A common case is when you try to select a column using `.` instead of `[]` when the column name contains white space (e.g. `'col1 '`). 
```python
df.col1       # <--- error
df['col1 ']   # <--- no error
```

<br>

Another common case is when you try to call a Series method on a DataFrame. For example, `tolist()` (or `map()`) are Series methods so they must be called on a column. If you call them on a DataFrame, you'll get
```none
AttributeError: 'DataFrame' object has no attribute 'tolist'

AttributeError: 'DataFrame' object has no attribute 'map'
```
As [hoang tran](https://stackoverflow.com/a/52552220/19123103) explains, this is what is happening with OP as well. `.str` is a Series accessor and it's not implemented for DataFrames.

<br>

Yet another case is if you have a typo and try to call/access an attribute that's simply not defined; e.g. if you try to call `rows()` instead of `iterrows()`, you'll get 
```none
AttributeError: 'DataFrame' object has no attribute 'rows'
```
You can check the full list of attributes using the following comprehension.
```python
[x for x in dir(pd.DataFrame) if not x.startswith('_')]
```

---

When you assign column names as `df.columns = [['col1', 'col2']]`, `df` is a MultiIndex dataframe now, so to access each column, you'll need to pass a tuple:
```python
df['col1'].str.contains('Product A')    # <---- error
df['col1',].str.contains('Product A')   # <---- no error; note the trailing comma
```
In fact, you can pass a tuple to select a column of any MultiIndex dataframe, e.g.
```python
df['level_1_colname', 'level_2_colname'].str.contains('Product A')
```
---

You can also flatten a MultiIndex column names by mapping a "flattener" function on it. A common one is `''.join`:
```python
df.columns = df.columns.map('_'.join)
```