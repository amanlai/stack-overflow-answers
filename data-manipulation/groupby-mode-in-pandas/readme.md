## GroupBy pandas DataFrame and select most common value

<sup>It's a post that was first posted as an answer to the following Stack Overflow question and can be found [here](https://stackoverflow.com/a/72427324/19123103). </sup>

> I have a data frame with three string columns. I know that the only one value in the 3rd column is valid for every combination of the first two. To clean the data I have to group by data frame by first two columns and select most common value of the third column for each combination.
>
> My code:
> ```python
> import pandas as pd
> from scipy import stats
>
> source = pd.DataFrame({
>    'Country': ['USA', 'USA', 'Russia', 'USA'], 
>    'City': ['New-York', 'New-York', 'Sankt-Petersburg', 'New-York'],
>    'Short name': ['NY', 'New', 'Spb', 'NY']})
>
> source.groupby(['Country','City']).agg(lambda x: stats.mode(x['Short name'])[0])
> ```
>
> Last line of code doesn't work, it says `KeyError: 'Short name'` and if I try to group only by City, then I got an AssertionError. What can I do fix it?


## Use [`DataFrame.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.value_counts.html) for fast solution

The top 3 answers on the relevant Stack Overflow Q&A:

- `source.groupby(['Country','City'])['Short name'].agg(pd.Series.mode)`
- `source.groupby(['Country','City']).agg(lambda x:x.value_counts().index[0])`
- `source.groupby(['Country','City']).agg(lambda x: stats.mode(x)[0])`

are incredibly slow for large datasets. 

Solution using `collections.Counter` is much faster (20-40 times faster than the top 3 methods)

- `source.groupby(['Country', 'City'])['Short name'].agg(lambda srs: Counter(list(srs)).most_common(1)[0][0])`

but still very slow.

Solutions by abw333 and Josh Friedlander are much faster (about 10 times faster than the method using `Counter`). These solutions can be further optimized by using `value_counts` instead (`DataFrame.value_counts` is available since pandas 1.1.0.).

```python
source.value_counts(['Country', 'City', 'Short name']).pipe(lambda x: x[~x.droplevel('Short name').index.duplicated()]).reset_index(name='Count')
```
To make the function account for NaNs like in Josh Friedlander's function, simply turn off `dropna` parameter:
```python
source.value_counts(['Country', 'City', 'Short name'], dropna=False).pipe(lambda x: x[~x.droplevel('Short name').index.duplicated()]).reset_index(name='Count')
```

Using abw333's setup, if we test the runtime difference, for a DataFrame with 1mil rows, `value_counts` is about 10% faster than abw333's solution.
```
scale_test_data = [[random.randint(1, 100),
                    str(random.randint(100, 900)), 
                    str(random.randint(0,2))] for i in range(1000000)]
source = pd.DataFrame(data=scale_test_data, columns=['Country', 'City', 'Short name'])
keys = ['Country', 'City']
vals = ['Short name']

%timeit source.value_counts(keys+vals).pipe(lambda x: x[~x.droplevel(vals).index.duplicated()]).reset_index(name='Count')
# 376 ms ± 3.42 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit mode(source, ['Country', 'City'], 'Short name', 'Count')
# 415 ms ± 1.08 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
```
---

For easy use, I wrapped this solution in a function that you can readily copy paste and use in your own environment. This function can find group modes of multiple columns as well.
```python
def get_groupby_modes(source, keys, values, dropna=True, return_counts=False):
    """
    A function that groups a pandas dataframe by some of its columns (keys) and 
    returns the most common value of each group for some of its columns (values).
    The output is sorted by the counts of the first column in values (because it
    uses pd.DataFrame.value_counts internally).
    An equivalent one-liner if values is a singleton list is:
    (
        source
        .value_counts(keys+values)
        .pipe(lambda x: x[~x.droplevel(values).index.duplicated()])
        .reset_index(name=f"{values[0]}_count")
    )
    If there are multiple modes for some group, it returns the value with the 
    lowest Unicode value (because under the hood, it drops duplicate indexes in a 
    sorted dataframe), unlike, e.g. df.groupby(keys)[values].agg(pd.Series.mode).
    Must have Pandas 1.1.0 or later for the function to work and must have 
    Pandas 1.3.0 or later for the dropna parameter to work.
    -----------------------------------------------------------------------------
    Parameters:
    -----------
    source: pandas dataframe.
        A pandas dataframe with at least two columns.
    keys: list.
        A list of column names of the pandas dataframe passed as source. It is 
        used to determine the groups for the groupby.
    values: list.
        A list of column names of the pandas dataframe passed as source. 
        If it is a singleton list, the output contains the mode of each group 
        for this column. If it is a list longer than 1, then the modes of each 
        group for the additional columns are assigned as new columns.
    dropna: bool, default: True.
        Whether to count NaN values as the same or not. If True, NaN values are 
        treated by their default property, NaN != NaN. If False, NaN values in 
        each group are counted as the same values (NaN could potentially be a 
        most common value).
    return_counts: bool, default: False.
        Whether to include the counts of each group's mode. If True, the output 
        contains a column for the counts of each mode for every column in values. 
        If False, the output only contains the modes of each group for each 
        column in values.
    -----------------------------------------------------------------------------
    Returns:
    --------
    a pandas dataframe.
    -----------------------------------------------------------------------------
    Example:
    --------
    get_groupby_modes(source=df, 
                      keys=df.columns[:2].tolist(), 
                      values=df.columns[-2:].tolist(), 
                      dropna=True,
                      return_counts=False)
    """
    
    def _get_counts(df, keys, v, dropna):
        c = df.value_counts(keys+v, dropna=dropna)
        return c[~c.droplevel(v).index.duplicated()]
    
    counts = _get_counts(source, keys, values[:1], dropna)
    
    if len(values) == 1:
        if return_counts:
            final = counts.reset_index(name=f"{values[0]}_count")
        else:
            final = counts.reset_index()[keys+values[:1]]
    else:
        final = counts.reset_index(name=f"{values[0]}_count", level=values[0])
        if not return_counts:
            final = final.drop(columns=f"{values[0]}_count")
        for v in values:
            counts = _get_counts(source, keys, [v], dropna).reset_index(level=v)
            if return_counts:
                final[[v, f"{v}_count"]] = counts
            else:
                final[v] = counts[v]
        final = final.reset_index()
    return final
```