import matplotlib.pyplot as plt


# sample data
x = [0, 1, 2]


# first plot

fig, (ax1, ax2) = plt.subplots(1, 2)

# square, blue, size=10 markers with black edges of width=3
ax1.plot(x, 's', ms=10, mec='black', mew=3)
ax2.scatter(x, x, marker='s', s=100, ec='black', lw=3)



# second plot

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(x, 's')
ax2.scatter(x, x)

# make marker edge width = 3
ax1.lines[0].set_mew(3)     
# or
ax1.lines[0].set_markeredgewidth(3)

# make marker edge width = 3
ax2.collections[0].set_linewidth(3)
# or
ax2.collections[0].set_lw(3)


# change markersize, marker, marker edge color, marker face color, marker edge width
ax1.lines[0].set(markersize=22.36, marker='s', markeredgecolor='black', markerfacecolor='green', markeredgewidth=3)

# change marker size, marker edge color, marker face color, hatch, marker edge width
ax2.collections[0].set(sizes=[500], edgecolor='black', facecolor='green', hatch='|', linewidth=3);

