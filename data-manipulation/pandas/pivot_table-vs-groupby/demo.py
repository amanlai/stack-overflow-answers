import pandas as pd
import numpy as np

# sample
df = pd.DataFrame({"a": [1,1,1,2,2,2], "b": [1,1,2,2,3,3], "c": [0,0.5,1,1,2,2]})

df = pd.DataFrame(np.random.default_rng(0).choice(3, size=(100,3)), columns=['a', 'b', 'c'])


# example
gb = df.groupby(['a','b'])[['c']].sum()
pt = df.pivot_table(index=['a','b'], values=['c'], aggfunc='sum')

# equality test
print(gb.equals(pt))  #True



gb = df.groupby(['a','b'])[['c']].sum().unstack(['b'])
pt = df.pivot_table(index=['a'], columns=['b'], values=['c'], aggfunc='sum')

print(gb.equals(pt))  # True