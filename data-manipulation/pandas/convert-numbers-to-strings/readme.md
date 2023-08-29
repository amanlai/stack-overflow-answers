## Convert columns to string in Pandas

<sup> This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75528571/19123103). </sup>


_Most of the time_, `astype()` should be enough.
```python
# for a string column
df['col'] = df['col'].astype(str)

# for nullable string type
df['col'] = df['col'].astype('string')
```

#### 1. `.map(repr)` is very fast

If you want to convert values to strings in a column, consider `.map(repr)`. For multiple columns, consider `.applymap(str)`.
```python
df['col_as_str'] = df['col'].map(repr)

# multiple columns
df[['col1', 'col2']] = df[['col1', 'col2']].applymap(str)
# or
df[['col1', 'col2']] = df[['col1', 'col2']].apply(lambda col: col.map(repr))
```

In fact, a `timeit` test shows that `map(repr)` is 3 times faster than `astype(str)` (and is faster than any other method mentioned on this page). Even for multiple columns, this runtime difference still holds. The following is the runtime plot of various methods mentioned here.

[![perfplot][1]][1]

`astype(str)` has very little overhead but for larger frames/columns, `map`/`applymap` outperforms it. 


---

#### 2. Don't convert to strings in the first place

There's very little reason to convert a numeric column into strings given pandas string methods are not optimized and often get outperformed by vanilla Python string methods. If not numeric, there are dedicated methods for those dtypes. For example, datetime columns should be converted to strings using `pd.Series.dt.strftime()`. 

One way numeric->string seems to be used is in a machine learning context where a numeric column needs to be treated as categorical. In that case, instead of converting to strings, consider other dedicated methods such as `pd.get_dummies` or `sklearn.preprocessing.LabelEncoder` or `sklearn.preprocessing.OneHotEncoder` to process your data instead.

 
---

#### 3. Use `rename` to convert column names to specific types

If you want to convert column _labels_ to strings (not the dataframe body), then `rename()` is the method for that task. Simply passing the string constructor function `str()` to the `rename()` method does the job.
```python
df = pd.DataFrame([[1, 2], [3, 4]])
df.columns.dtype    # dtype('int64')

df.rename(columns=str, inplace=True)
df.columns.dtype    # dtype('O')
```


---


The code used to produce the runtime timing plot may be found on the current repo [here](./numbers_to_string_test.py).


  [1]: https://i.stack.imgur.com/cr3dc.png