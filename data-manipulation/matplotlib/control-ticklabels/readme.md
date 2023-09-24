## Control tick labels

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75692664/19123103).</sup>

The simplest case to change the default setting is to use the values used for x-ticks for x-ticklabels. For example, if using pyplot:
```python
plt.xticks(x)
```

However, setting xticks using the values that are not evenly spaced makes a "bad" plot sometimes. For example, in the following case:
```python
x = [1,2.9,3.1,4,5,6,7,8,9,10]
y = np.random.rand(10)

plt.scatter(x, y)
plt.xticks(x);
```
the x-tick labels are unreadable at some points.

[![res1][1]][1]

It's better if the tick labels are evenly spaced:
```python
plt.scatter(x, y)
plt.xticks(range(min(x), max(x)+1));
```
[![res2][2]][2]

FYI, you can get the limits of an axis by calling `plt.xlim()` or `plt.ylim()` so that you can set more accurate tick labels. Also, with `plt.xticks()` (and `plt.yticks()`), you can set arbitrary tick labels. For example, instead of numbers, tick labels could be strings (e.g. `a`, `b`, `c`).
```python
plt.scatter(x, y)
plt.xticks(range(min(x), max(x)+1));
ymin, ymax = plt.ylim()   # (0.19667230980587072, 1.0097016485006163)
plt.yticks(np.linspace(0, 1, 4), ['0', 'a', 'b', 'c']);
plt.ylim(ymin, ymax);
```

[![res3][3]][3]

The very same graph can be plotted by explicitly creating subplots and setting the properties of the Axes object as well.
```python
fig, ax = plt.subplots(figsize=(5,2))
ax.scatter(x, y)
ax.set(xticks=np.arange(min(x), max(x)+1), yticks=np.linspace(0, 1, 4), yticklabels=['0', 'a', 'b', 'c'], ylim=ax.get_ylim());
```

  [1]: https://i.stack.imgur.com/FqPeT.png
  [2]: https://i.stack.imgur.com/3epYN.png
  [3]: https://i.stack.imgur.com/eNg9V.png