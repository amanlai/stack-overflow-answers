## How can I pivot a dataframe?

<sup>This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/73060100/19123103), [2](https://stackoverflow.com/a/73330534/19123103).</sup>

The canonical method to reshape a dataframe by pivoting it is `pivot()`.
```python
df = pd.DataFrame({'A': range(9), 'B': ['a', 'b', 'c']*3, 'C': [*'XXXYYYZZZ']})
agg_df = df.pivot(values='A', index='B', columns='C')
```

"Pivot" may refer to 2 different operations: 

1. Unstacked aggregation (i.e. make the results of `groupby.agg` wider.)
2. Reshaping (similar to pivot in Excel, `reshape` in numpy or `pivot_wider` in R)


#### 1. Aggregation

`pivot_table` or `crosstab` are simply unstacked results of `groupby.agg` operation. In fact, the [source code](https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/pivot.py) shows that, under the hood, the following are true:

- `pivot_table` = `groupby` + `unstack` ([read here](https://stackoverflow.com/a/72933069/19123103) for more info.)
- `crosstab` = `pivot_table`

N.B. You can use list of column names as `index`, `columns` and `values` arguments.
```python
df.groupby(rows+cols)[vals].agg(aggfuncs).unstack(cols)
# equivalently,
df.pivot_table(vals, rows, cols, aggfuncs)
```

##### 1.1. `crosstab` is a special case of `pivot_table`; thus of `groupby` + `unstack`

The following are equivalent:

- `pd.crosstab(df['colA'], df['colB'])`
- `df.pivot_table(index='colA', columns='colB', aggfunc='size', fill_value=0)`
- `df.groupby(['colA', 'colB']).size().unstack(fill_value=0)`

Note that `pd.crosstab` has a significantly larger overhead, so it's significantly slower than both `pivot_table` and `groupby` + `unstack`. In fact, as [noted here](https://stackoverflow.com/q/44229489/19123103), `pivot_table` is slower than `groupby` + `unstack` as well.

#### 2. Reshaping

`pivot` is a more limited version of `pivot_table` where its purpose is to reshape a long dataframe into a long one.

```python
df.set_index(rows+cols)[vals].unstack(cols)
# equivalently, 
df.pivot(rows, cols, vals)
```

##### 2.1. Augment rows/columns

For questions such as: How to make the following 
```none
   A   B
0  a   0
1  a  11
2  a   2
3  a  11
4  b  10
5  b  10
6  b  14
7  c   7
```
into the following:
```none
      a     b    c
0   0.0  10.0  7.0
1  11.0  10.0  NaN
2   2.0  14.0  NaN
3  11.0   NaN  NaN
```

You can also apply the previous insight to multi-column pivot operation as well. There are two cases: 

- **"long-to-long"**: reshape by augmenting the indices

  [![case1][2]][2]

  Code:
   
  ```python
  df = pd.DataFrame({'A': [1, 1, 1, 2, 2, 2], 'B': [*'xxyyzz'], 
                     'C': [*'CCDCDD'], 'E': [100, 200, 300, 400, 500, 600]})
  rows, cols, vals = ['A', 'B'], ['C'], 'E'

  # using pivot syntax
  df1 = (
      df.assign(ix=df.groupby(rows+cols).cumcount())
      .pivot([*rows, 'ix'], cols, vals)
      .fillna(0, downcast='infer')
      .droplevel(-1).reset_index().rename_axis(columns=None)
  )
  
  # equivalently, using set_index + unstack syntax
  df1 = (
      df
      .set_index([*rows, df.groupby(rows+cols).cumcount(), *cols])[vals]
      .unstack(fill_value=0)
      .droplevel(-1).reset_index().rename_axis(columns=None)
  )
  ```
   
- **"long-to-wide"**: reshape by augmenting the columns

  [![case2][3]][3]

  Code:
  ```python
  df1 = (
      df.assign(ix=df.groupby(rows+cols).cumcount())
      .pivot(rows, [*cols, 'ix'])[vals]
      .fillna(0, downcast='infer')
  )
  df1 = df1.set_axis([f"{c[0]}_{c[1]}" for c in df1], axis=1).reset_index()

  # equivalently, using the set_index + unstack syntax
  df1 = (
      df
      .set_index([*rows, df.groupby(rows+cols).cumcount(), *cols])[vals]
      .unstack([-1, *range(-2, -len(cols)-2, -1)], fill_value=0)
  )
  df1 = df1.set_axis([f"{c[0]}_{c[1]}" for c in df1], axis=1).reset_index()
  ```

- minimum case using the `set_index` + `unstack` syntax:

  [![case3][4]][4]

  Code:
  ```python
  df1 = df.set_index(['A', df.groupby('A').cumcount()])['E'].unstack(fill_value=0).add_prefix('Col').reset_index()
  ```

---


#### Call `reset_index()` (along with `add_suffix()`)

Oftentimes, `reset_index()` is needed after you call `pivot_table` or `pivot`. For example, to make the following transformation (where one column _became_ column names)

[![res][1]][1]

you use the following code, where after `pivot`, you add prefix to the newly created column names and convert the index (in this case `"movies"`) back into a column and remove the name of the axis name:
```python
df.pivot(*df).add_prefix('week_').reset_index().rename_axis(columns=None)
```


#### Rename columns aftering pivoting

`pivot_table` or `pivot` call sometimes create a MultiIndex that needs to be flattened. In that case, a further manipulation on the columns object fixes the issue.

If some column names are not strings, you can `map` the column names to strings and `join` them.
```python
df = pd.DataFrame({
    'c0': ['A','A','B','C'],
    'c01': ['A','A1','B','C'],
    'c02': ['b','b','d','c'],
    'v1': [1, 3,4,5],
    'v2': [1, 3,4,5]})

df2 = pd.pivot_table(df, index=["c0"], columns=["c01","c02"], values=["v1","v2"]).reset_index()

df2.columns = ['_'.join(map(str, c)).strip('_') for c in df2]
```

If you want to chain the renaming method to `pivot_table` method to put it in a pipeline, you can do so using `pipe` and `set_axis`. 

Moreover, you can also reorder column levels using `reorder_levels`, e.g. `<c01 value>_<c02 value>_<v1>` instead of `<v1>_<c01 value>_<c02 value>`
```python

df2 = (
    df.pivot_table(index=["c0"], columns=["c01","c02"], values=['1','2'])
    .reorder_levels([1,2,0], axis=1)                # makes "v1","v2" the last level
    .pipe(lambda x: x.set_axis(
        map('_'.join, x)                            # if all column names are strings
        #('_'.join(map(str, c)) for c in x)         # if some column names are not strings
        , axis=1)
         )                                          # rename columns
    .reset_index()
)
```
[![result][1]][1]


  [1]: https://i.stack.imgur.com/JdCrw.png




<sup>1</sup> `pivot_table()` aggregates the values and unstacks it. Specifically, it creates a single flat list out of index and columns, calls `groupby()` with this list as the grouper and aggregates using the passed aggregator methods (the default is `mean`). Then after aggregation, it calls `unstack()` by the list of columns. So internally, **pivot_table = groupby + unstack**. Moreover, if `fill_value` is passed, `fillna()` is called.

   In other words, the method that produces `pv_1` is the same as the method that produces `gb_1` in the example below.

   ```python
   pv_1 = df.pivot_table(index=rows, columns=cols, values=vals, aggfunc=aggfuncs, fill_value=0)
   # internal operation of `pivot_table()`
   gb_1 = df.groupby(rows+cols)[vals].agg(aggfuncs).unstack(cols).fillna(0, downcast="infer")
   pv_1.equals(gb_1) # True
   ```

<sup>2</sup> `crosstab()` calls `pivot_table()`, i.e., **crosstab = pivot_table**. Specifically, it builds a DataFrame out of the passed arrays of values, filters it by the common indices and calls `pivot_table()`. It's more limited than `pivot_table()` because it only allows a one-dimensional array-like as `values`, unlike `pivot_table()` that can have multiple columns as `values`.
</sup>


  [1]: https://i.stack.imgur.com/SlCqF.png
  [2]: https://i.stack.imgur.com/aCG37.png
  [3]: https://i.stack.imgur.com/uLNqo.png
  [4]: https://i.stack.imgur.com/j1CJI.png




You can use list of column names as `index`, `columns` and `values` arguments.
```python
rows, cols, vals, aggfuncs = ['row', 'key'], ['col', 'item'], ['val0', 'val1'], ['mean', 'sum']

df.groupby(rows+cols)[vals].agg(aggfuncs).unstack(cols)
# equivalently,
df.pivot_table(vals, rows, cols, aggfuncs)


df.set_index(rows+cols)[vals].unstack(cols)
# equivalently, 
df.pivot(rows, cols, vals)
```

You can also apply the insight from Question 10 to multi-column pivot operation as well. Simply append the auxiliary index from `groupby().cumcount()` to either `rows` or `cols` depending on how you want your result to be (appending it to `rows` makes the result "long", and appending it to `cols` makes it "wide"). Additionally, calling `droplevel().reset_index()` fixes the surplus and duplicate index issue.

```
# for "long" result
df.assign(ix=df.groupby(rows+cols).cumcount()).pivot(rows+['ix'], cols, vals).droplevel(-1).reset_index()

# for "wide" result
df.assign(ix=df.groupby(rows+cols).cumcount()).pivot(rows, cols+['ix'], vals).droplevel(-1, axis=1).reset_index()
```

For example, the following doesn't work.
```python
df = pd.DataFrame({'A': [1, 1, 2], 'B': ['a', 'a', 'b'], 'C': range(3)})
df.pivot('A','B','C')
```
But the following work:
```python
# long
(
    df.assign(ix=df.groupby(['A','B']).cumcount())
    .pivot(['A','ix'], 'B', 'C')
    .droplevel(-1).reset_index()
)

B  A    a    b
0  1  0.0  NaN
1  1  1.0  NaN
2  2  NaN  2.0



# wide
(
    df.assign(ix=df.groupby(['A','B']).cumcount())
    .pivot('A', ['B', 'ix'], 'C')
    .droplevel(-1, axis=1).reset_index()
)

B  A    a    a    b
0  1  0.0  1.0  NaN
1  2  NaN  NaN  2.0
```





---

`pivot_table()` with `aggfunc` results in aggregated data, which is very similar to a `groupby.agg()`. `pivot()` is simply reshaping and/or stacking data (reminiscent of numpy reshape and stack methods), so naturally, it's related to their pandas cousins, `unstack()` and `stack()`.

In fact, if we check the [source code](https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/pivot.py), internally, each method pair are the same.

1. pivot_table = groupby + unstack
2. pivot = set_index + unstack
3. crosstab = pivot_table

Using the setup in the OP:
```python
from numpy.core.defchararray import add
np.random.seed([3,1415])
n = 20

cols = np.array(['key', 'row', 'item', 'col'])
arr1 = (np.random.randint(5, size=(n, 4)) // [2, 1, 2, 1]).astype(str)

df = pd.DataFrame(add(cols, arr1), columns=cols).join(pd.DataFrame(np.random.rand(n, 2).round(2)).add_prefix('val'))

rows, cols, vals, aggfuncs = ['row', 'key'], ['col', 'val1'], ['val0'], ['mean', 'sum']
```



1. `pivot_table()` aggregates the values and unstacks it. Specifically, it creates a single flat list out of index and columns, calls `groupby()` with this list as the grouper and aggregates using the passed aggregator methods (the default is `mean`). Then after aggregation, it calls `unstack()` by the list of columns. So internally, **pivot_table = groupby + unstack**. Moreover, if `fill_value` is passed, `fillna()` is called.

   In other words, the method that produces `pv_1` is the same as the method that produces `gb_1` in the example below.

```python
pv_1 = df.pivot_table(index=rows, columns=cols, values=vals, aggfunc=aggfuncs, fill_value=0)
# internal operation of `pivot_table()`
gb_1 = df.groupby(rows+cols)[vals].agg(aggfuncs).unstack(cols).fillna(0, downcast="infer")
pv_1.equals(gb_1) # True
```

2. `pivot()` creates a MultiIndex from the column values passed as index and columns, builds a MultiIndex DataFrame and calls `unstack()` by the list of columns. So internally, **pivot = set_index + unstack**.

   In other words, all of the following are True:
```python
# if the entire df needs to be pivoted
pv_2 = df.pivot(index=rows, columns=cols)
# internal operation of `pivot()`
su_2 = df.set_index(rows+cols).unstack(cols)
pv_2.equals(su_2) # True

# if only subset of df.columns need to be considered for pivot, specify so
pv_3 = df.pivot(index=rows, columns=cols, values=vals)
su_3 = df.set_index(rows+cols)[vals].unstack(cols)
pv_3.equals(su_3) # True

# this is the precise method used internally (building a new DF seems to be faster than set_index of an existing one)
pv_4 = df.pivot(index=rows, columns=cols, values=vals)
su_4 = pd.DataFrame(df[vals].values, index=pd.MultiIndex.from_arrays([df[c] for c in rows+cols]), columns=vals).unstack(cols)
pv_4.equals(su_4) # True
```

3. `crosstab()` calls `pivot_table()`, i.e., **crosstab = pivot_table**. Specifically, it builds a DataFrame out of the passed arrays of values, filters it by the common indices and calls `pivot_table()`. It's more limited than `pivot_table()` because it only allows a one-dimensional array-like as `values`, unlike `pivot_table()` that can have multiple columns as `values`.

   In other words, the following is True.
```python
indexes, columns, values = [df[r] for r in rows], [df[c] for c in cols], next(df[v] for v in vals)
# crosstab
ct_5 = pd.crosstab(indexes, columns, values, aggfunc=aggfuncs)
# internal operation (abbreviated)
from functools import reduce
data = pd.DataFrame({f'row_{i}': r for i, r in enumerate(indexes)} | {f'col_{i}': c for i, c in enumerate(columns)} | {'v': values}, 
                    index = reduce(lambda x, y: x.intersection(y.index), indexes[1:]+columns, indexes[0].index)
                   )
pv_5 = data.pivot_table('v', [k for k in data if k[:4]=='row_'], [k for k in data if k[:4]=='col_'], aggfuncs)
ct_5.equals(pv_5) # True
```