## Count the frequency that a value occurs in a dataframe column

<sup> This is a post that first appeared as an answer to a Stack Overflow question that may be found at [1](https://stackoverflow.com/a/76002061/19123103). </sup>



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



  [1]: https://i.stack.imgur.com/vuLrO.png