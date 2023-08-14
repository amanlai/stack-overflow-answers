import timeit
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame(np.random.default_rng(0).random(size=(30,100))).add_prefix('col')

t1 = min(timeit.repeat("pd.DataFrame(StandardScaler().fit_transform(df))", 
                       globals=globals(), number=100)) / 5                   # 0.11218072000192478
t2 = min(timeit.repeat("df.apply(stats.zscore)", 
                       globals=globals(), number=100)) / 5                   # 2.476688000001013
t3 = min(timeit.repeat("stats.zscore(df)", 
                       globals=globals(), number=100)) / 5                   # 0.044902299996465445
t4 = min(timeit.repeat("df.sub(df.mean()).div(df.std(ddof=0))", 
                       globals=globals(), number=100)) / 5                   # 0.028368819993920623