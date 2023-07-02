## How to control scientific notation in matplotlib?
#### How to handle `AttributeError: This method only works with the ScalarFormatter`

<sup>This is an answer I posted as an answer to a Stack Overflow question that can be found [here](https://stackoverflow.com/q/46735745/19123103). </sup>



If you're here wondering why you got the error, 
```none
AttributeError: This method only works with the ScalarFormatter
```
then you got the error because as the error says, `ticklabel_format` only works with `ScalarFormatter` (which formats tick values as numbers), but some tick labels of your plot are not numbers. 

##### 1. Check if the plot has minor ticks that need to be formatted

A common way this error might occur is when you want to format the ticklabels of a plot with two levels of ticks (major and minor) where the major ticks are not scalars. A common way this happens is when a bar plot is plotted with log scale. The easiest way to solve the error is to ditch `ticklabel_format` and use `ScalarFormatter` on both levels of ticks instead.
```python
plt.bar([1,2], [1000, 2000], log=True)

plt.ticklabel_format(axis='y', style='plain')             # <---- error


from matplotlib.ticker import ScalarFormatter
plt.gca().yaxis.set_major_formatter(ScalarFormatter()) 
plt.gca().yaxis.set_minor_formatter(ScalarFormatter());   # <---- OK
```

##### 2. Check if the plot has minor ticks that need to be formatted

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
[![res][1]][1]



  [1]: https://i.stack.imgur.com/2Qso1.png
