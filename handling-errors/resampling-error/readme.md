## Resampling error: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex

<sup>This post is reproduced from my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75273282/19123103).</sup>

Because it is designed for time-series data, as the error says, `resample()` works only if the index is datetime, timedelta or period. The following are a few common ways this error may show up.

However, you can also use the `on=` parameter to **use a column as grouper**, without having a datetime index.
```python
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
bars = df.resample('30min', on='Timestamp')['Price'].ohlc()
volumes = df.resample('30min', on='Timestamp')['Volume'].sum()
```
[![res1][1]][1]

<br>

If you have a **MultiIndex dataframe** where one of the index is datetime, then you can use `level=` to select that level as the grouper.
```python
volumes = df.resample('30min', level='Timestamp')['Volume'].sum()
```
[![res2][2]][2]

<br>

You can also use `resample.agg` to pass multiple methods.
```python
resampled = df.resample('30min', on='Timestamp').agg({'Price': 'ohlc', 'Volume': 'sum'})
```
[![res3][3]][3]


  [1]: https://i.stack.imgur.com/FmHVA.png
  [2]: https://i.stack.imgur.com/HKp43.png
  [3]: https://i.stack.imgur.com/fWvbG.png