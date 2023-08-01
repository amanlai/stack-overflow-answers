## What is the difference between `groupby` and `pivot_table`

<sup> This is a combination of my posts that were first written as answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/72933069/19123103) and [2](https://stackoverflow.com/a/74048672/19123103). </sup>

### `pivot_table = groupby + unstack` and `groupby = pivot_table + stack` are True.

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

---


### Performance difference: `pivot_table` vs `groupby`

If we peek into the [source code](https://github.com/pandas-dev/pandas/blob/v1.5.0/pandas/core/reshape/pivot.py#L55-L109) of `pivot_table()`, the way it is implemented is that, when you pass a list of aggregator functions a.k.a. aggfuncs to it, for each `func()` in the list, `groupby().func().unstack()` is called and the resulting list of dataframes are concatenated later on. Meanwhile, [`groupby().agg()`](https://github.com/pandas-dev/pandas/blob/87cfe4e38bafe7300a6003a1d18bd80f3f77c763/pandas/core/apply.py#L320) tries to first call cython-optimized methods and use loop as a last resort. 

So if the functions in aggfuncs are all cython-optimized such as `'sum'` or `'size'`, `groupby().agg()` will perform as many times faster than `pivot_table()` as the number of functions in aggfuncs. In particular, for a single aggregator function, they will perform about the same (although, I imagine `pivot_table()` will still be slightly slower since it has a larger overhead). 

However, if the list of functions are not cython-optimized, then since both calls each function in a loop, they will perform about the same. N.B. `groupby().agg().unstack()` makes a call to `unstack()` only once while `pivot_table()` makes the call `len(aggfuncs)` number of times; so naturally, `pivot_table()` will also be slightly slower.

A demonstration of this in code may be found in this repo here: [for Cython-optimized functions](./performance_cython_funcs.py) and [non-Cython-optimized functions](./performance_non_cython_funcs.py).

#### Cython-optimized functions

As can be seen from the benchmarks, the gap between the performance of `groupby().agg().unstack()` and `pivot_table()` increases as the number of aggregator functions increase. For a single aggregator function, they perform about the same but for two functions, `pivot_table()` is about twice as slow and for three functions, it is about 3 times as slow etc.

#### Non-cython-optimized functions

For non-cython optimized functions, `groupby().agg().unstack()` and `pivot_table()` perform about the same even for multiple aggregator functions because both loop over the list of functions under the hood.