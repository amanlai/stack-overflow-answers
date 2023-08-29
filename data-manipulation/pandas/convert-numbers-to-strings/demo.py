import pandas as pd

df = pd.DataFrame({'col': range(10)})
df['col_as_str'] = df['col'].map(repr)
print(df)

# multiple columns
df = pd.DataFrame({'col1': range(10), 'col2': range(10, 100, 10)})
df[['col1', 'col2']] = df[['col1', 'col2']].applymap(str)
# or
df[['col1', 'col2']] = df[['col1', 'col2']].apply(lambda col: col.map(repr))
print(df)

### 2. Use `rename` to convert column names to specific types

df = pd.DataFrame([[1, 2], [3, 4]])
print(df.columns.dtype)    # dtype('int64')

df.rename(columns=str, inplace=True)
print(df.columns.dtype)    # dtype('O')