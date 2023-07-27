## How to create a boxplot using mean, min, max and standard deviation

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/76783440/19123103).</sup>

Given the information available (mean, standard deviation, min, max), `errorbar` is probably the only graph that can be plotted but if, say, you want to plot a box plot from aggregated data, matplotlib has `bxp()` method that can be used. Note that it is an Axes-level function (cannot be called as `plt.bxp`). It uses a list of dictionaries where each dictionary contains the data about a specific boxplot.

However, boxplots need median, first and third quartiles at the minimum, which cannot be inferred from mean, standard deviation etc. without further assumptions about the distribution of the dataset. 

Suppose the dataset is normally distributed. Then we can estimate median, first and third quartiles using mean and standard deviation. Using those values, we can also approximate whiskers. Assuming the outliers are not available, we can plot a rudimentary boxplot as follows.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# construct some data
x = np.random.default_rng(0).normal(size=(1000, 8))

means = x.mean(axis=0)
q1 = means + std * stats.norm.ppf(0.25)
q3 = means + std * stats.norm.ppf(0.75)
whislo = q1 - (q3 - q1)*1.5
whishi = q3 + (q3 - q1)*1.5

keys = ['med', 'q1', 'q3', 'whislo', 'whishi']
stats = [dict(zip(keys, vals)) for vals in zip(means, q1, q3, whislo, whishi)]
plt.subplot().bxp(stats, showfliers=False);
```

[![no fliers][1]][1]

---

Now assume we have access to median, first and third quartiles (`median`, `q1`, `q3` below). Furthermore, let's assume we have access to values just below `q1-(q3-q1)*1.5` and just above `q3+(q3-q1)*1.5` which can be used to locate the whiskers. Also, let's assume we have access to values outside the whiskers (`fliers`). Then passing all this information to `bxp()` plots a graph that is the very same one that is plotted by `plt.boxplot`.

```python
# construct some data
x = np.random.default_rng(0).normal(size=(1000, 8))
median = np.median(x, axis=0)
q1 = np.quantile(x, 0.25, axis=0)
q3 = np.quantile(x, 0.75, axis=0)

# compute whiskers' locations
whislo = [np.min(x[x[:, i] > v, i]) for i, v in enumerate(q1 - (q3 - q1)*1.5)]
whishi = [np.max(x[x[:, i] < v, i]) for i, v in enumerate(q3 + (q3 - q1)*1.5)]
# identify fliers
fliers = [x[(x[:, i] < lo) | (x[:, i] > hi), i] for i, (lo, hi) in enumerate(zip(whislo, whishi))]

keys = ['med', 'q1', 'q3', 'whislo', 'whishi', 'fliers']
stats = [dict(zip(keys, vals)) for vals in zip(median, q1, q3, whislo, whishi, fliers)]

plt.subplot().bxp(stats);
```

[![full boxplot][2]][2]

You can verify that the above plot is the very same plot that is plotted by
```python
plt.boxplot(x);
```


  [1]: https://i.stack.imgur.com/VsTiY.png
  [2]: https://i.stack.imgur.com/2AgF4.png