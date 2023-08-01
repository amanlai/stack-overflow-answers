## How to use groupby in pandas

<sup> This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/72905344/19123103), [2](https://stackoverflow.com/a/72916928/19123103), [3](https://stackoverflow.com/a/72918043/19123103), [4](https://stackoverflow.com/a/72919143/19123103). </sup>

#### How to use group-by to get group sum

The canonical way is as follows.
```python
df.groupby(['Fruit','Name']).sum()
```

If you want the aggregated column to have a custom name such as `Total Number`, `Total` etc., then use named aggregation:
```python
df.groupby(['Fruit', 'Name'], as_index=False).agg(**{'Total Number': ('Number', 'sum')})
```
or (if the custom name doesn't need to have a white space in it):
```python
df.groupby(['Fruit', 'Name'], as_index=False).agg(Total=('Number', 'sum'))
```
this is equivalent to SQL query:
```sql
SELECT Fruit, Name, sum(Number) AS Total
FROM df 
GROUP BY Fruit, Name
```
Speaking of SQL, there's `pandasql` module that allows you to query pandas dataFrames in the local environment using SQL syntax. It's not part of Pandas, so will have to be installed separately.
```python
#! pip install pandasql
from pandasql import sqldf
sqldf("""
SELECT Fruit, Name, sum(Number) AS Total
FROM df 
GROUP BY Fruit, Name
""")
```

----

#### Multiple aggregations of the same column

The canonical way to create a groupby object using the grouper, and then call `groupby.agg` with the function names passed as parameters.

```python
df = pd.DataFrame({'dummy': [0, 1, 1], 'A': range(3), 'B':range(1, 4), 'C':range(2, 5)})

# with default names
df.groupby('dummy')['B'].agg(['mean', 'sum'])

# using named aggregation
df.groupby('dummy').agg(Mean=('B', 'mean'), Sum=('B', 'sum'))
```

If you have multiple columns that you need to apply the same multiple aggregation functions on, the simplest way is to use a dictionary comprehension.
```python
df.groupby("dummy").agg({k: ['sum', 'mean'] for k in ['A', 'B', 'C']})
```
[![multiindex][1]][1]

The above results in a dataframe with MultiIndex column. If a flat custom column names are desired, named aggregation is the way to go. 

As [stated in the docs](https://pandas.pydata.org/docs/user_guide/groupby.html#named-aggregation), the keys should be the output column names and the values should be tuples `(column, aggregation function)` for named aggregations. Since there are multiple columns and multiple functions, this results in a nested structure. To flatten it into a single dictionary, you can either use `collections.ChainMap()` or a nested loop.

Also, if you prefer the grouper column (`dummy`) as a column (not index), specify `as_index=False` in `groupby()`.
```python
from collections import ChainMap
# convert a list of dictionaries into a dictionary
dct = dict(ChainMap(*reversed([{f'{k}_total': (k, 'sum'), f'{k}_mean': (k, 'mean')} for k in ['A','B','C']])))
# {'A_total': ('A', 'sum'), 'A_avg': ('A', 'mean'), 'B_total': ('B', 'sum'), 'B_avg': ('B', 'mean'), 'C_total': ('C', 'sum'), 'C_avg': ('C', 'mean')}

# the same result obtained by a nested loop
# dct = {k:v for k in ['A','B','C'] for k,v in [(f'{k}_total', (k, 'sum')), (f'{k}_avg', (k, 'mean'))]}

# aggregation
df.groupby('dummy', as_index=False).agg(**dct)
```
[![flat][2]][2]

---

#### Exclude certain columns

`df.groupby('dummy').sum()` sums values in all columns other than `dummy`. How to group-sum values in _some_ of the columns? That may be done by selecting the desired columns on the groupby object.
```python
df.groupby('dummy')[['A', 'B']].sum()
```
If you want to add a suffix/prefix to the aggregated column names, use `add_suffix()` / `add_prefix()`.
```python
df.groupby('dummy')[["A", "B"]].sum().add_suffix("_total")
```

---

If you want to retain `dummy` as a column after aggregation, set `as_index=False` in `groupby()` or use `reset_index()`.
```python
df.groupby("dummy", as_index=False)[['A', 'B']].sum()

# or
df.groupby("dummy")[['A', 'B']].sum().reset_index()
```

#### Groupby in groupby

How to make the following transformation where the average of group-specific averages are computed?
```none
cluster   org   time          cluster mean(time)
     1      a      8                1         15 #=((8 + 6) / 2 + 23) / 2
     1      a      6   -->          2         54 #=(74 + 34) / 2
     2      h     34                3          6
     1      c     23
     2      d     74
     3      w      6 
```

The easiest method is to call `groupby` twice; once to find group-specific mean values; then to compute the average of the averages.

```python
df.groupby(['cluster', 'org'], as_index=False).mean().groupby('cluster')['time'].mean()
```

Another possible solution is to reshape the dataframe using `pivot_table()` then take `mean()`. Note that it's necessary to pass `aggfunc='mean'` (this averages `time` by `cluster` and `org`).
```python
df.pivot_table(index='org', columns='cluster', values='time', aggfunc='mean').mean()
```

Another possibility is to use `level` parameter of `mean()` after the first `groupby()` to aggregate:
```python
df.groupby(['cluster', 'org']).mean().mean(level='cluster')
```

#### Get the topmost n records within each group

To get the **first N rows of each group**, the canonical way is 

```python
N = 2
df.groupby('id').head(N)
```
Another way is via `groupby().nth[:N]`. The outcome of this call is the same as `groupby().head(N)`. For example, for the top-2 rows for each id, call:
```python
N = 2
df1 = df.groupby('id', as_index=False).nth[:N]
```

---

To get the **largest N values of each group**, I suggest two approaches. 

1. First sort by "id" and "value" (make sure to sort "id" in ascending order and "value" in descending order by using the `ascending` parameter appropriately) and then call `groupby().nth[]`.
   ```python
   N = 2
   df1 = df.sort_values(by=['id', 'value'], ascending=[True, False])
   df1 = df1.groupby('id', as_index=False).nth[:N]
   ```
   <br>

2. Another approach is to rank the values of each group and filter using these ranks.
   ```python
   # for the entire rows
   N = 2
   msk = df.groupby('id')['value'].rank(method='first', ascending=False) <= N
   df1 = df[msk]

   # for specific column rows
   df1 = df.loc[msk, 'value']
   ```

---

Also, instead of slicing, you can also pass a list/tuple/range to a `.nth()` call:
```python
df.groupby('id', as_index=False).nth([0,1])

# doesn't even have to be consecutive
# the following returns 1st and 3rd row of each id
df.groupby('id', as_index=False).nth([0,2])
```




  [1]: https://i.stack.imgur.com/Nx5gv.png
  [2]: https://i.stack.imgur.com/1OKwX.png
