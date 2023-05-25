## Change column type in pandas
# sample data
import numpy as np
import pandas as pd

table = [
     ['a',  '1.2',  '4.2' ],
     ['b',  '70',   '0.03'],
     ['x',  '5',    '0'   ],
]
df = pd.DataFrame(table)

### 0. `astype` or `pd.to_numeric` make conversions

df.iloc[:, [1, 2]] = df.iloc[:, [1, 2]].astype(float)
# or
df.iloc[:, [1, 2]] = df.iloc[:, [1, 2]].apply(pd.to_numeric)

### 1. Convert string representation of long floats to numeric values

# If a column contains string representation of really long floats that 
# need to be evaluated with precision (`float` would round them after 
# 15 digits and `pd.to_numeric` is even more imprecise), then use `Decimal` 
# from the standard `decimal` library. The dtype of the column will be `object` 
# but `decimal.Decimal` supports all arithmetic operations, so you can still 
# perform vectorized operations such as arithmetic and comparison operators etc.

from decimal import Decimal
df = pd.DataFrame({'long_float': ["0.1234567890123456789", 
                                  "0.123456789012345678", 
                                  "0.1234567890123456781"]})

df['w_float'] = df['long_float'].astype(float)       # imprecise
df['w_Decimal'] = df['long_float'].map(Decimal)      # precise


# In the example above, `float` converts all of them into the 
# same number whereas `Decimal` maintains their difference:
df['w_Decimal'] == Decimal(df.loc[1, 'long_float'])   # False, True, False
df['w_float'] == float(df.loc[1, 'long_float'])       # True, True, True



##### 2. Convert string representation of long integers to integers

# By default, `astype(int)` converts to `int32`, which wouldn't work 
# (`OverflowError`) if a number is particularly long (such as phone number); 
# try `'int64'` (or even `float`) instead:
df['long_num'] = df['long_num'].astype('int64')


# On a side note, if you get `SettingWithCopyWarning`, then make a copy 
# of your frame and do whatever you were doing again. For example, if you 
# were converting `col1` and `col2` to float dtype, then do:
df = df.copy()
df[['col1', 'col2']] = df[['col1', 'col2']].astype(float)

# or use assign to overwrite the old columns and make a new copy
df = df.assign(**df[['col1', 'col2']].astype(float))

# or enable copy--on-write mode
pd.options.mode.copy_on_write = True
df[['col1', 'col2']] = df[['col1', 'col2']].astype(float)




##### 3. Convert integers to timedelta

# Also, the long string/integer maybe datetime or timedelta, 
# in which case, use `to_datetime` or `to_timedelta` to convert 
# to datetime/timedelta dtype:
df = pd.DataFrame({'long_int': ['1018880886000000000', '1590305014000000000', 
                                '1101470895000000000', '1586646272000000000', 
                                '1460958607000000000']})
df['datetime'] = pd.to_datetime(df['long_int'].astype('int64'))
# or
df['datetime'] = pd.to_datetime(df['long_int'].astype(float))

df['timedelta'] = pd.to_timedelta(df['long_int'].astype('int64'))




##### 4. Convert timedelta to numbers

# To perform the reverse operation (convert datetime/timedelta to numbers), 
# view it as `'int64'`. This could be useful if you were building a machine 
# learning model that somehow needs to include time (or datetime) as a numeric value. 
# Just make sure that if the original data are strings, then they must be converted to 
# timedelta or datetime before any conversion to numbers.

df = pd.DataFrame({'Time diff': ['2 days 4:00:00', '3 days', '4 days', '5 days', '6 days']})
df['Time diff in nanoseconds'] = pd.to_timedelta(df['Time diff']).view('int64')
df['Time diff in seconds'] = pd.to_timedelta(df['Time diff']).view('int64') // 10**9
df['Time diff in hours'] = pd.to_timedelta(df['Time diff']).view('int64') // (3600*10**9)




##### 5. Convert datetime to numbers

# For datetime, the numeric view of a datetime is the time difference between 
# that datetime and the UNIX epoch (1970-01-01).

df = pd.DataFrame({'Date': ['2002-04-15', '2020-05-24', '2004-11-26', '2020-04-11', '2016-04-18']})
df['Time_since_unix_epoch'] = pd.to_datetime(df['Date'], format='%Y-%m-%d').view('int64')


##### 6. `astype` is faster than `to_numeric`

df = pd.DataFrame(np.random.default_rng().choice(1000, size=(10000, 50)).astype(str))
df = pd.concat([df, pd.DataFrame(np.random.rand(10000, 50).astype(str), columns=range(50, 100))], axis=1)

%timeit df.astype(dict.fromkeys(df.columns[:50], int) | dict.fromkeys(df.columns[50:], float))
# 488 ms ± 28 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit df.apply(pd.to_numeric)
# 686 ms ± 45.8 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)