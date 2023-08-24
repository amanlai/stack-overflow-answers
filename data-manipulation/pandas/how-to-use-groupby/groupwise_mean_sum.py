from collections import ChainMap
import pandas as pd

df = pd.DataFrame({
    'dummy': [0, 1, 1], 
    'A': range(3), 
    'B':range(1, 4), 
    'C':range(2, 5)
})

# with default names
x1 = df.groupby('dummy')['B'].agg(['mean', 'sum'])

# using named aggregation
x2 = df.groupby('dummy').agg(Mean=('B', 'mean'), Sum=('B', 'sum'))

x3 = df.groupby("dummy").agg({k: ['sum', 'mean'] for k in ['A', 'B', 'C']})


# convert a list of dictionaries into a dictionary
dct1 = dict(ChainMap(*reversed([{f'{k}_total': (k, 'sum'), f'{k}_mean': (k, 'mean')} for k in ['A','B','C']])))

dct2 = {k:v for k in ['A','B','C'] for k,v in [(f'{k}_total', (k, 'sum')), (f'{k}_avg', (k, 'mean'))]}

# aggregation
x4 = df.groupby('dummy', as_index=False).agg(**dct1)
x5 = df.groupby('dummy', as_index=False).agg(**dct2)