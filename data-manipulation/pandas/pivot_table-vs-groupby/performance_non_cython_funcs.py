import numpy as np
import pandas as pd

def groupby_unstack(funcs):
    return df.groupby(['INDEX', 'COLUMN'])['VALUE'].agg(funcs).unstack(level='COLUMN', fill_value=0)

def pivot_table_(funcs):
    return df.pivot_table(index='INDEX', columns='COLUMN', values='VALUE', aggfunc=funcs, fill_value=0)

def get_df(k):
    return pd.DataFrame({'INDEX': np.random.default_rng().choice(k // 2, size=k), 
                         'COLUMN': np.random.default_rng().choice(16, size=k), 
                         'VALUE': np.random.rand(k).round(2)})



df = get_df(80_000)

funcs = [lambda x: list(x.mode()), lambda x: x.nunique()**2]

%timeit groupby_unstack(funcs)
# 26.6 s ± 5.99 s per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit pivot_table_(funcs)
# 27.2 s ± 6.46 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
