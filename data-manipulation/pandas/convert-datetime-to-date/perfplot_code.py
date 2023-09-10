import pandas as pd
import perfplot
import matplotlib.pyplot as plt


fig, ax = plt.subplots(facecolor='white', figsize=(7,4))
plt.sca(ax)
perfplot.plot(
    setup=lambda n: pd.Series([pd.Timestamp('now')]*n),
    kernels=[lambda s: s.dt.date, lambda s: s.dt.normalize(), lambda s: s.dt.floor('D')],
    labels= ["col.dt.date", "col.dt.normalize()", "col.dt.floor('D')"],
    n_range=[2**k for k in range(21)],
    xlabel='Length of column',
    title='Removing Time From Datetime',
    equality_check=lambda x,y: all(x.eq(y))
)
fig.savefig('benchmark.png');
