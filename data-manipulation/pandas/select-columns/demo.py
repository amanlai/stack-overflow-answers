import pandas as pd

df = pd.DataFrame({'a': [1, 1, 1, 1], 'b': [2, 2, 1, 0], 'c': [3, 3, 1, 0]})
cols = ['a', 'b']

df1 = df[cols]


####################################################


cols = ['a', 'b', 'f']
df1 = df.loc[:, df.columns.isin(cols)]   # <----- OK


####################################################

cols = ['a', 'b', 'f']
df1 = df.filter(cols)