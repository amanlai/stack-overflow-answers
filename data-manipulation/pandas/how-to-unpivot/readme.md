## How to convert a wide dataframe into a long one

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75780687/19123103).</sup>


Given a dataframe that looks like the following:
```none
   2014  2015 farm  fruit
0    10    11    A  apple
1    12    13    B  apple
2     6     7    A   pear
3     8     9    B   pear
```
how to make it long that looks like the following:
```none
  farm  fruit  value  year
0    A  apple     10  2014
1    B  apple     12  2014
2    A   pear      6  2014
3    B   pear      8  2014
4    A  apple     11  2015
5    B  apple     13  2015
6    A   pear      7  2015
7    B   pear      9  2015
```

The dedicated method for this is called `melt`:
```python
long_df = df.melt(id_vars=['farm', 'fruit'], var_name='year', value_name='value')
```


It can be done using `stack()`; just that `set_index()` has to be called first to repeat `farm` and `fruit` for each year-value pair.
```python
long_df = df.set_index(['farm', 'fruit']).rename_axis(columns='year').stack().reset_index(name='value')
```
[![result1][1]][1]


One interesting function is `pd.wide_to_long` which can also be used to "melt" a frame. However, it requires a `stubname`, so wouldn't work for the case in the OP but works for other cases. For example, in the case below (note how years in the column labels have `value_` in it).
```python
long_df = pd.wide_to_long(df, 'value', i=['farm', 'fruit'], j='year', sep='_').reset_index()
```
[![result2][2]][2]


  [1]: https://i.stack.imgur.com/A7DqM.png
  [2]: https://i.stack.imgur.com/4k0CX.png