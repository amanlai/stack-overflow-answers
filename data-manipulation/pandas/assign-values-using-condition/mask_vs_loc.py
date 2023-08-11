import timeit
import pandas as pd

def mask(df):
    return df.assign(is_rich=pd.Series('no', index=df.index).mask(df['salary']>50, 'yes'))

df = pd.DataFrame({'salary': np.random.rand(10_000_000)*100})


t1 = min(timeit.repeat("mask(df)", globals=globals(), repeat=10, number=100)) / 10    # 0.391
t2 = min(timeit.repeat("loc(df)", globals=globals(), repeat=10, number=100)) / 10     # 0.558
print(t1, t2)