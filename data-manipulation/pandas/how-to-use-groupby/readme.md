## How to use group-by to get group sum

<sup> This post is based on my answers to Stack Overflow questions that may be found [here](https://stackoverflow.com/a/72905344/19123103) and [here](https://stackoverflow.com/a/72916928/19123103). </sup>

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


  [1]: https://i.stack.imgur.com/Nx5gv.png
  [2]: https://i.stack.imgur.com/1OKwX.png
