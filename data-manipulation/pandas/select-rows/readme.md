## Select rows from a DataFrame

<sup>This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/73762002/19123103), [2](https://stackoverflow.com/a/72842272/19123103), [3](https://stackoverflow.com/a/72862831/19123103), [4](https://stackoverflow.com/a/72873572/19123103) and [5](https://stackoverflow.com/a/73074165/19123103). </sup>

### 1. Use f-strings inside `query()` calls

If the column name used to filter your dataframe comes from a local variable, f-strings may be useful. For example,
```python
col = 'A'
df.query(f"{col} == 'foo'")
```
In fact, f-strings can be used for the query variable as well (except for datetime):
```python
col = 'A'
my_var = 'foo'
df.query(f"{col} == '{my_var}'") # if my_var is a string

my_num = 1
df.query(f"{col} == {my_num}") # if my_var is a number

my_date = '2022-12-10'
df.query(f"{col} == @my_date") # must use @ for datetime though
```

### 2. Install `numexpr` to speed up `query()` calls

The pandas documentation [recommends installing numexpr][1] to speed up numeric calculation when using `query()`. Use `pip install numexpr` (or `conda`, `sudo` etc. depending on your environment) to install it.

For larger dataframes (where performance actually matters), `df.query()` with `numexpr` engine performs much faster than `df[mask]`. In particular, it performs better for the following cases.


**Logical and/or comparison operators on columns of strings**

If a column of strings are compared to some other string(s) and matching rows are to be selected, even for a single comparison operation, `query()` performs faster than `df[mask]`. For example, for a dataframe with 80k rows, it's 30% faster<sup>1</sup> and for a dataframe with 800k rows, it's 60% faster.<sup>2</sup>
```python
df[df.A == 'foo']
df.query("A == 'foo'")  # <--- performs 30%-60% faster
```
This gap increases as the number of operations increases (if 4 comparisons are chained `df.query()` is 2-2.3 times faster than `df[mask]`)<sup>1,2</sup> and/or the dataframe length increases.<sup>2</sup>

**Multiple operations on numeric columns**

If multiple arithmetic, logical or comparison operations need to be computed to create a boolean mask to filter `df`, `query()` performs faster. For example, for a frame with 80k rows, it's 20% faster<sup>1</sup> and for a frame with 800k rows, it's 2 times faster.<sup>2</sup>
```python
df[(df.B % 5) **2 < 0.1]
df.query("(B % 5) **2 < 0.1")  # <--- performs 20%-100% faster.
```
This gap in performance increases as the number of operations increases and/or the dataframe length increases.<sup>2</sup>



The following plot shows how the methods perform as the dataframe length increases.<sup>3</sup>

[![perfplot][3]][3]

### 3. Call pandas methods inside `query()`

`Numexpr` [currently supports][2] only logical (`&`, `|`, `~`), comparison (`==`, `>`, `<`, `>=`, `<=`, `!=`) and basic arithmetic operators (`+`, `-`, `*`, `/`, `**`, `%`). 

For example, it doesn't support integer division (`//`). However, calling the equivalent pandas method (`floordiv()`) works.
```python
df.query('B.floordiv(2) <= 3')  # or 
df.query('B.floordiv(2).le(3)')

# for pandas < 1.4, need `.values`
df.query('B.floordiv(2).values <= 3')
```



### 4. Use a list of values to select rows

If we need to select multiple rows using a list of values such as the following:
```python
df = DataFrame({'A' : [5,6,3,4], 'B' : [1,2,3, 5]})
list_of_values = [3,6]
```
then the canonical way is `isin()` or `query()` such as:
```python
df1 = df[df['A'].isin(list_of_values)]

df2 = df.query("A in @list_of_values")
```

`list_of_values` doesn't have to be a `list`; it can be `set`, `tuple`, `dictionary`, numpy array, pandas Series, generator, `range` etc. and `isin()` and `query()` will still work.

**a. `list_of_values` is a range**

If you need to filter within a range, you can use [`between()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html) method or `query()`.

```python
list_of_values = [3, 4, 5, 6] # a range of values

df[df['A'].between(3, 6)]  # or
df.query('3<=A<=6')
```

**b. Return `df` in the order of `list_of_values`**

In the OP, the values in `list_of_values` don't appear in that order in `df`. If you want `df` to return in the order they appear in `list_of_values`, i.e. "sort" by `list_of_values`, use `loc`.
```python
list_of_values = [3, 6]
df.set_index('A').loc[list_of_values].reset_index()
```
If you want to retain the old index, you can use the following.
```python
list_of_values = [3, 6, 3]
df.reset_index().set_index('A').loc[list_of_values].reset_index().set_index('index').rename_axis(None)
```

**c. Don't use `apply`**

In general, `isin()` and `query()` are the best methods for this task; there's no need for `apply()`. For example, for function `f(A) = 2*A - 5` on column `A`, both `isin()` and `query()` work much more efficiently:
```python
df[(2*df['A']-5).isin(list_of_values)]         # or
df[df['A'].mul(2).sub(5).isin(list_of_values)] # or
df.query("A.mul(2).sub(5) in @list_of_values")
```

**d. Select rows not in `list_of_values`**

To select rows not in `list_of_values`, negate `isin()`/`in`:
```python
df[~df['A'].isin(list_of_values)]
df.query("A not in @list_of_values")  # df.query("A != @list_of_values")
```

**e. Select rows where multiple columns are in `list_of_values`**

If you want to filter using both (or multiple) columns, there's `any()` and `all()` to reduce columns (`axis=1`) depending on the need.

1. Select rows where at least one of `A` or `B` is in `list_of_values`:
   ```python
   df[df[['A','B']].isin(list_of_values).any(1)]
   df.query("A in @list_of_values or B in @list_of_values")
   ```
2. Select rows where both of `A` and `B` are in `list_of_values`:
   ```python
   df[df[['A','B']].isin(list_of_values).all(1)] 
   df.query("A in @list_of_values and B in @list_of_values")
   ```


### 5. Filter string data based on its string length

For string operations such as this, vanilla Python using built-in methods (without lambda) is much faster than `apply()` or `str.len()`. 

Building a boolean mask by mapping `len` to each string inside a list comprehension is approx. 40-70% faster than `apply()` and `str.len()` respectively. 

For multiple columns, `zip()` allows to evaluate values from different columns concurrently.
```python
df = pd.DataFrame({'A' : ['hi', 'hello', 'day'], 'B' : [1, 2, 3]})
col_A_len = map(len, df['A'])
col_B_len = map(len, df['B'])
m = [a==3 and b==3 for a,b in zip(col_A_len, col_B_len)]
df1 = df[m]
```
For a single column, drop `zip()` and loop over the column and check if the length is equal to 3:
```python
df2 = df[[a==3 for a in map(len, df['A'])]]
```
This code can be written a little concisely using the `Series.map()` method (but a little slower than list comprehension due to pandas overhead):
```python
df2 = df[df['A'].map(len)==3]
```

`query()` works with `str.` methods as well. For example, to select rows from a dataframe by string length the following may be used.


```python
df.query('A.str.len() != 3')
```


### Select rows using a complex criteria

If we want to select rows using multiple conditions such as: 

> Select values from 'A' for which corresponding values for 'B' will be greater than 50, and for 'C' not equal to 900.

In this case, as discussed above, creating a boolean mask and filtering is the canonical way.
```python
msk = (df["B"] > 50) & (df["C"] != 900)
df1 = df[msk]
```
or using `query()`:
```python
df.query("B > 50 and C != 900")
```

It may be more readable to assign each condition to a variable, especially if there are a lot of them (maybe with descriptive names) and chain them together using bitwise operators such as (`&` or `|`). As a bonus, you don't need to worry about brackets `()` because each condition evaluates independently.
```python
m1 = df['B'] > 50
m2 = df['C'] != 900
m3 = df['C'].pow(2) > 1000
m4 = df['B'].mul(4).between(50, 500)

# filter rows where all of the conditions are True
df[m1 & m2 & m3 & m4]

# filter rows of column A where all of the conditions are True
df.loc[m1 & m2 & m3 & m4, 'A']
```
or put the conditions in a list and reduce it via `bitwise_and` from `numpy` (wrapper for `&`).
```python
conditions = [
    df['B'] > 50,
    df['C'] != 900,
    df['C'].pow(2) > 1000,
    df['B'].mul(4).between(50, 500)
]
# filter rows of A where all of conditions are True
df.loc[np.bitwise_and.reduce(conditions), 'A']
```

---

<sup>1</sup> Benchmark code using a frame with 80k rows can be found on the current repo [here][7].

<sup>2</sup> Benchmark code using a frame with 800k rows can be found on the current repo [here][6].

<sup>3</sup>: Code used to produce the performance graphs of the two methods for strings and numbers can be found on the current repo [here][5].




  [1]: https://pandas.pydata.org/docs/getting_started/install.html#install-recommended-dependencies
  [2]: https://numexpr.readthedocs.io/projects/NumExpr3/en/latest/user_guide.html#supported-operators
  [3]: https://i.stack.imgur.com/AgEhg.png
  [4]: https://stackoverflow.com/a/57338153/19123103
  [5]: ./perfplot_tester.py
  [6]: ./timeit_tester_800k.py
  [7]: ./timeit_tester_80k.py