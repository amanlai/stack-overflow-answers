It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/75528571/19123103

## Convert columns to string in Pandas

> I have the following DataFrame from a SQL query:
> ```none
> (Pdb) pp total_rows
>      ColumnID  RespondentCount
> 0          -1                2
> 1  3030096843                1
> 2  3030096845                1
> ```
> and I pivot it like this:
> ```python
> total_data = total_rows.pivot_table(cols=['ColumnID'])
> ```
> which produces
> ```none
> (Pdb) pp total_data
> ColumnID         -1            3030096843   3030096845
> RespondentCount            2            1            1
> 
> [1 rows x 3 columns]
> ```
> When I convert this dataframe into a dictionary (using `total_data.to_dict('records')[0]`), I get
> ```python
> {3030096843: 1, 3030096845: 1, -1: 2}
> ```
> but I want to make sure the 303 columns are cast as strings instead of integers so that I get this:
> ```python
> {'3030096843': 1, '3030096845': 1, -1: 2}
> ```


#### 1. `.map(repr)` is very fast

If you want to convert values to strings in a column, consider `.map(repr)`. For multiple columns, consider `.applymap(str)`.
```python
df['col_as_str'] = df['col'].map(repr)

# multiple columns
df[['col1', 'col2']] = df[['col1', 'col2']].applymap(str)
# or
df[['col1', 'col2']] = df[['col1', 'col2']].apply(lambda col: col.map(repr))
```

In fact, a `timeit` test shows that `map(repr)` is 3 times faster than `astype(str)` (and is faster than any other method mentioned on this page). Even for multiple columns, this runtime difference still holds. The following is the runtime plot of various methods mentioned here.

[![perfplot][1]][1]

`astype(str)` has very little overhead but for larger frames/columns, `map`/`applymap` outperforms it. 


---

#### 2. Don't convert to strings in the first place

There's very little reason to convert a numeric column into strings given pandas string methods are not optimized and often get outperformed by vanilla Python string methods. If not numeric, there are dedicated methods for those dtypes. For example, datetime columns should be converted to strings using `pd.Series.dt.strftime()`. 

One way numeric->string seems to be used is in a machine learning context where a numeric column needs to be treated as categorical. In that case, instead of converting to strings, consider other dedicated methods such as `pd.get_dummies` or `sklearn.preprocessing.LabelEncoder` or `sklearn.preprocessing.OneHotEncoder` to process your data instead.

 
---

#### 3. Use `rename` to convert column names to specific types

The specific question in the OP is about converting column _names_ to strings, which can be done by `rename` method:
```python
df = total_rows.pivot_table(columns=['ColumnID'])
df.rename(columns=str).to_dict('records')
# [{'-1': 2, '3030096843': 1, '3030096845': 1}]
```

---


The code used to produce the above plots:
```python
import numpy as np
from perfplot import plot
plot(
    setup=lambda n: pd.Series(np.random.default_rng().integers(0, 100, size=n)),
    kernels=[lambda s: s.astype(str), lambda s: s.astype("string"), lambda s: s.apply(str), lambda s: s.map(str), lambda s: s.map(repr)],
    labels= ['col.astype(str)', 'col.astype("string")', 'col.apply(str)', 'col.map(str)', 'col.map(repr)'],
    n_range=[2**k for k in range(4, 22)],
    xlabel='Number of rows',
    title='Converting a single column into string dtype',
    equality_check=lambda x,y: np.all(x.eq(y)));
plot(
    setup=lambda n: pd.DataFrame(np.random.default_rng().integers(0, 100, size=(n, 100))),
    kernels=[lambda df: df.astype(str), lambda df: df.astype("string"), lambda df: df.applymap(str), lambda df: df.apply(lambda col: col.map(repr))],
    labels= ['df.astype(str)', 'df.astype("string")', 'df.applymap(str)', 'df.apply(lambda col: col.map(repr))'],
    n_range=[2**k for k in range(4, 18)],
    xlabel='Number of rows in dataframe',
    title='Converting every column of a 100-column dataframe to string dtype',
    equality_check=lambda x,y: np.all(x.eq(y)));
```


  [1]: https://i.stack.imgur.com/cr3dc.png