## ValueError: Columns must be same length as key

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/73443047/19123103).</sup>

To solve this error, check the shape of the object you're trying to assign the df columns (using `np.shape`). The second (or the last) dimension must match the number of columns you're trying to assign to. For example, if you try to assign a 2-column numpy array to 3 columns, you'll see this error. 

A general workaround (for **case 1** and **case 2** below) is to cast the object you're trying to assign to a DataFrame and `join()` it to `df`, i.e. instead of (1), use (2).
```python
df[cols] = vals   # (1)
df = df.join(vals) if isinstance(vals, pd.DataFrame) else df.join(pd.DataFrame(vals))  # (2)
```
If you're trying to replace values in an existing column and got this error (**case 3(a)** below), convert the object to list and assign.
```python
df[cols] = vals.values.tolist()
```
If you have duplicate columns (**case 3(b)** below), then there's no easy fix. You'll have to make the dimensions match manually.

<br>

---


This error occurs in 3 cases:

**Case 1:** When you try to assign a list-like object (e.g. lists, tuples, sets, numpy arrays, and pandas Series) to a list of DataFrame column(s) as new arrays<sup>1</sup> but the number of columns doesn't match the second (or last) dimension (found using `np.shape`) of the list-like object. So the following reproduces this error:
```python
df = pd.DataFrame({'A': [0, 1]})
cols, vals = ['B'], [[2], [4, 5]]
df[cols] = vals # number of columns is 1 but the list has shape (2,)
```
Note that if the columns are not given as list, pandas Series, numpy array or Pandas Index, this error won't occur. So the following doesn't reproduce the error:
```python
df[('B',)] = vals # the column is given as a tuple
```
One interesting edge case occurs when the list-like object is multi-dimensional (but not a numpy array). In that case, under the hood, the object is cast to a pandas DataFrame first and is checked if its last dimension matches the number of columns. This produces the following interesting case:
```python
# the error occurs below because pd.DataFrame(vals1) has shape (2, 2) and len(['B']) != 2
vals1 = [[[2], [3]], [[4], [5]]]
df[cols] = vals1

# no error below because pd.DataFrame(vals2) has shape (2, 1) and len(['B']) == 1
vals2 = [[[[2], [3]]], [[[4], [5]]]]
df[cols] = vals2
```
**Case 2:** When you try to assign a DataFrame to a list (or pandas Series or numpy array or pandas Index) of columns but the respective numbers of columns don't match. This case is what caused the error in the OP. The following reproduce the error:
```python
df = pd.DataFrame({'A': [0, 1]})
df[['B']] = pd.DataFrame([[2, 3], [4]]) # a 2-column df is trying to be assigned to a single column

df[['B', 'C']] = pd.DataFrame([[2], [4]]) # a single column df is trying to be assigned to 2 columns
```
**Case 3:** When you try to replace the values of existing column(s) by a DataFrame (or a list-like object) whose number of columns doesn't match the number of columns it's replacing. So the following reproduce the error:
```python
# case 3(a)
df1 = pd.DataFrame({'A': [0, 1]})
df1['A'] = pd.DataFrame([[2, 3], [4, 5]]) # df1 has a single column named 'A' but a 2-column-df is trying to be assigned

# case 3(b): duplicate column names matter too
df2 = pd.DataFrame([[0, 1], [2, 3]], columns=['A','A'])
df2['A'] = pd.DataFrame([[2], [4]]) # df2 has 2 columns named 'A' but a single column df is being assigned
```


<sup>1</sup>: `df.loc[:, cols] = vals` may overwrite data inplace, so this won't produce the error but will create columns of NaN values.