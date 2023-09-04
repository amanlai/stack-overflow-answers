## Drop duplicate rows across multiple columns

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75250654/19123103).</sup> 

Given a dataframe such as the following:

```none
    A   B   C
0   foo 0   A
1   foo 1   A
2   foo 1   B
3   bar 1   A
```
how do we drop duplicate rows across multiple columns?

---

The canonical method for this task is `drop_duplicates()` where you can pass multiple columns as a list.
```python
df.drop_duplicates(subset=['A', 'C'], keep=False)
```

Note that `keep=` takes three possible values `'first'`, `'last'` and `False`.

 - first : Drop duplicates except for the first occurrence.
 - last  : Drop duplicates except for the last occurrence.
 - False : Drop all duplicates.

---

Another method is `duplicated()` where you can pass multiple columns as a list.
```python
new_df = df[~df.duplicated(subset=['A', 'C'], keep=False)].copy()
```

You can use `duplicated()` to flag all duplicates and filter out flagged rows. If you need to assign columns to `new_df` later, make sure to call `.copy()` so that you don't get `SettingWithCopyWarning` later on.

[![res1][1]][1]


One nice feature of this method is that you can conditionally drop duplicates with it. For example, to drop all duplicated rows only if column A is equal to `'foo'`, you can use the following code.
```python
new_df = df[~( df.duplicated(subset=['A', 'B', 'C'], keep=False) & df['A'].eq('foo') )].copy()
```
[![res2][2]][2]


Also, if you don't wish to write out columns by name, you can pass slices of `df.columns` to `subset=`. This is also true for `drop_duplicates()` as well.
```python
# to consider all columns for identifying duplicates
df[~df.duplicated(subset=df.columns, keep=False)].copy()

# the same is true for drop_duplicates
df.drop_duplicates(subset=df.columns, keep=False)

# to consider columns in positions 0 and 2 (i.e. 'A' and 'C') for identifying duplicates
df.drop_duplicates(subset=df.columns[[0, 2]], keep=False)
```


  [1]: https://i.stack.imgur.com/6W4wk.png
  [2]: https://i.stack.imgur.com/NsqJl.png