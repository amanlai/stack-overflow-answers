Instead of via `gridspec_kw`, `height_ratios`/`width_ratios` can be passed to `plt.subplots` as kwargs since matplotlib 3.6.0. So the relative height can be set as follows.
```python
import matplotlib.pyplot as plt
import random
data = random.sample(range(100), k=100)

fig, axs = plt.subplots(2, figsize=(6,4), height_ratios=[1, 2])
#                                         ^^^^^^^^^  <---- here
axs[0].plot(data)
axs[1].scatter(range(100), data, s=10);
```
[![result1][1]][1]

---

However, if it's desired to draw subplots of differing sizes, one way is to use `matplotlib.gridspec.GridSpec` but a much simpler way is to pass appropriate positions to `add_subplot()` calls. In the following example, first, the first subplot in a 2x1 layout is plotted. Then instead of plotting in the second subplot of the 2x1 layout, initialize a 2x2 layout but plot in its third subplot (the space for the first two subplots in this layout is already taken by the top plot).
```python
fig = plt.figure(figsize=(6, 4))

ax1 = fig.add_subplot(2, 1, 1)      # initialize the top Axes
ax1.plot(data)                      # plot the top graph

ax2 = fig.add_subplot(2, 2, 3)      # initialize the bottom left Axes
ax2.scatter(range(100), data, s=10) # plot the bottom left graph

ax3 = fig.add_subplot(2, 2, 4)      # initialize the bottom right Axes
ax3.plot(data)                      # plot the bottom right graph
```
[![result2][2]][2]

---

Finally, if it's needed to make a subplot of a custom size, one way is to pass `(left, bottom, width, height)` information to a `add_axes()` call on the figure object.
```python
fig = plt.figure(figsize=(6,4))
ax1 = fig.add_axes([0.05, 0.6, 0.9, 0.25])  # add the top Axes
ax1.plot(data)                              # plot in the top Axes
ax2 = fig.add_axes([0.25, 0, 0.5, 0.5])     # add the bottom Axes
ax2.scatter(range(100), data, s=10);        # plot in the bottom Axes
```
[![result3][3]][3]


  [1]: https://i.stack.imgur.com/UZesY.png
  [2]: https://i.stack.imgur.com/YUZB2.png
  [3]: https://i.stack.imgur.com/tHt2u.png