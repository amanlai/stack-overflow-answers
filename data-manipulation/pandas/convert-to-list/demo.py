import math
import pandas as pd

d = [['hello', 1, 'GOOD', 'long.kw'],
     [1.2, 'chipotle', np.nan, 'bingo'],
     ['various', np.nan, 3000, 123.456]]

df = pd.DataFrame(data=d, columns=['A','B','C','D']) 


df['combined_list'] = df[['A', 'B']].values.tolist()
print(df)
print(df.iloc[0, 4])
df.drop(columns=['combined_list'], inplace=True)

df['combined_arr'] = list(df[['A', 'B']].values)
print(df)
print(df.iloc[0, 4])
df.drop(columns=['combined_arr'], inplace=True)


#####################################################################

df['combined'] = [[e for e in row if e==e] for row in df.values.tolist()]
print(df)

df['combined'] = [[e for e in row if not (isinstance(e, float) and math.isnan(e))] for row in df.values.tolist()]
print(df)


cols = ['A', 'B']
df['combined'] = [[e for e in row if e==e] for row in df[cols].values.tolist()]
print(df)