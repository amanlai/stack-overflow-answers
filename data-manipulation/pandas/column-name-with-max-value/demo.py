import pandas as pd

df = pd.DataFrame({
    'A': [0.74, 0.33, 0.61], 
    'B': [0.05, 0.00, 0.04],
    'C': [0.11, 0.58, 0.29],
    'D': [0.08, 0.08, 0.04]
})

df['Max'] = df[['A', 'B', 'C', 'D']].idxmax(axis=1)

print(df)

#####################################################################

df = pd.DataFrame({
    'A': [0.74, 0.33, 0.61], 
    'B': [0.05, 0.00, 0.04],
    'C': [0.11, 0.58, 0.29],
    'D': [0.08, 0.08, 0.04]
})

# look for the max values in each row
mxs = df.eq(df.max(axis=1), axis=0)
# join the column names of the max values of each row into a single string
df['Max'] = mxs.dot(mxs.columns + ', ').str.rstrip(', ')
print(df)


#####################################################################


df = pd.DataFrame({
    'A': [0.74, 0.33, 0.61], 
    'B': [0.05, 0.00, 0.04],
    'C': [0.11, 0.58, 0.29],
    'D': [0.08, 0.08, 0.04]
})

mxs = df.eq(df.max(axis=1), axis=0)
df['Max'] = mxs.where(mxs).stack().groupby(level=0).sample(n=1).index.get_level_values(1)
print(df)

#####################################################################


df = pd.DataFrame({
    'A': [0.74, 0.33, 0.61], 
    'B': [0.05, 0.00, 0.04],
    'C': [0.11, 0.58, 0.29],
    'D': [0.08, 0.08, 0.04]
})

# for column names of max value of each row
cols = ['A', 'B', 'C']
mxs = df[cols].eq(df[cols].max(axis=1), axis=0)
df['max among cols'] = mxs.dot(mxs.columns + ', ').str.rstrip(', ')
print(df)