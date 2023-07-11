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


df = get_df(800_000)

cython_funcs1 = ['sum', 'size']

%timeit groupby_unstack(cython_funcs1)
# 1.41 s ± 35.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit pivot_table_(cython_funcs1)
# 3.51 s ± 263 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


cython_funcs2 = ['sum', 'size', 'mean']

%timeit groupby_unstack(cython_funcs2)
# 1.63 s ± 16.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit pivot_table_(cython_funcs2)
# 5.08 s ± 57 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


cython_funcs3 = ['median']

%timeit groupby_unstack(cython_funcs3)
# 1.17 s ± 92.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit pivot_table_(cython_funcs3)
# 1.84 s ± 70.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)