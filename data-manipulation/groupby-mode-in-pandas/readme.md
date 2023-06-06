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

For easy use, I wrapped this solution in a function that can be found [here](./groupby_mode.py). To use it simply import it as
```python
from groupby_mode import get_groupby_modes
agg_df = get_groupby_modes(source=df, keys=df.columns[:2].tolist(), values=df.columns[-2:].tolist())
```

