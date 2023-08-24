import pandas as pd

df = pd.DataFrame({'id': [1, 1, 1, 2, 2, 2, 2, 3, 4], 'value':[1, 2, 3, 1, 2, 3, 4, 1, 1]})
N = 2

x1 = df.groupby('id').head(N)

x2 = df.groupby('id', as_index=False).nth[:N]

x3 = df.groupby('id', as_index=False).nth([0,2])


x4 = df.sort_values(by=['id', 'value'], ascending=[True, False])
x5 = df1.groupby('id', as_index=False).nth[:N]


msk = df.groupby('id')['value'].rank(method='first', ascending=False) <= N
x6 = df[msk]

x7 = df.loc[msk, 'value']
