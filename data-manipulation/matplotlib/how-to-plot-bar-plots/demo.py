import pandas as pd
import io

data = """
Hour  V1  V2  A1  A2
   0  15  13  25  37
   1  26  52  21  45
   2  18  45  45  25
   3  65  38  98  14
"""

df = pd.read_csv(io.StringIO(data), sep='  *', engine='python')

ax = df.plot(x='Hour',                # values on x-axis
             y=['V1', 'V2'],          # values on y-axis
             kind='bar',              # specify that it is a bar-plot
             title="V comp",          # set title
             figsize=(12,6),          # set figure size
             ylabel='V',              # set y-axis label
             rot=0,                   # do not rotate x-ticklabels
             color=['red', 'blue'])   # set bar colors
for heights in ax.containers:
    ax.bar_label(heights)             # label each bar by its height