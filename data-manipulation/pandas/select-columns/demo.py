import pandas as pd

df = pd.DataFrame({
    'a': [1, 1, 1, 1], 
    'b': [2, 2, 1, 0], 
    'c': [3, 3, 1, 0]
})
cols = ['a', 'b']


df1 = df[cols]
print(df1)


####################################################


cols = ['a', 'b', 'f']
df1 = df.loc[:, df.columns.isin(cols)]   # <----- OK
print(df1)


####################################################


cols = ['a', 'b', 'f']
df1 = df.filter(cols)
print(df1)


####################################################


df1 = df.take([0,2], axis=1)
print(df1)


####################################################


df1 = df.xs(pd.Index(['a', 'b']), axis=1)
print(df1)


df2 = df.xs('col1', level=1, axis=1)
print(df2)

# can select specific columns as well
df3 = df.xs(pd.MultiIndex.from_tuples([('A', 'col1'), ('B', 'col2')]), axis=1)
print(df3)
