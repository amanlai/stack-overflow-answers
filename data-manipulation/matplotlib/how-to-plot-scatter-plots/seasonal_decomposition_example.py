from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd

data = pd.Series(range(366)).sample(frac=1).set_axis(pd.date_range('2022', '2023', freq='D'))
fig1 = seasonal_decompose(data).plot()                       # <--- marker sizes are unchanged
fig2 = seasonal_decompose(data).plot()
fig2.axes[3].lines[0].set(markersize=3, markeredgewidth=0);  # <--- change the marker size and edges of the residual plot