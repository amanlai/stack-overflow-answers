The question may be found here: https://stackoverflow.com/q/22391433/19123103

## Count the frequency that a value occurs in a dataframe column

> I have a dataset
> ```none
> category
> cat a
> cat b
> cat a
> ```
> I'd like to return something like the following which shows the unique values and their frequencies
> ```none
> category   freq 
> cat a       2
> cat b       1
> ```



### TL;DR: `value_counts()` is the way to go. All other methods are inferior

On top of it being idiomatic and easy to call, here are a couple more reasons why it should be used.

#### 1. It is faster than other methods

If you look at the performance plots below, for most of the native pandas dtypes, `value_counts()` is the most efficient (or equivalent to) option.<sup>1</sup> In particular, it's faster than both `groupby.size` and `groupby.count` for all dtypes.

[![perfplot][1]][1]

#### 2. It can make bins for histograms

You can not only count the frequency of each value, you can bin them in one go. For other options, you'll have to go through an additional `pd.cut` step to get the same output. For example,
```python
df = pd.DataFrame({'col': range(100)})

bins = [-float('inf'), 33, 66, float('inf')]
df['col'].value_counts(bins=bins, sort=False)


(-inf, 33.0]    34
(33.0, 66.0]    33
(66.0, inf]     33
Name: col, dtype: int64
```

#### 3. More general than `groupby.count` or `groupby.size`

The main difference between `groupby.count` and `groupby.size` is that `count` counts only non-NaN values while `size` returns the length (which includes NaN), if the column has NaN values.

`value_counts()` is equivalent to `groupby.count` by default but can become equivalent to `groupby.size` if `dropna=False`, i.e. `df['col'].value_counts(dropna=False)`.

---

<sup>1</sup> Code used to produce the perfplot:
```python
import numpy as np
import pandas as pd
from collections import Counter
import perfplot
import matplotlib.pyplot as plt

gen = lambda N: pd.DataFrame({'col': np.random.default_rng().integers(N, size=N)})
setup_funcs = [
    ('numeric', lambda N: gen(N)),
    ('nullable integer dtype', lambda N: gen(N).astype('Int64')),
    ('object', lambda N: gen(N).astype(str)),
    ('string (extension dtype)', lambda N: gen(N).astype('string')),
    ('categorical', lambda N: gen(N).astype('category')),
    ('datetime', lambda N: pd.DataFrame({'col': np.resize(pd.date_range('2020', '2024', N//10+1), N)}))
]

fig, axs = plt.subplots(3, 2, figsize=(15, 15), facecolor='white', constrained_layout=True)
for i, funcs in enumerate(zip(*[iter(setup_funcs)]*2)):
    for j, (label, func) in enumerate(funcs):
        plt.sca(axs[i, j])
        perfplot.plot(
            setup=func,
            kernels=[
                lambda df: df['col'].value_counts(sort=False),
                lambda df: pd.Series(*reversed(np.unique(df['col'], return_counts=True))),
                lambda df: pd.Series(Counter(df['col'])),
                lambda df: df.groupby('col').size(),
                lambda df: df.groupby('col')['col'].count()
            ],
            labels=['value_counts', 'np.unique', 'Counter', 'groupby.size', 'groupby.count'],
            n_range=[2**k for k in range(21)],
            xlabel='len(df)',
            title=f'Count frequency in {label} column',
            equality_check=lambda x,y: x.eq(y.loc[x.index]).all()
        );
```

  [1]: https://i.stack.imgur.com/vuLrO.png