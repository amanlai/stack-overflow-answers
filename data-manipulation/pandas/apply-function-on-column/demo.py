import numpy as np
import pandas as pd


df = pd.DataFrame({'a': range(5)})
df['a'] = df['a'].apply('add', other=1)
print(df)


#######################################################################

def read_data(path, sep=',', usecols=[0]):
    return pd.read_csv(path, sep=sep, usecols=usecols)

df = pd.DataFrame({'paths': ['../x/yz.txt', '../u/vw.txt']})

x = df['paths'].apply(read_data)                            # you don't need lambda
print(x)

y = df['paths'].apply(read_data, args=(',', [0, 1]))        # pass the positional arguments to `args=`
print(y)

z = df['paths'].apply(read_data, sep=',', usecols=[0, 1])   # pass as keyword arguments
print(z)


#######################################################################

df = pd.DataFrame({'a': range(5)})

# add 1 to every element in column `a`
df['a'] += 1

# for every row, subtract column `a` value from column `b` value
df['c'] = df['b'] - df['a']
print(df)

#######################################################################


def func(row):
    if row == 'a':
        return 1
    elif row == 'b':
        return 2
    else:
        return -999


df = pd.DataFrame({'col': ['a', 'b', 'a', 'b', 'a']})

# instead of applying a `func` to each row of a column, use `numpy.select` as below
conditions = [df['col'] == 'a', df['col'] == 'b']
choices = [1, 2]
df['new'] = np.select(conditions, choices, default=-999)
print(df)