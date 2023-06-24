import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.rand(100,4), columns=['one', 'two', 'three', 'four'])

# case 1
msk = (df['one'].gt(0) | df['two'].gt(0) | df['three'].gt(0)) & df['four'].lt(0)
idx_to_drop = df.index[msk]
df1 = df.drop(idx_to_drop)


msk1 = df[['one', 'two', 'three']].gt(0).any(axis=1) & df['four'].lt(0)
idx_to_drop1 = df.index[msk1]
df2 = df.drop(idx_to_drop1)

df1.equals(df2)



# case 2

msk = df[['one', 'two', 'three']].gt(0).any(axis=1) & df['four'].lt(0)
df1 = df[~msk]


# case 3

# negate the condition to drop
df1 = df.query("not ((one > 0 or two > 0 or three > 0) and four < 0)")

# the same condition transformed using de Morgan's laws
df1 = df.query("one <= 0 and two <= 0 and three <= 0 or four >= 0")