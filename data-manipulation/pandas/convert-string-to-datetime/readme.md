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

#### Convert a column of mixed format strings to a datetime

How to convert to datetime in the following case:
```python
df = pd.DataFrame({
    'Date': [
        '12/07/2013 21:50:00',
        '13/07/2013 00:30:00',
        '15/07/2013',
        '11/07/2013'
    ]
})
```

If we look at the [source code](https://github.com/pandas-dev/pandas/blob/0b04174115d156541552da07e2c220df613ae36f/pandas/core/tools/datetimes.py#L445-L449), if you pass `format=` and `dayfirst=` arguments, `dayfirst=` will never be read because passing `format=` calls a C function (np_datetime_strings.c) that doesn't use `dayfirst=` to make conversions. On the other hand, if you pass only `dayfirst=`, it will be used to first guess the format and falls back on `dateutil.parser.parse` to make conversions. So, use only one of them.

In most cases, 

```python
df['Date'] = pd.to_datetime(df['Date'])
```
does the job.

In the specific example, passing `dayfirst=True` does the job.
```python
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
```

That said, as elaborated above, passing the `format=` makes the conversion run ~25x faster, so it's probably better to pass the `format=`. Now since the format is mixed, one way is to perform the conversion in two steps (`errors='coerce'` argument will be useful) 

- convert the datetimes with time component 
- fill in the NaT values (the "coerced" rows) by a Series converted with a different format.
```python
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df['Date'] = df['Date'].fillna(pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce'))
```
This method (of performing or more conversions) can be used to convert any column with "weirdly" formatted datetimes.



  [1]: https://i.stack.imgur.com/Qx5cy.png
  [2]: https://stackoverflow.com/q/56614558/7758804