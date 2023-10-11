## How to set the axis limits

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75797959/19123103).</sup>

The canonical way to set axis limits is via `xlim()` and `ylim()` methods in pyplot and `set_xlim()` and `set_ylim()` on Axes objects.


Also, `ylim` can be set using `Axes.set()`. In fact a whole host of properties can be set via `set()`, such as ticks, ticklabels, labels, title etc. (that were set separately in the OP).
```python
ax = plt.gca()
ax.set(ylim=(20, 250), xlim=(0, 100))
```
Then again, `ylim` (and other properties) can be set in the `plt.subplot` instance as well. For the case in the OP, that would be
```python
aPlot = plt.subplot(321, facecolor='w', title="Year 1", ylim=(20,250), xticks=paramValues, ylabel='Average Price', xlabel='Mark-up')
#                                                       ^^^^  <---- ylim here
plt.plot(paramValues, plotDataPrice[0], color='#340B8C', marker='o', ms=5, mfc='#EB1717');
```


To set `ylim` (and other properties) for multiple subplots, use `plt.setp`. For example, if we include 2 more subplots to OP's code and if we want to set the same properties to all of them, one way to do it would be as follows:
```python
import matplotlib.pyplot as plt
import random

plt.figure(1, figsize = (8.5,11))
plt.suptitle('plot title')
ax = []
paramValues = range(10)
for i in range(1, 4):
    aPlot = plt.subplot(3,2,i, title=f"Year {i}")
    ax.append(aPlot)
    aPlot.plot(paramValues, [random.randint(20,200) for _ in paramValues], color='#340B8C', marker='o', ms=5, mfc='#EB1717')
    aPlot.grid(True);

plt.setp(ax, ylim=(20,250), facecolor='w', xticks=paramValues, ylabel='Average Price', xlabel='Mark-up')
#            ^^^^  <---- ylim here
plt.tight_layout();
```
