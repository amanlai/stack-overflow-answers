import numpy as np
import pandas as pd
from collections import Counter
import perfplot
import matplotlib.pyplot as plt

gen = lambda N: pd.DataFrame({'col': np.random.default_rng().integers(N, size=N)})
setup_funcs = [
    ('numeric', lambda N: gen(N)),
    ('nullable integer dtype', lambda N: gen(N).astype('Int64')),
    ('object', lambda N: gen(N).astype(str)),
    ('string (extension dtype)', lambda N: gen(N).astype('string')),
    ('categorical', lambda N: gen(N).astype('category')),
    ('datetime', lambda N: pd.DataFrame({'col': np.resize(pd.date_range('2020', '2024', N//10+1), N)}))
]

fig, axs = plt.subplots(3, 2, figsize=(15, 15), facecolor='white', constrained_layout=True)
for i, funcs in enumerate(zip(*[iter(setup_funcs)]*2)):
    for j, (label, func) in enumerate(funcs):
        plt.sca(axs[i, j])
        perfplot.plot(
            setup=func,
            kernels=[
                lambda df: df['col'].value_counts(sort=False),
                lambda df: pd.Series(*reversed(np.unique(df['col'], return_counts=True))),
                lambda df: pd.Series(Counter(df['col'])),
                lambda df: df.groupby('col').size(),
                lambda df: df.groupby('col')['col'].count()
            ],
            labels=['value_counts', 'np.unique', 'Counter', 'groupby.size', 'groupby.count'],
            n_range=[2**k for k in range(21)],
            xlabel='len(df)',
            title=f'Count frequency in {label} column',
            equality_check=lambda x,y: x.eq(y.loc[x.index]).all()
        );