import numpy as np
import pandas as pd
import timeit

def loc(df):
    df['difficulty'] = 'Unknown'
    df.loc[(df['Time']<30) & (df['Time']>0), 'difficulty'] = 'Easy'
    df.loc[(df['Time']>=30) & (df['Time']<=60), 'difficulty'] = 'Medium'
    df.loc[df['Time']>60, 'difficulty'] = 'Hard'
    return df

def np_select(df):
    df['difficulty'] = np.select([df['Time'].between(0, 30, inclusive='neither'), df['Time'].between(30, 60, inclusive='both'), df['Time']>60], ['Easy', 'Medium', 'Hard'], 'Unknown')
    return df

def nested_np_where(df):
    df['difficulty'] = np.where(df['Time'].between(0, 30, inclusive='neither'), 'Easy', np.where(df['Time'].between(30, 60, inclusive='both'), 'Medium', np.where(df['Time'] > 60, 'Hard', 'Unknown')))
    return df


df = pd.DataFrame({'Time': np.random.default_rng().choice(120, size=15_000_000)-30})

t1 = min(timeit.repeat("loc(df.copy())", globals=globals(), number=10, repeat=7)) / 7               # 891 ms
t2 = min(timeit.repeat("np_select(df.copy())", globals=globals(), number=10, repeat=7)) / 7         # 3.93 s
t3 = min(timeit.repeat("nested_np_where(df.copy())", globals=globals(), number=10, repeat=7)) / 7   # 4.82 s