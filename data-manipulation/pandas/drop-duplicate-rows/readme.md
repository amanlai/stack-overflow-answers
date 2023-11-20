## Drop duplicate rows

<sup>This post is based on my answer to a Stack Overflow question that may be found at 
[1](https://stackoverflow.com/a/75250654/19123103),
[2](https://stackoverflow.com/a/75901274/19123103).
</sup> 

### Drop duplicates across multiple rows

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


### Drop duplicates in groups

#### 1. `groupby.head(1)`

The relevant `groupby` method to drop duplicates in each group is `groupby.head(1)`. Note that it is important to pass `1` to select the first row of each date-cid pair.
```python
df1 = df.groupby(['date', 'cid']).head(1)
```

#### 2. `duplicated()` is more flexible

Another method is to use `duplicated()` to create a boolean mask and filter.
```python
df3 = df[~df.duplicated(['date', 'cid'])]
```
An advantage of this method over `drop_duplicates()` is that is can be chained with other boolean masks to filter the dataframe more flexibly. For example, to select the unique cids in Nevada for each date, use:
```python
df_nv = df[df['state'].eq('NV') & ~df.duplicated(['date', 'cid'])]
```

#### 3. `groupby.sample(1)`

Another method to select a unique row from each group to use `groupby.sample()`. Unlike the previous methods mentioned, it selects a row from each group randomly (whereas the others only keep the first row from each group).
```python
df4 = df.groupby(['date', 'cid']).sample(n=1)
```

---

You can verify that `df1`, `df2` (ayhan's output) and `df3` all produce the very same output and `df4` produces an output where `size` and `nunique` of cid match for each date (as required in the OP). In short, the following returns True.
```python
w, x, y, z = [d.groupby('date')['cid'].agg(['size', 'nunique']) for d in (df1, df2, df3, df4)]
w.equals(x) and w.equals(y) and w.equals(z)   # True
```
and `w`, `x`, `y`, `z` all look like the following:
```none
       size  nunique
date        
2005      7        3
2006    237       10
2007   3610      227
2008   1318       52
2009   2664      142
2010    997       57
2011   6390      219
2012   2904       99
2013   7875      238
2014   3979      146
```

  [1]: https://i.stack.imgur.com/6W4wk.png
  [2]: https://i.stack.imgur.com/NsqJl.png