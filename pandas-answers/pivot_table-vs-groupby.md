It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/72933069/19123103

## Difference between groupby and pivot_table
> I just started learning Pandas and was wondering if there is any difference between `groupby` and `pivot_table` functions. Can anyone help me understand the difference between them?

**pivot_table = groupby + unstack** and **groupby = pivot_table + stack** hold True.

In particular, if `columns` parameter of `pivot_table()` is not used, then `groupby()` and `pivot_table()` both produce the same result (if the same aggregator function is used).

```python
# sample
df = pd.DataFrame({"a": [1,1,1,2,2,2], "b": [1,1,2,2,3,3], "c": [0,0.5,1,1,2,2]})

# example
gb = df.groupby(['a','b'])[['c']].sum()
pt = df.pivot_table(index=['a','b'], values=['c'], aggfunc='sum')

# equality test
gb.equals(pt) #True
```
---
In general, if we check the [source code](https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/pivot.py), `pivot_table()` internally calls `__internal_pivot_table()`. This function creates a single flat list out of index and columns and calls `groupby()` with this list as the grouper. Then after aggregation, calls `unstack()` on the list of columns.

If columns are never passed, there is nothing to unstack on, so `groupby` and `pivot_table` trivially produce the same output.

A demonstration of this function is:
```python
gb = (
    df
    .groupby(['a','b'])[['c']].sum()
    .unstack(['b'])
)
pt = df.pivot_table(index=['a'], columns=['b'], values=['c'], aggfunc='sum')

gb.equals(pt) # True
```
As `stack()` is the inverse operation of `unstack()`, the following holds True as well:
```python
(
    df
    .pivot_table(index=['a'], columns=['b'], values=['c'], aggfunc='sum')
    .stack(['b'])
    .equals(
        df.groupby(['a','b'])[['c']].sum()
    )
) # True
```

In conclusion, depending on the use case, one is more convenient than the other but they can both be used instead of the other and after correctly applying `stack()`/`unstack()`, both will result in the same output.

However, there's a performance difference between the two methods. In short, `pivot_table()` is slower than `groupby().agg().unstack()`. You can [read more about it from this answer](https://stackoverflow.com/a/74048672/19123103).