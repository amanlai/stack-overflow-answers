## How to change fontsize on matplotlib plots

<sup>This post is based on my answer to a Stack Overflow question that may be found at 
[1](https://stackoverflow.com/a/75633114/19123103),
[2](https://stackoverflow.com/a/75633160/19123103).
</sup>


#### Change ylabel fontsize

The easiest way is to pass the fontsize when creating the label, `plt.ylabel('y-label', fontsize=40)` or `ax.set_ylabel('y-label', fontsize=40)`. However, in some cases, it's not possible to do so; for example the plot may be plotted via a third-party library. In that case, you can set the fontsize by manipulating the `Text` object; one example is via `ax.yaxis.label.set_size(40)`.

`ax.get_ylabel()` returns a string, which doesn't define a `set_fontsize` method but `ax.yaxis.get_label()` returns a `matplotlib.text.Text` object, which does; so the following can be used to change fontsize of ylabel as well.
```python
ax.yaxis.get_label().set_fontsize(40)
```
You can also change the position of the ylabel by calling `set()` on `Text` object:
```python
ax.yaxis.get_label().set(fontsize=40, position=[0.5,0.7])
```

The same logic applies for x-axis labels as well.

A working example is as follows.
```python
fig, ax = plt.subplots(figsize=(5,3))
ax.plot(range(10), range(10))
ax.set(xlabel='Time', ylabel='Value')
ax.xaxis.label.set(fontsize=20, position=(0.9, 0))
ax.yaxis.label.set(fontsize=15, position=(0, 0.9))
```

[![result][1]][1]


  [1]: https://i.stack.imgur.com/YHf7o.png