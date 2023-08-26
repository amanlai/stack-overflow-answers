## Plotting a gaussian fit to a histogram

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/76966863/19123103).</sup>

Plotting a gaussian fit onto a histogram is possible using seaborn's `distplot` as follows.
```python
import seaborn as sns
from scipy import stats
sns.distplot(data, kde=False, fit=stats.norm);
```
However, `distplot` is deprecated, so how do we fill in the gap in this functionality?

---

`distplot`'s [source code](https://github.com/mwaskom/seaborn/blob/58cf6285d7299ac6dda83bbd4af8dbd019c58058/seaborn/distributions.py#L2517-L2534) regarding `fit=` parameter is works as follows. 
1. initialize some support array,
2. compute the PDF parameters e.g. mean/std of the given data
3. compute PDF values from it using the mean/std of the given data
4. superimpose a line plot on top of the histogram. 

We can directly "transcribe" the relevant part of the code into a custom function and use it to plot a gaussian fit (doesn't have to be normal; could be any continuous distribution). The resulting function may be found on this repo [here](./add_fit_to_histplot.py)

```python
import numpy as np
import seaborn as sns
from add_fit_to_histplot import add_fit_to_histplot

# sample data
x = np.random.default_rng(0).normal(1, 4, size=500) * 0.1

# plot histogram with gaussian fit
sns.histplot(x, stat='density')
add_fit_to_histplot(x, fit=stats.norm);
```
[![first iteration][1]][1]


If you don't fancy the black edge colors or the colors in general, we can change bar colors, edge colors and the alpha parameter to make the `histplot()` output the same as the default style output of the deprecated `distplot()`.
```python
sns.histplot(x, stat='density', color='#1f77b4', alpha=0.4, edgecolor='none', ax=ax2)
add_fit_to_histplot(x, fit=stats.norm, ax=ax2)
```

[![result][2]][2]

The code used to produce the above figure may be found on this repo [here](./distplot_vs_histplot_demo.py).

---

This answer differs from simply drawing a normal distribution on top of a `histplot()` instance because it fits a gaussian (or any other continuous distribution e.g. gamma) on the histogram where there is data (which is also how the fit is plotted in `distplot()`). The aim is to replicate `distplot()`'s fit functionality as much as possible.

For example, say, you have data that follows the Poisson distribution, plot its histogram and plot a gaussian fit to it. With `add_fit_to_histplot()`, because the support is tied to the data endpoints (and uses Scott's rule for bandwidth), the resulting gaussian fit plot is drawn only where there is corresponding data on the histogram, which is also how it's drawn using `distplot()` (the left subplot below). On the other hand, [ohtotasche][3]'s `normal()` function plots even if there isn't corresponding data, i.e. the left tail of the normal pdf is drawn fully (the right subplot below).

[![difference][5]][5]

The code used to produce the above figure may be found on this repo [here](./demo_no2.py).


  [1]: https://i.stack.imgur.com/bnIfU.png
  [2]: https://i.stack.imgur.com/wGbCi.png
  [5]: https://i.stack.imgur.com/ogfqh.png