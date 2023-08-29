## What is the difference between `string` and `object` dtypes in Pandas?

<sup> This is adapted from my answer to a Stack Overflow question that can be found at [1](https://stackoverflow.com/a/76055971/19123103) and [2](https://stackoverflow.com/a/75230706/19123103).</sup>

Since pandas 1.0, there's a new `'string'` dtype where you can keep a Nullable integer dtype after casting a column into a `'string'` dtype. For example, if you want to convert floats to strings without decimals, yet the column contains NaN values that you want to keep as null, you can use `'string'` dtype.
```python
df = pd.DataFrame({
    'Col1': [1.2, 3.4, 5.5, float('nan')]
})

df['Col1'] = df['Col1'].astype('string').str.split('.').str[0]
```
returns
```none
0       1
1       3
2       5
3    <NA>
Name: Col1, dtype: object
```
where `<NA>` is a Nullable integer that you can drop with `dropna()` while `df['Col1'].astype(str)` casts NaNs into strings.

---

As of pandas 1.5.3, there are two main differences between the two dtypes.

#### 1. Null handling

`object` dtype can store not only strings but also mixed data types, so if you want to cast the values into strings, `astype(str)` is the prescribed method. This however casts all values into strings, even NaNs become literal `'nan'` strings. `string` is a nullable dtype, so casting as `'string'` preserves NaNs as null values.
```python
x = pd.Series(['a', float('nan'), 1], dtype=object)
x.astype(str).tolist()          # ['a', 'nan', '1']
x.astype('string').tolist()     # ['a', <NA>, '1']
```
A consequence of this is that string operations (e.g. counting characters, comparison) that are performed on `object` dtype columns return `numpy.int` or `numpy.bool` etc. whereas the same operations performed on `'string'` dtype return nullable `pd.Int64` or `pd.Boolean` dtypes. In particular, NaN comparisons return False (because NaN is not equal to any value) for comparisons performed on `object` dtypes, while `pd.NA` remains `pd.NA` for comparisons performed on `'string'` dtype.
```python
x = pd.Series(['a', float('nan'), 'b'], dtype=object)
x == 'a'

0     True
1    False
2    False
dtype: bool
    
    
y = pd.Series(['a', float('nan'), 'b'], dtype='string')
y == 'a'

0     True
1     <NA>
2    False
dtype: boolean
```

So with `'string'` dtype, null handling is more flexible because you can call `fillna()` etc. to handle null values however you want to.<sup>1</sup>

#### 2. `string` dtype is clearer

If a pandas column is `object` dtype, values in it can be replaced with anything. For example, a string in it can be replaced by an integer and that's OK (e.g. `x` below). It might have unwanted consequences afterwards if you expect each value in it to be strings. `string` dtype does not have that problem because a string can only be replaced by another string (e.g. `y` below).
```python
x = pd.Series(['a', 'b'], dtype=str)
y = pd.Series(['a', 'b'], dtype='string')
x[1] = 3                        # OK
y[1] = 3                        # ValueError
y[1] = '3'                      # OK
```
---
This has the advantage where you can use `select_dtypes()` to select only string columns. In other words, with `object` dtypes, there is no way to identify string columns, but with `'string'` dtypes, there is.
```python
df = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': [[1], [2,3], [4,5]]}).astype({'A': 'string'})
df.select_dtypes('string')      # only selects the string column


    A
0   a
1   b
2   c



df = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': [[1], [2,3], [4,5]]})
df.select_dtypes('object')      # selects the mixed dtype column as well


    A   B
0   a   [1]
1   b   [2, 3]
2   c   [4, 5]
```


#### 3. Memory efficiency

String Dtype `'string'` has storage options (python and pyarrow) and if the strings are short, pyarrow is very efficient. Look at the following example:

```python
lst = np.random.default_rng().integers(1000000, size=1000).astype(str).tolist()

x = pd.Series(lst, dtype=object)
y = pd.Series(lst, dtype='string[pyarrow]')
x.memory_usage(deep=True)       # 63041
y.memory_usage(deep=True)       # 10041
```
As you can see, if the strings are short (at most 6 characters in the example above), pyarrow is consumes over 6 times less memory. However, as the following example shows, if the strings are long, there's barely any difference.
```python
z = x * 1000
w = (y.astype(str) * 1000).astype('string[pyarrow]')
z.memory_usage(deep=True)       # 5970128
w.memory_usage(deep=True)       # 5917128
```

---

<sup>1</sup> Similar intuition already exists for `str.contains`, `str.match` for example.
```python
x = pd.Series(['a', float('nan'), 'b'], dtype=object)
x.str.match('a', na=np.nan)

0     True
1      NaN
2    False
dtype: object
```