## Convert Pandas Column to DateTime

<sup> This is based on my answers to Stack Overflow questions that can be found [here](https://stackoverflow.com/q/26763344/19123103) and [here](https://stackoverflow.com/a/75253473/19123103). </sup>

#### Multiple datetime columns

If you want to convert multiple string columns to datetime, then using `apply()` would be useful.
```python
df[['date1', 'date2']] = df[['date1', 'date2']].apply(pd.to_datetime)
```
You can pass parameters to `to_datetime` as kwargs.
```python
df[['start_date', 'end_date']] = df[['start_date', 'end_date']].apply(pd.to_datetime, format="%m/%d/%Y")
```

Passing to `apply`, without specifying `axis`, still converts values vectorially *for each column*. `apply` is needed here because `pd.to_datetime` can only be called on a single column. If it has to be called on multiple columns, the options are either use an explicit `for-loop`, or pass it to `apply`. On the other hand, if you call `pd.to_datetime` using `apply` on a column (e.g. `df['date'].apply(pd.to_datetime))`, that would not be vectorized, and should be avoided.


#### `errors='coerce'` is useful

If some rows are not in the correct format or not datetime at all, `errors=` parameter is very useful, so that you can convert the valid rows and handle the rows that contained invalid values later.
```python
df['date'] = pd.to_datetime(
    df['date'], format='%d%b%Y:%H:%M:%S.%f', errors='coerce')

# for multiple columns
df[['start', 'end']] = df[['start', 'end']].apply(
    pd.to_datetime, format='%d%b%Y:%H:%M:%S.%f', errors='coerce')
```

#### Setting the correct `format=` is much faster than letting pandas find out<sup>1</sup>

If the column contains a **time** component and you know the format of the datetime/time, then passing the format explicitly would significantly speed up the conversion. There's barely any difference if the column is only date, though. In my project, for a column with 5 millions rows, the difference was huge: ~2.5 min vs 6s. 

It turns out explicitly specifying the format is about 25x faster. The following runtime plot shows that there's a huge gap in performance depending on whether you passed format or not. 

All valid format options can be found at https://strftime.org/.

[![perfplot][1]][1]

<sup>1</sup> Code used to produce the timeit test plot may be found on this repo [here](./perfplot_code.py)

If the column contains multiple formats, see [Convert a column of mixed format strings to a datetime Dtype][2].


  [1]: https://i.stack.imgur.com/Qx5cy.png
  [2]: https://stackoverflow.com/q/56614558/7758804