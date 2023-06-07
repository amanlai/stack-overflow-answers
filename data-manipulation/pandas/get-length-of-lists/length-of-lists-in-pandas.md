## How to determine the length of lists in a pandas dataframe column

<sup>It's a post that was first posted as an answer to the following Stack Overflow question and can be found [here](https://stackoverflow.com/a/75796628/19123103). </sup>

> I have a dataframe like this:
> 
> ```none
>                                                     CreationDate
> 2013-12-22 15:25:02                  [ubuntu, mac-osx, syslinux]
> 2009-12-14 14:29:32  [ubuntu, mod-rewrite, laconica, apache-2.2]
> 2013-12-22 15:42:00               [ubuntu, nat, squid, mikrotik]
> ```
> I am calculating the length of lists in the `CreationDate` column and making a new `Length` column like this:
> ```python
> df['Length'] = df.CreationDate.apply(lambda x: len(x))
> ```
>     
> Which gives me this:
> ```none
>                                                     CreationDate  Length
> 2013-12-22 15:25:02                  [ubuntu, mac-osx, syslinux]       3
> 2009-12-14 14:29:32  [ubuntu, mod-rewrite, laconica, apache-2.2]       4
> 2013-12-22 15:42:00               [ubuntu, nat, squid, mikrotik]       4
> ```
>     
> Is there a more pythonic way to do this?





##### Convert to list and `map` a function

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



  [1]: https://i.stack.imgur.com/QZcyE.png