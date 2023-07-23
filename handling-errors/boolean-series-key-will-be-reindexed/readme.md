## Boolean Series key will be reindexed to match DataFrame index

<sup> This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/73353186/19123103).</sup>

If you got this warning, using `.loc[]` instead of `[]` suppresses this warning.<sup>1</sup>
```python
df.loc[boolean_mask]           # <--------- OK
df[boolean_mask]               # <--------- warning
```

In particular, this is raised if indexers are chained like the following.
```python
df.loc[a_list][df['a_col'].isna()]
```
The easiest solution is to create a single boolean mask the filter.
```python
df[df.index.isin(a_list) & df['a_col'].isna()]
```

You can also chain `.loc[]` indexers:
```python
df.loc[a_list].loc[df['a_col'].isna()]
```
or chain all conditions using `and` inside `query()`:
```python
# if a_list is a list of indices of df
df.query("index in @a_list and a_col != a_col")

# if a_list is a list of values in some other column such as b_col
df.query("b_col in @a_list and a_col != a_col")
```
or chain all conditions using `&` inside `[]` (as in @IanS's post).

---

This warning occurs if

- the index of the boolean mask is **not in the same order** as the index of the dataframe it is filtering.
  ```python
  df = pd.DataFrame({'a_col':[1, 2, np.nan]}, index=[0, 1, 2])
  m1 = pd.Series([True, False, True], index=[2, 1, 0])
  df.loc[m1]       # <--------- OK
  df[m1]           # <--------- warning
  ```

- the index of a boolean mask is a **super set** of the index of the dataframe it is filtering. For example:
  ```python
  m2 = pd.Series([True, False, True, True], np.r_[df.index, 10])
  df.loc[m2]       # <--------- OK
  df[m2]           # <--------- warning
  ```

---

<sup>1: If we look at the source codes of [`[]`](https://github.com/pandas-dev/pandas/blob/main/pandas/core/frame.py) and [`loc[]`](https://github.com/pandas-dev/pandas/blob/main/pandas/core/indexing.py), literally the only difference when the index of the boolean mask is a (weak) super set of the index of the dataframe is that `[]` shows this warning (via `_getitem_bool_array` method) and `loc[]` does not.</sup>