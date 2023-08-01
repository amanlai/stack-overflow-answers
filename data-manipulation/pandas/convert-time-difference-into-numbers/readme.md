## How to convert time difference into seconds, minutes

<sup> This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/74132498/19123103). </sup>


#### Convert datetime to UNIX timestamp seconds

When you calculate the difference between two datetimes, the dtype of the difference is `timedelta64[ns]` by default (`ns` in brackets). By changing `[ns]` into `[ms]`, `[s]`, `[m]` etc as you cast the output to a new `timedelta64` object, you can convert the difference into milliseconds, seconds, minutes etc.

For example, to find the number of seconds passed since Unix epoch, subtract datetimes and change dtype. 
```python
df = pd.DataFrame({'time': [pd.to_datetime('2019-01-15 13:25:43')]})
df_unix_sec = (df['time'] - pd.Timestamp('1970-01-01')).astype('timedelta64[s]')
```
N.B. Oftentimes, the differences are very large numbers, so if you want them as integers, use `astype('int64')` (NOT `astype(int)`).
```python
df_unix_sec = (df['time'] - pd.Timestamp('1970-01-01')).astype('timedelta64[s]').astype('int64')
```

For the above example, this yields,
```none
0    1547472343
Name: time, dtype: int64
```

----

Yet another, faster way is integer division:
```python
df['time'].view('int64') / 10**9
```