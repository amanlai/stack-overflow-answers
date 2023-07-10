## How can I use the `apply()` function for a single column?

<sup> This post was originally created as an answer to the following Stack Overflow that can be found [here](https://stackoverflow.com/a/75264127/19123103).</sup>

I have a pandas dataframe with two columns. I need to change the values of the first column without affecting the second one and get back the whole dataframe with just first column values changed. How can I do that using `apply()` in pandas?


#### Make a copy of your dataframe first if you need to modify a column

Many answers here suggest modifying some column and assign the new values to the old column. It is common to get the `SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.` warning. This happens when your dataframe was created from another dataframe but is not a proper copy.

To silence this warning, make a copy and assign back.
```python
df = df.copy()
df['a'] = df['a'].apply('add', other=1)
```

#### `apply()` only needs the name of the function

You can invoke a function by simply passing its name to `apply()` (no need for `lambda`). If your function needs **additional arguments**, you can pass them either as keyword arguments or pass the positional arguments as `args=`. For example, suppose you have file paths in your dataframe and you need to read files in these paths.

```python
def read_data(path, sep=',', usecols=[0]):
    return pd.read_csv(path, sep=sep, usecols=usecols)

df = pd.DataFrame({'paths': ['../x/yz.txt', '../u/vw.txt']})

df['paths'].apply(read_data)                            # you don't need lambda

df['paths'].apply(read_data, args=(',', [0, 1]))        # pass the positional arguments to `args=`

df['paths'].apply(read_data, sep=',', usecols=[0, 1])   # pass as keyword arguments
```

#### Don't apply a function, call the appropriate method directly

It's almost never ideal to apply a custom function on a column via `apply()`. Because `apply()` is a syntactic sugar for a Python loop with a pandas overhead, it's often _slower_ than calling the same function in a **list comprehension**, never mind, calling optimized pandas methods. Almost all numeric operators can be directly applied on the column and there are corresponding methods for all of them. 
```python
# add 1 to every element in column `a`
df['a'] += 1

# for every row, subtract column `a` value from column `b` value
df['c'] = df['b'] - df['a']
```

If you want to apply a function that has if-else blocks, then you should probably be using [numpy.where()](https://numpy.org/doc/stable/reference/generated/numpy.where.html) or [numpy.select()](https://numpy.org/doc/stable/reference/generated/numpy.select.html) instead. It is much, much faster. If you have anything larger than 10k rows of data, you'll notice the difference right away. 

For example, if you have a custom function similar to `func()` below, then instead of applying it on the column, you could operate directly on the columns and return values using `numpy.select()`.
```python
def func(row):
    if row == 'a':
        return 1
    elif row == 'b':
        return 2
    else:
        return -999

# instead of applying a `func` to each row of a column, use `numpy.select` as below

import numpy as np
conditions = [df['col'] == 'a', df['col'] == 'b']
choices = [1, 2]
df['new'] = np.select(conditions, choices, default=-999)
```
As you can see, `numpy.select()` has very minimal syntax difference from an if-else ladder; only need to separate conditions and choices into separate lists. For other options, check out [this answer](https://stackoverflow.com/a/73643899/19123103).