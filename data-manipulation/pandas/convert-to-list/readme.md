## Convert pandas objects into a list

<sup>This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/73027950/19123103).</sup>

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


  [1]: https://i.stack.imgur.com/OnHHL.png