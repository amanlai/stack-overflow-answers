## How to draw a trendline to a scatter plot

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75562058/19123103).</sup>

Trendline for a scatter plot is the simple regression line. The `seaborn` library has a function ([`regplot`][1]) that does it in one function call. You can even draw the confidence intervals (with `ci=`; I turned it off in the plot below).
```python
import seaborn as sns
sns.regplot(x=x_data, y=y_data, ci=False, line_kws={'color':'red'});
```
The above call produces the following plot for the following dataset:
```python
import numpy as np
x_data, y_data = np.repeat(np.linspace(0, 9, 100)[None,:], 2, axis=0) + np.random.rand(2, 100)*2
```
[![res][2]][2]

If you were using subplots, you can pass the `ax=` as well.
```python
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1,2, figsize=(12,3))
axs[0].scatter(x_data, y_data)
sns.regplot(x=x_data, y=y_data, ci=False, line_kws={'color':'red'}, ax=axs[1]);
```
[![res2][3]][3]

---

Simple regression coefficients have a closed form solution so you can also solve explicitly for them and plot the regression line along with the scatter plot.

If `x_data` and `y_data` are lists:
```python
x_mean = sum(x_data) / len(x_data)
y_mean = sum(y_data) / len(y_data)
covar = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x_data, y_data))
x_var = sum((xi - x_mean)**2 for xi in x_data)
beta = covar / x_var
alpha = y_mean - beta * x_mean
y_hat = [alpha + beta * xi for xi in x_data]
```
If `x_data` and `y_data` are numpy arrays:
```python
x_mean, y_mean = np.mean(x_data), np.mean(y_data)
beta = np.sum((x_data - x_mean) * (y_data - y_mean)) / np.sum((x_data - x_mean)**2)
alpha = y_mean - beta * x_mean
y_hat = alpha + beta * x_data
```
Then just draw the two plots:
```python
import matplotlib.pyplot as plt
plt.plot(x_data, y_data, 'bo', x_data, y_hat, "r-");
```


  [1]: https://seaborn.pydata.org/generated/seaborn.regplot.html
  [2]: https://i.stack.imgur.com/xCzz0.png
  [3]: https://i.stack.imgur.com/iqIFj.png