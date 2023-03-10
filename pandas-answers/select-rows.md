It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/72933069/19123103

## How do I select rows from a DataFrame based on column values?

> How can I select rows from a DataFrame based on values in some column in Pandas?
> 
> In SQL, I would use:
> 
> ```sql
> SELECT *
> FROM table
> WHERE column_name = some_value
> ```

## 1. Use f-strings inside `query()` calls

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

## 2. Install `numexpr` to speed up `query()` calls

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

## 3. Call pandas methods inside `query()`

`Numexpr` [currently supports][2] only logical (`&`, `|`, `~`), comparison (`==`, `>`, `<`, `>=`, `<=`, `!=`) and basic arithmetic operators (`+`, `-`, `*`, `/`, `**`, `%`). 

For example, it doesn't support integer division (`//`). However, calling the equivalent pandas method (`floordiv()`) works.
```python
df.query('B.floordiv(2) <= 3')  # or 
df.query('B.floordiv(2).le(3)')

# for pandas < 1.4, need `.values`
df.query('B.floordiv(2).values <= 3')
```

<br>

---

<sup>1</sup> Benchmark code using a frame with 80k rows 
```python
import numpy as np
df = pd.DataFrame({'A': 'foo bar foo baz foo bar foo foo'.split()*10000, 
                   'B': np.random.rand(80000)})

%timeit df[df.A == 'foo']
# 8.5 ms ± 104.5 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%timeit df.query("A == 'foo'")
# 6.36 ms ± 95.7 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit df[((df.A == 'foo') & (df.A != 'bar')) | ((df.A != 'baz') & (df.A != 'buz'))]
# 29 ms ± 554 µs per loop (mean ± std. dev. of 10 runs, 100 loops each)
%timeit df.query("A == 'foo' & A != 'bar' | A != 'baz' & A != 'buz'")
# 16 ms ± 339 µs per loop (mean ± std. dev. of 10 runs, 100 loops each)

%timeit df[(df.B % 5) **2 < 0.1]
# 5.35 ms ± 37.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%timeit df.query("(B % 5) **2 < 0.1")
# 4.37 ms ± 46.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

<sup>2</sup> Benchmark code using a frame with 800k rows 

```python
df = pd.DataFrame({'A': 'foo bar foo baz foo bar foo foo'.split()*100000, 
                   'B': np.random.rand(800000)})

%timeit df[df.A == 'foo']
# 87.9 ms ± 873 µs per loop (mean ± std. dev. of 10 runs, 100 loops each)
%timeit df.query("A == 'foo'")
# 54.4 ms ± 726 µs per loop (mean ± std. dev. of 10 runs, 100 loops each)

%timeit df[((df.A == 'foo') & (df.A != 'bar')) | ((df.A != 'baz') & (df.A != 'buz'))]
# 310 ms ± 3.4 ms per loop (mean ± std. dev. of 10 runs, 100 loops each)
%timeit df.query("A == 'foo' & A != 'bar' | A != 'baz' & A != 'buz'")
# 132 ms ± 2.43 ms per loop (mean ± std. dev. of 10 runs, 100 loops each)

%timeit df[(df.B % 5) **2 < 0.1]
# 54 ms ± 488 µs per loop (mean ± std. dev. of 10 runs, 100 loops each)
%timeit df.query("(B % 5) **2 < 0.1")
# 26.3 ms ± 320 µs per loop (mean ± std. dev. of 10 runs, 100 loops each)
```
<sup>3</sup>: Code used to produce the performance graphs of the two methods for strings and numbers.
```python
from perfplot import plot
constructor = lambda n: pd.DataFrame({'A': 'foo bar foo baz foo bar foo foo'.split()*n, 'B': np.random.rand(8*n)})
plot(
    setup=constructor,
    kernels=[lambda df: df[(df.B%5)**2<0.1], lambda df: df.query("(B%5)**2<0.1")],
    labels= ['df[(df.B % 5) **2 < 0.1]', 'df.query("(B % 5) **2 < 0.1")'],
    n_range=[2**k for k in range(4, 24)],
    xlabel='Rows in DataFrame',
    title='Multiple mathematical operations on numbers',
    equality_check=pd.DataFrame.equals);
plot(
    setup=constructor,
    kernels=[lambda df: df[df.A == 'foo'], lambda df: df.query("A == 'foo'")],
    labels= ["df[df.A == 'foo']", """df.query("A == 'foo'")"""],
    n_range=[2**k for k in range(4, 24)],
    xlabel='Rows in DataFrame',
    title='Comparison operation on strings',
    equality_check=pd.DataFrame.equals);
```



  [1]: https://pandas.pydata.org/docs/getting_started/install.html#install-recommended-dependencies
  [2]: https://numexpr.readthedocs.io/projects/NumExpr3/en/latest/user_guide.html#supported-operators
  [3]: https://i.stack.imgur.com/AgEhg.png
  [4]: https://stackoverflow.com/a/57338153/19123103