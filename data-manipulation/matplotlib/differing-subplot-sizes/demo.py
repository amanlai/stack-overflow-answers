import matplotlib.pyplot as plt
import random


data = random.sample(range(100), k=100)

fig, axs = plt.subplots(2, figsize=(6,4), height_ratios=[1, 2])
axs[0].plot(data)
axs[1].scatter(range(100), data, s=10);


#########################################################################


fig = plt.figure(figsize=(6, 4))

ax1 = fig.add_subplot(2, 1, 1)      # initialize the top Axes
ax1.plot(data)                      # plot the top graph

ax2 = fig.add_subplot(2, 2, 3)      # initialize the bottom left Axes
ax2.scatter(range(100), data, s=10) # plot the bottom left graph

ax3 = fig.add_subplot(2, 2, 4)      # initialize the bottom right Axes
ax3.plot(data)                      # plot the bottom right graph


#########################################################################


fig = plt.figure(figsize=(6,4))
ax1 = fig.add_axes([0.05, 0.6, 0.9, 0.25])  # add the top Axes
ax1.plot(data)                              # plot in the top Axes
ax2 = fig.add_axes([0.25, 0, 0.5, 0.5])     # add the bottom Axes
ax2.scatter(range(100), data, s=10);        # plot in the bottom Axes