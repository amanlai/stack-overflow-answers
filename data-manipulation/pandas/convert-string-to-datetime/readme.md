## Convert Pandas Column to DateTime

<sup> This is based on my answer to a Stack Overflow question that can be found [here](https://stackoverflow.com/q/26763344/19123103) </sup>

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

Long story short, passing the correct `format=` from the beginning as in [chrisb's post](https://stackoverflow.com/a/26763793/19123103) is much faster than letting pandas figure out the format, especially if the format contains **time** component. The runtime difference for dataframes greater than 10k rows is huge (~25 times faster, so we're talking like a couple minutes vs a few seconds). All valid format options can be found at https://strftime.org/.

[![perfplot][1]][1]

<sup>1</sup> Code used to produce the timeit test plot may be found on this repo [here](./perfplot_code.py)

If the column contains multiple formats, see [Convert a column of mixed format strings to a datetime Dtype][2].


  [1]: https://i.stack.imgur.com/Qx5cy.png
  [2]: https://stackoverflow.com/q/56614558/7758804