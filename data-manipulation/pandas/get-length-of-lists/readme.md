## How to determine the length of lists in a pandas dataframe column

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75796628/19123103). </sup>

If a dataframe column contains lists such as the following:

```none
                                        col
                [ubuntu, mac-osx, syslinux]
[ubuntu, mod-rewrite, laconica, apache-2.2]
             [ubuntu, nat, squid, mikrotik]
```
How do you compute the length of each of the lists to get the following output:
```none
                                        col  Length
                [ubuntu, mac-osx, syslinux]       3
[ubuntu, mod-rewrite, laconica, apache-2.2]       4
             [ubuntu, nat, squid, mikrotik]       4
```

Weirdly, `.str` accessor can also work on lists, so the canonical way is to call `str.len()`. However, as is often the case with pandas columns of object dtype, there are _better_ ways to perform the same task by dropping down to a Python level loop.


#### Convert to list and `map` a function

Pandas dataframe columns are not meant to store collections such as lists, tuples etc. because virtually none of the optimized methods work on these columns, so when a dataframe contains such items, it's usually more efficient to convert the column into a Python list and manipulate the list.

Also, if a function (especially a built-in one like `len()`) needs to be called on each item in a list, it's usually faster to `map` this function, rather than calling it in a loop.

```python
mylist = df['CreationDate'].tolist()
df['Length'] = list(map(len, mylist))
```

##### Handle NaNs

Nice thing about `str.len()` is that it handles NaNs but a custom function with `try-except` should fill that gap.

```python
def nanlen(x):
    try:
        return len(x)
    except TypeError:
        return float('nan')
    
df['Length'] = list(map(nanlen, mylist))
```

##### Runtime benchmarks

Essentially, mapping `len` over lists is approx. 2.5 times faster than looping over a Series, which in turn is 2.5 times faster than `pd.Series.str.len` for large frames.

[![res][1]][1]

The code used to produce the performance plot above can be found on the current repo [here](./perfplot_tester.py).



  [1]: https://i.stack.imgur.com/QZcyE.png