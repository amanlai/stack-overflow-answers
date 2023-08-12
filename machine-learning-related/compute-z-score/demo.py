import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler


df = pd.DataFrame(np.random.default_rng(0).random(size=(100,3)), columns=['col1', 'col2', 'col3'])

cols = ['col1', 'col2']
new_cols = [f"{c}_zscore" for c in cols]

sc = StandardScaler()
df[new_cols] = sc.fit_transform(df[cols])
print(df.head())



df[new_cols] = df[cols].apply(stats.zscore)
print(df.head())



df[new_cols] = (df[cols] - df[cols].mean()) / df[cols].std(ddof=0)
print(df.head())

