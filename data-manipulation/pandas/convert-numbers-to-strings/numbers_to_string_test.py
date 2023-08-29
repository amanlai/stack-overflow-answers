import numpy as np
import matplotlib.pyplot as plt
from perfplot import plot

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5), facecolor='white')
plt.sca(ax1)
plot(
    setup=lambda n: pd.Series(np.random.default_rng().integers(0, 100, size=n)),
    kernels=[lambda s: s.astype(str), lambda s: s.astype("string"), lambda s: s.apply(str), lambda s: s.map(str), lambda s: s.map(repr)],
    labels= ['col.astype(str)', 'col.astype("string")', 'col.apply(str)', 'col.map(str)', 'col.map(repr)'],
    n_range=[2**k for k in range(4, 22)],
    xlabel='Number of rows',
    title='Converting a single column into string dtype',
    equality_check=lambda x,y: np.all(x.eq(y)));
plt.sca(ax2)
plot(
    setup=lambda n: pd.DataFrame(np.random.default_rng().integers(0, 100, size=(n, 100))),
    kernels=[lambda df: df.astype(str), lambda df: df.astype("string"), lambda df: df.applymap(str), lambda df: df.apply(lambda col: col.map(repr))],
    labels= ['df.astype(str)', 'df.astype("string")', 'df.applymap(str)', 'df.apply(lambda col: col.map(repr))'],
    n_range=[2**k for k in range(4, 18)],
    xlabel='Number of rows in dataframe',
    title='Converting every column of a 100-column dataframe to string dtype',
    equality_check=lambda x,y: np.all(x.eq(y)));
fig.savefig('benchmark.png')