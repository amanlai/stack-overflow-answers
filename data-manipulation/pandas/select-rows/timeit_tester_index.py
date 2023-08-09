import pandas as pd
import numpy as np
import timeit

n = 20_000_000
df = pd.DataFrame({'NumCol': np.random.rand(n).astype('float16'), 
                   'BoolCol': np.random.default_rng().choice([True, False], size=n)})

t1 = min(timeit.repeat("df.index[df['BoolCol']]", globals=globals(), number=1000, repeat=10)) / 10    # 181 ms
t2 = min(timeit.repeat("df['BoolCol'].pipe(lambda x: x.index[x])", globals=globals(), number=1000, repeat=10)) / 10    # 181 ms
t3 = min(timeit.repeat("df['BoolCol'].loc[lambda x: x].index", globals=globals(), number=1000, repeat=10)) / 10    # 297 ms

print(t1, t2, t3)