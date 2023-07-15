## How to use group-by to get group sum

<sup> This post is based on my answers to Stack Overflow question that may be found [here](https://stackoverflow.com/a/72905344/19123103). </sup>

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