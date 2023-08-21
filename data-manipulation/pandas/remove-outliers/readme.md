## Remove outliers in data with several categories

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/74552687/19123103).</sup>

Given a time-series with several products, how do we remove outliers using the Tukey-Fence method?

---

It can be done using the following steps:

1. Compute quantiles
2. Derive inter-quartile range (IQR)
3. Compute fence bounds from IQR
4. Map the fence bounds to the original dataframe
5. Remove the values outside the fence bounds


```python
# compute quantiles
quantiles = df.groupby('prod')['units'].quantile([0.25, 0.75]).unstack()
# compute interquartile range for each prod
iqr = quantiles.diff(axis=1).bfill(axis=1)
# compute fence bounds
fence_bounds = quantiles + iqr * [-1.5, 1.5]

# check if units are outside their respective tukey ranges
df['flag'] = df.merge(fence_bounds, left_on='prod', right_index=True).eval('not (`0.25` < units < `0.75`)').astype(int)
```

[![output][1]][1]


  [1]: https://i.stack.imgur.com/daFdn.png