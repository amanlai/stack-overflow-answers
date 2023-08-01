import pandas as pd

df = pd.DataFrame({'time': [pd.to_datetime('2019-01-15 13:25:43')]})
df_unix_sec = (df['time'] - pd.Timestamp('1970-01-01')).astype('timedelta64[s]')
print(df_unix_sec)

df_unix_sec = (df['time'] - pd.Timestamp('1970-01-01')).astype('timedelta64[s]').astype('int64')
print(df_unix_sec)


