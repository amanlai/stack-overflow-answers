import pandas as pd

df = pd.DataFrame({
    'date': [1, 2, 3, 4, 1, 2, 3, 4],
    'prod': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
    'units': [100, 90, 80, 15, 200, 180, 190, 30000]
})

# compute quantiles
quantiles = df.groupby('prod')['units'].quantile([0.25, 0.75]).unstack()
# compute interquartile range for each prod
iqr = quantiles.diff(axis=1).bfill(axis=1)
# compute fence bounds
fence_bounds = quantiles + iqr * [-1.5, 1.5]

# check if units are outside their respective tukey ranges
df['flag'] = df.merge(fence_bounds, left_on='prod', right_index=True).eval('not (`0.25` < units < `0.75`)').astype(int)
