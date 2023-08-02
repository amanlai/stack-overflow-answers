import pandas as pd

df = pd.DataFrame({'time': [pd.to_datetime('2019-01-15 13:25:43')]})
df_unix_sec = (df['time'] - pd.Timestamp('1970-01-01')).astype('timedelta64[s]')
print(df_unix_sec)

df_unix_sec = (df['time'] - pd.Timestamp('1970-01-01')).astype('timedelta64[s]').astype('int64')
print(df_unix_sec)


df = pd.DataFrame({'date': pd.date_range('2020','2021', 3)})
df['as_int64'] = df['date'].view('int64')
df['seconds_since_epoch'] = df['date'].view('int64') // 10**9
print(df)