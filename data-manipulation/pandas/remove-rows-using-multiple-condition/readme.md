It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/75852256/19123103.

## Deleting rows based on multiple conditions in a pandas dataframe

> I want to delete rows when a few conditions are met:
> 
> An example dataframe is shown below:
> ```none
>         one       two     three      four
> 0 -0.225730 -1.376075  0.187749  0.763307
> 1  0.031392  0.752496 -1.504769 -1.247581
> 2 -0.442992 -0.323782 -0.710859 -0.502574
> 3 -0.948055 -0.224910 -1.337001  3.328741
> 4  1.879985 -0.968238  1.229118 -1.044477
> 5  0.440025 -0.809856 -0.336522  0.787792
> 6  1.499040  0.195022  0.387194  0.952725
> 7 -0.923592 -1.394025 -0.623201 -0.738013
> 8 -1.775043 -1.279997  0.194206 -1.176260
> 9 -0.602815  1.183396 -2.712422 -0.377118
> ```
> I want to delete rows based on the conditions that:
> 
> *Row with value of col 'one', 'two', **or** 'three' greater than 0; **and** value of col 'four' less than 0 should be deleted.* 
> 
> Then I tried to implement as follows:
> ```python
> df = df[df.one > 0 or df.two > 0 or df.three > 0 and df.four < 1]
> ```
> However, it results in a error message as follows:
> ```none
> ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
> ```
> Could someone help me on how to delete based on multiple conditions?




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