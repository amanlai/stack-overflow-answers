## When to use `close()`, `clf()` or `cla()`

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/77218935/19123103).</sup>

### When to use cla(), clf() or close()

As [David Zwicker](https://stackoverflow.com/a/8228808/19123103) explained, all these methods clear different things. This post adds some examples to help clarify when to use them.

- If you want to re-use particular configurations of a figure (facecolor, dpi, layout etc.) for another figure, use `fig.clf()` to clear the current objects (including Axes) on the figure. Note that this doesn't delete a previously instantiated Figure instance, but only clears objects on it. So in the following code, a single Figure instance is re-used to produce 2 image files.
  ```python
  fig, ax = plt.subplots()        # instantiate a Figure and an Axes
  ax.plot([0,1,2])                # draw a line plot
  fig.savefig('images/img1.png')
  fig.clf()                       # clear Figure (removes Axes)
  ax = fig.add_subplot()          # add new Axes to previously instantiated `fig`
  ax.plot([1,2,0,0,2,1], 'o')     # draw a scatter plot
  fig.savefig('images/img2.png')
  ```
  Since `fig.clf()` removes the Axes, it's important to add a new one on it in order to plot something.
  
- If you want to re-use a figure but change an Axes on it, then use `ax.cla()` to clear the current objects (e.g. ticks, titles, plots etc.) on the Axes. In particular, the position of an Axes on a figure is an important attribute that could be re-used (e.g. the figure has a small Axes could be superimposed on a larger Axes).

- If want to close a figure window, use `plt.close()`. This is especially useful if you use an IDE with an interactive mode such as Jupyter or Spyder and you don't want to see the figure(s) your script creates. If you use a Python shell such as IDLE (that comes with a Python installation), then it literally closes the window that shows a figure. Even though it closes the window, the Figure instance is still in memory along with whatever objects defined on it. For example in the following code, even though `fig` is closed, it can still be worked on. However, because the figure/Axes was not cleared, whatever was in `fig` persists.
  ```python
  fig, ax = plt.subplots()        # instantiate a Figure and an Axes
  ax.plot([0,1,2])                # draw a line plot
  fig.savefig('images/img1.png')  # save the line plot
  plt.close(fig)                  # close `fig`
  ax.plot([1,2,0,0,2,1], 'o')     # draw a scatter plot on top of the previously plotted lineplot
  fig.savefig('images/img2.png')  # save scatter + line plot
  ```


