## How to control scientific notation in matplotlib?

<sup>This post is based on my answers to Stack Overflow questions that may be found at 
[1](https://stackoverflow.com/a/75796438/19123103),
[2](https://stackoverflow.com/a/75728279/19123103). </sup>


### Prevent scientific notation

One way to prevent it is via setting style to plain in `ticklabel_format()`.
```python
ax = plt.subplot()
ax.plot(range(2003,2012,1),range(200300,201200,100))
ax.ticklabel_format(useOffset=False, style='plain')
```
Another way to prevent scientific notation is to "widen" the interval where scientific notation is not used using the `scilimits=` parameter.
```python
plt.plot(np.arange(1e6, 3 * 1e7, 1e6))
plt.ticklabel_format(scilimits=(-5, 8))
```
[![result1][1]][1]

Here, scientific notation is used on an axis if the axis limit is less than 10^-5 or greater than 10^8.

By default, scientific notation is used for numbers [smaller than 10^-5 or greater than 10^6][2], so if the highest value of the ticks are in this interval, scientific notation is not used.

So the plot created by 
```python
plt.plot(np.arange(50), np.logspace(0, 6));
plt.ylim((0, 1000000))
```
has scientific notation because 1000000=10^6 but the plot created by
```python
plt.plot(np.arange(50), np.logspace(0, 6));
plt.ylim((0, 999999));
```
does not because the y-limit (999999) is smaller than 10^6, the default limit.

This default limit can be changed by using the `scilimits=` parameter of `ticklabel_format()`; simply pass a tuple of the format: `(low, high)` where the upper limit of the ticks should be in the interval `(10^low, 10^high)`. For example, in the following code (a little extreme example), ticks are shown as full numbers because `np.logspace(0,100)[-1] < 10**101` is True.
```
plt.plot(np.logspace(0, 8), np.logspace(0, 100));
plt.ticklabel_format(scilimits=(0, 101))
```
[![result2][3]][3]




### How to handle `AttributeError: This method only works with the ScalarFormatter`

If you're here wondering why you got the error, 
```none
AttributeError: This method only works with the ScalarFormatter
```
then you got the error because as the error says, `ticklabel_format` only works with `ScalarFormatter` (which formats tick values as numbers), but some tick labels of your plot are not numbers. 

#### 1. Check if the plot has minor ticks that need to be formatted

A common way this error might occur is when you want to format the ticklabels of a plot with two levels of ticks (major and minor) where the major ticks are not scalars. A common way this happens is when a bar plot is plotted with log scale. The easiest way to solve the error is to ditch `ticklabel_format` and use `ScalarFormatter` on both levels of ticks instead.
```python
plt.bar([1,2], [1000, 2000], log=True)

plt.ticklabel_format(axis='y', style='plain')             # <---- error


from matplotlib.ticker import ScalarFormatter
plt.gca().yaxis.set_major_formatter(ScalarFormatter()) 
plt.gca().yaxis.set_minor_formatter(ScalarFormatter());   # <---- OK
```

#### 2. Check if the plot has minor ticks that need to be formatted

Another way is when one axis tick labels are not scalars (as in the OP). In the OP, x-axis tick labels are not numbers so the error was raised (by default both axes are flagged). Specifying `axis='y'` in `ticklabel_format` solves the error.

```python
ax = my_df['stats'].plot(kind='bar', legend=False, xlabel='Month', ylabel='Stats', rot=0)
ax.ticklabel_format(axis='y', scilimits=(0,10))   # <--- no error
ax.ticklabel_format(axis='x', scilimits=(0,10))   # <--- error because ticklabels are strings
```

Also if the y-ticklabels need a thousands separator comma, then `set_yticks()` could be used to change it as such.
```python
ax = my_df['stats'].plot(kind='bar', legend=False, xlabel='Month', ylabel='Stats', rot=0)
ax.set_yticks(ax.get_yticks()[:-1], [f"{int(x):,}" for x in ax.get_yticks()[:-1]]);
```
[![res][4]][4]


  [1]: https://i.stack.imgur.com/yURfZ.png
  [2]: https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/mpl-data/matplotlibrc#L386
  [3]: https://i.stack.imgur.com/lLr77.png
  [4]: https://i.stack.imgur.com/2Qso1.png
