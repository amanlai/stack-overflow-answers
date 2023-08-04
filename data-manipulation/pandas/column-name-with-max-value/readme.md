## Find the column name which has the maximum value for each row

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/73903067/19123103).</sup>

If we want to get the column label that has the maximum value for each row, the basic method is `idxmax` with `axis=1` set to fetch the column labels. This is analogous to numpy's `argmax()` method.
```python
df.idxmax(axis=1)
```
Following example, illustrates this point.

```python
df = pd.DataFrame({
    'A': [0.74, 0.33, 0.61], 
    'B': [0.05, 0.00, 0.04],
    'C': [0.11, 0.58, 0.29],
    'D': [0.08, 0.08, 0.04]
})
df['Max'] = df[['A', 'B', 'C', 'D']].idxmax(axis=1)
```

which outputs the following dataframe:

```none
   A     B     C     D  Max
0.74  0.05  0.11  0.08    A
0.33  0.00  0.58  0.08    C	 
0.61  0.04  0.29  0.04    A
```


Another solution is to flag the position of the maximum values of each row and get the corresponding column names. In particular, this solution works well if multiple columns contain the maximum value for some rows and you want to return **all column names with the maximum value** for each row:<sup>1</sup>

[![case1][1]][1]

Code:
```python
# look for the max values in each row
mxs = df.eq(df.max(axis=1), axis=0)
# join the column names of the max values of each row into a single string
df['Max'] = mxs.dot(mxs.columns + ', ').str.rstrip(', ')
```

---

A slight variation: If you want to **pick one column randomly** when multiple columns contain the maximum value:

[![case2][2]][2]

Code:
```python
mxs = df.eq(df.max(axis=1), axis=0)
df['Max'] = mxs.where(mxs).stack().groupby(level=0).sample(n=1).index.get_level_values(1)
```
---

You can also do this for specific columns by selecting the columns:
```python
# for column names of max value of each row
cols = ['Communications', 'Search', 'Business']
mxs = df[cols].eq(df[cols].max(axis=1), axis=0)
df['max among cols'] = mxs.dot(mxs.columns + ', ').str.rstrip(', ')
```
---

<sup>1: `idxmax(1)` returns only the first column name with the max value if the max value is the same for multiple columns, which may not be desirable depending on the use case. This solution generalizes `idxmax(1)`; in particular, if the max values are unique in each row, it matches the `idxmax(1)` solution.</sup>


  [1]: https://i.stack.imgur.com/RqOgy.png
  [2]: https://i.stack.imgur.com/kDXd5.png