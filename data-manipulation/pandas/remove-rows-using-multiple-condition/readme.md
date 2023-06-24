## Deleting rows based on multiple conditions in a pandas dataframe

<sup>It's a post that was first posted as an answer to a Stack Overflow question that can be found [here](https://stackoverflow.com/a/75852256/19123103).</sup>



#### `drop` could be used to drop rows

The most obvious way is to constructing a boolean mask given the condition, filter the index by it to get an array of indices to drop and drop these indices using `drop()`. If the condition is:

> Row with value of col 'one', 'two', **or** 'three' greater than 0; **and** value of col 'four' less than 0 should be deleted.

then the following works.
```python
msk = (df['one'].gt(0) | df['two'].gt(0) | df['three'].gt(0)) & df['four'].lt(0)
idx_to_drop = df.index[msk]
df1 = df.drop(idx_to_drop)
```
The first part of the condition, i.e. `col 'one', 'two', or 'three' greater than 0` can be written a little concisely with `.any(axis=1)`:
```python
msk = df[['one', 'two', 'three']].gt(0).any(axis=1) & df['four'].lt(0)
```
---

#### Keep the complement of the rows to drop

Deleting/removing/dropping rows is the inverse of **keeping rows**. So another way to do this task is to negate (`~`) the boolean mask for dropping rows and filter the dataframe by it.
```python
msk = df[['one', 'two', 'three']].gt(0).any(axis=1) & df['four'].lt(0)
df1 = df[~msk]
```

#### `query()` the rows to keep

`pd.DataFrame.query()` is a pretty readable API for filtering rows to keep. It also "understands" `and`/`or` etc. So the following works.

```python
# negate the condition to drop
df1 = df.query("not ((one > 0 or two > 0 or three > 0) and four < 0)")

# the same condition transformed using de Morgan's laws
df1 = df.query("one <= 0 and two <= 0 and three <= 0 or four >= 0")
```

All of the above perform the following transformation:

[![result][1]][1]


  [1]: https://i.stack.imgur.com/CRe2M.png