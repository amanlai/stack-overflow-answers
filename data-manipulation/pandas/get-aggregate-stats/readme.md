## Get statistics for each group (such as count, mean, etc)

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75787334/19123103).</sup>

#### `pivot_table` with specific `aggfunc`s

For a dataframe of aggregate statistics, `pivot_table` can be used as well. It produces a table not too dissimilar from Excel pivot table. The basic idea is to pass in the columns to be aggregated as `values=` and grouper columns as `index=` and whatever aggregator functions as `aggfunc=` (all of the optimized functions that are admissible for `groupby.agg` are OK). 

One advantage of `pivot_table` over `groupby.agg` is that for multiple columns it produces a single `size` column whereas `groupby.agg` which creates a `size` column for each column (all except one are redundant).
```python
agg_df = df.pivot_table(
    values=['col3', 'col4', 'col5'], 
    index=['col1', 'col2'], 
    aggfunc=['size', 'mean', 'median']
).reset_index()
# flatten the MultiIndex column (should be omitted if MultiIndex is preferred)
agg_df.columns = [i if not j else f"{j}_{i}" for i,j in agg_df.columns]
```
[![res1][1]][1]

#### Use named aggregation for custom column names

For custom column names, instead of multiple `rename` calls, use named aggregation from the beginning.

From the [docs][2]: 

> To support column-specific aggregation with control over the output column names, pandas accepts the special syntax in GroupBy.agg(), known as “named aggregation”, where
> 
> - The keywords are the output column names
> - The values are tuples whose first element is the column to select and the second element is the aggregation to apply to that column. pandas provides the pandas.NamedAgg namedtuple with the fields ['column', 'aggfunc'] to make it clearer what the arguments are. As usual, the aggregation can be a callable or a string alias.

As an example, to produce aggregate dataframe where each of `col3`, `col4` and `col5` has its mean and count computed, the following code could be used. Note that it does the renaming columns step as part of `groupby.agg`.

```python
aggfuncs = {f'{c}_{f}': (c, f) for c in ['col3', 'col4', 'col5'] for f in ['mean', 'count']}
agg_df = df.groupby(['col1', 'col2'], as_index=False).agg(**aggfuncs)
```
[![res3][3]][3]

Another use case of _named aggregation_ is if each column needs a different aggregator function. For example, if only the mean of `col3`, median of `col4` and `min` of `col5` are needed with custom column names, it can be done using the following code.
```python
agg_df = df.groupby(['col1', 'col2'], as_index=False).agg(col3_mean=('col3', 'mean'), col4_median=('col4', 'median'), col5_min=('col5', 'min'))
# or equivalently,
agg_df = df.groupby(['col1', 'col2'], as_index=False).agg(**{'_'.join(p): p for p in [('col3', 'mean'), ('col4', 'median'), ('col5', 'min')]})
```
[![res2][4]][4]


  [1]: https://i.stack.imgur.com/uDGGE.png
  [2]: https://pandas.pydata.org/docs/user_guide/groupby.html#named-aggregation
  [3]: https://i.stack.imgur.com/0pDSo.png
  [4]: https://i.stack.imgur.com/ZdyJp.png