## Handling duplicates in a dataframe

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75774190/19123103).</sup>


#### Remove rows with group-wise unique values

Given a dataframe such as the following
```none
id    val1     val2
 1     1.1      2.2
 1     1.1      2.2
 2     2.1      5.5
 3     8.8      6.2
 4     1.1      2.2
 5     8.8      6.2
```
how do we group by `val1` and `val2` and keep rows with multiple occurrences of the same `val1` and `val2` combination?

Here, to best way is to use a boolean mask to filter the relevant rows. One way to create the correct boolean mask is via `duplicated()`

```python
df[df.duplicated(subset=['val1','val2'], keep=False)]
```

Another is via `groupby.transform()`:
```python
msk = df.groupby(['val1', 'val2'])['val1'].transform('size') > 1
df1 = df[msk]
```
The idea is to compute the size of groups and only keep the rows whose group is larger than 1.

[![res][1]][1]


  [1]: https://i.stack.imgur.com/6xIvk.png