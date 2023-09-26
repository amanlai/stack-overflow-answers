## How to plot barcharts

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75760362/19123103).</sup>

### Plot a bar plot from pandas

The first case is to simply select the columns to use in the plotting and call `plot()`.
```python
df[['V1','V2']].plot(kind='bar')
```

Another way: Column labels may be passed as axis labels (y-axis admits multiple column labels). Also, since pandas 1.1, axis labels may be passed into the `plot()` call as well.
```python
df.plot(x='Hour', y=['V1', 'V2'], kind='bar', title="V comp", figsize=(12,6), ylabel='V', rot=0);
```
[![result][1]][1]

---

Another example where bar colors are set and bars are labeled by its height (must have matplotlib>=3.4).

```python
ax = df.plot(x='Hour',                # values on x-axis
             y=['V1', 'V2'],          # values on y-axis
             kind='bar',              # specify that it is a bar-plot
             title="V comp",          # set title
             figsize=(12,6),          # set figure size
             ylabel='V',              # set y-axis label
             rot=0,                   # do not rotate x-ticklabels
             color=['red', 'blue'])   # set bar colors
for heights in ax.containers:
    ax.bar_label(heights)             # label each bar by its height
```
[![result2][2]][2]


  [1]: https://i.stack.imgur.com/qjT09.png
  [2]: https://i.stack.imgur.com/uRUm1.png