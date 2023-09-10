## Convert a datetime column into a date column

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75273393/19123103).</sup>

The default date data type is `datetime` in pandas. However, in Python, we have the `date` type, so in some cases it's useful to store dates instead of datetimes in pandas. For example, the data in the pandas DataFrame has to be stored in a SQL database where the type is `DATE`.

The default method is `dt.date`, which is analogous to Python datetime object's `date()` method. However, there are "better" methods for this task in pandas.

You can also use [`dt.normalize()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.normalize.html) to convert times to midnight (null times don't render) or [`dt.floor`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.floor.html) to floor the frequency to daily:
```python
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp'] = df['timestamp'].dt.normalize()

df['timestamp'] = df['timestamp'].dt.floor('D')
```
Note that this keeps the dtype of the column `datetime64[ns]` because each element is still of type `pd.Timestamp`, whereas `dt.date` converts it to `object` because each element becomes type `datetime.date`.

[![res][1]][1]

Also, it's worth noting that `dt.normalize` and `dt.floor('D')` are both significantly faster (approx. 10 times faster for longer dataframes) than `dt.date`:

[![perfplot][2]][2]

Code used to produce the timings plot may be found on this repo [here](./perfplot_code.py).


  [1]: https://i.stack.imgur.com/BaTuk.png
  [2]: https://i.stack.imgur.com/3FPtP.png