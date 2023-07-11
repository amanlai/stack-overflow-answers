import numpy as np
import pandas as pd
import timeit

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

t1 = np.mean(timeit.repeat("groupby_unstack(cython_funcs1)", globals=globals(), number=1, repeat=7))  # 1.41 s
t2 = np.mean(timeit.repeat("pivot_table_(cython_funcs1)", globals=globals(), number=1, repeat=7))     # 3.51 s
print(t1, t2)

cython_funcs2 = ['sum', 'size', 'mean']

t3 = np.mean(timeit.repeat("groupby_unstack(cython_funcs2)", globals=globals(), number=1, repeat=7))  # 1.63 s
t4 = np.mean(timeit.repeat("pivot_table_(cython_funcs2)", globals=globals(), number=1, repeat=7))     # 5.08 s
print(t3, t4)


cython_funcs3 = ['median']

t5 = np.mean(timeit.repeat("groupby_unstack(cython_funcs3)", globals=globals(), number=1, repeat=7))  # 1.17 s
t6 = np.mean(timeit.repeat("pivot_table_(cython_funcs3)", globals=globals(), number=1, repeat=7))     # 1.84 s
print(t5, t6)