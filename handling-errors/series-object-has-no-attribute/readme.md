## 'Series' object has no attribute

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/73607873/19123103).</sup>

In general, this error occurs if you try to access an attribute that doesn't exist on an object. For pandas Serieses (or DataFrames), it occurs because you tried to index it using the [attribute access](https://pandas.pydata.org/docs/user_guide/indexing.html#attribute-access) (`.`).

An example case is as follows.
```python
colNames = ['A', 'B']
df = pd.DataFrame(zip(*[range(10)]*2), columns=colNames)
df['D'] = df.colNames[0] + df.colNames[1]                  # <----- error
```

In the case above, `df.colNames[0]` is used to access the value on `colNames[0]` in `df` but `df` doesn't have attribute `colNames`, so the error occurred.<sup>1</sup>

Another case this error may occur is if an index had a white space in it that you didn't know about. For example, the following case reproduces this error.
```python
s = pd.Series([1, 2], index=[' a', 'b'])
s.a
```
In this case, make sure to remove the white space:
```python
s.index = [x.strip() for x in s.index]
# or
s.index = [x.replace(' ', '') for x in s.index]
```

Finally, it's always safe to use `[]` to index a Series (or a DataFrame).

<sup>1: Serieses have the following attributes: `axes`, `dtypes`, `empty`, `index`, `ndim`, `size`, `shape`, `T`, `values`. DataFrames have all of these attributes + `columns`. When you use `df.apply(..., axis=1)`, it iterates over the rows where each row is a Series whose indices are the column names of `df`.</sup>