import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


plt.plot(range(3))
print(plt.gcf().axes)     # [<Axes: >]


fig, axs = plt.subplots(1, 3)
print(fig.axes)           # [<Axes: >, <Axes: >, <Axes: >]



# plot seasonal decomposition
data = pd.Series(range(100), index=pd.date_range('2020', periods=100, freq='D'))
fig = seasonal_decompose(data).plot()

fig.axes  # get Axes list
# [<Axes: >, <Axes: ylabel='Trend'>, <Axes: ylabel='Seasonal'>, <Axes: ylabel='Resid'>]

ax = fig.axes[3]               # last subplot
ax.lines[0].set_markersize(3)  # make marker size smaller on the last subplot