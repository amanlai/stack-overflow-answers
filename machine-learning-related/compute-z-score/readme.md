## How to compute z-score

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/74310969/19123103).</sup>

#### `scipy`

Python's scientific library `scipy` has a `stats` module that has `zscore` function that may be called to compute z-score column-wise. The simplest way is to call `stats.zscore` on the DataFrame itself, but it is also possible to call it on each column one-by-one using `apply()`.

```python
cols = ['col1', 'col2']
new_cols = [f"{c}_zscore" for c in cols]
df[new_cols] = df[cols].apply(stats.zscore)
# or

df[new_cols] = stats.zscore(df[cols])
```

#### `pandas`

Another way is to manually compute the z-score. Since z-score is nothing but standard normalization, we can simply compute it manually.

```python
df[new_cols] = (df[cols] - df[cols].mean()) / df[cols].std(ddof=0)
```

#### `scikit-learn`

Another way is to call `StandardScaler()` from scikit-learn. Simply instantiate `StandardScaler` and call `fit_transform` using the relevant columns as input. The result is a numpy array which you can assign back to the dataframe as new columns (or work on the array itself etc.).

```python
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
df[new_cols] = sc.fit_transform(df[cols])
```

A timeit test that may be found on this repo ([here](./timeit_test.py)) shows that `stats.zscore` called on the entire DataFrame is the fastest option.