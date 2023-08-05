## Convert pandas objects into a list

<sup>This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/73027950/19123103), [2](https://stackoverflow.com/a/73809084/19123103).</sup>

### Convert a DataFrame into a list

When we have the following dataframe `df`,
```python
d = [['hello', 1, 'GOOD', 'long.kw'],
     [1.2, 'chipotle', np.nan, 'bingo'],
     ['various', np.nan, 3000, 123.456]]

df = pd.DataFrame(data=d, columns=['A','B','C','D']) 
```
how do we convert it into a list?

---

The easiest method is to call `tolist()` on the underlying numpy array.
```python
lst = df.values.tolist()
```

Another method is to call `list()` on the underlying numpy array
```python
t['combined_arr'] = list(t.values)
```
It should be noted that this produces a slightly different column from using `.tolist()`. As can be seen from below, `tolist()` creates a nested list while `list()` creates a list of arrays.
```python
t['combined_list'] = t[['A', 'B']].values.tolist()
t['combined_arr'] = list(t[['A', 'B']].values)

t.iloc[0, 4]  # ['hello', 1]
t.iloc[0, 5]  # array(['hello', 1], dtype=object)
```
Depending on the use case, it's sometimes useful to preserve the ndarray type.

---

If you want to combine columns **without** NaN values, then the fastest method is to loop over rows while checking for NaN values. As `NaN!=NaN`, the fastest check is to check if a value equals itself.
```python
t['combined'] = [[e for e in row if e==e] for row in t.values.tolist()]


         A     B     C        D                     combined
0    hello   1.0  GOOD  long.kw  [hello, 1.0, GOOD, long.kw]
1      1.2  10.0   NaN    bingo           [1.2, 10.0, bingo]  <-- no NaN
2  various   NaN  3000  123.456     [various, 3000, 123.456]  <-- no NaN
```

A more complete check is to use `isnan` from the built-in `math` module.
```python
import math
t['combined'] = [[e for e in row if not (isinstance(e, float) and math.isnan(e))] for row in t.values.tolist()]
```
To combine specific columns of non-NaN values, select the columns first:
```python
cols = ['A', 'B']
t['combined'] = [[e for e in row if e==e] for row in t[cols].values.tolist()]
```

### TL;DR: Use `.tolist()`. Don't use `list()`

If we look at the source code of [`.tolist()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.tolist.html), under the hood, `list()` function is being called on the underlying data in the dataframe, so both should produce the same output.

However, it looks like `tolist()` is optimized for columns of Python scalars because I found that calling `list()` on a column was 10 times slower than calling `tolist()`. For the record, I was trying to convert a column of json strings in a very large dataframe into a list and `list()` was taking its sweet time. That inspired me to test the runtimes of the two methods.

FYI, there's no need to call `.to_numpy()` or get `.values` attribute because dataframe columns/Series objects already implement `.tolist()` method. Also, because of how numpy arrays are stored, `list()` and `tolist()` would give different types of scalars (at least) for numeric columns. For example,
```python
type(list(df['budget'].values)[0])     # numpy.int64
type(df['budget'].values.tolist()[0])  # int
```


---

The following perfplot shows the runtime differences between the two methods on various pandas dtype Series objects. Basically, it's showing the runtime differences between the following two methods:

```python
list(df['some_col'])      # list()
df['some_col'].tolist()   # .tolist()
```

As you can see, no matter the size of the column/Series, for numeric and object dtype columns/Series, `.tolist()` method is much faster than `list()`. Not included here but the graphs for `float` and `bool` dtype columns were very similar to that of the `int` dtype column shown here. Also the graph for an object dtype column containing lists was very similar to the graph of string column shown here. Extension dtypes such as `'Int64Dtype'`, `'StringDtype'`, `'Float64Dtype'` etc. also showed similar patterns.

On the other hand, there is virtually no difference between the two methods for `datetime`, `timedelta` and `Categorical` dtype columns.

[![perfplot][2]][2]

Code used to produce the above plot may be found [here](./perfplot_test.py) on the current repo.


  [2]: https://i.stack.imgur.com/ynSJV.png


  [1]: https://i.stack.imgur.com/OnHHL.png