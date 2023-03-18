It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/73643899/19123103

## Create new column based on values from other columns / apply a function of multiple columns, row-wise in Pandas

> I want to apply my custom function (it uses an if-else ladder) to these six columns (`ERI_Hispanic`, `ERI_AmerInd_AKNatv`, `ERI_Asian`, `ERI_Black_Afr.Amer`, `ERI_HI_PacIsl`, `ERI_White`) in each row of my dataframe.
> 
> I've tried different methods from other questions but still can't seem to find the right answer for my problem.  The critical piece of this is that if the person is counted as Hispanic they can't be counted as anything else.  Even if they have a "1" in another ethnicity column they still are counted as Hispanic not two or more races.  Similarly, if the sum of all the ERI columns is greater than 1 they are counted as two or more races and can't be counted as a unique ethnicity(except for Hispanic). 
> 
> It's almost like doing a for loop through each row and if each record meets a criterion they are added to one list and eliminated from the original.  
> 
> From the dataframe below I need to calculate a new column based on the following spec in SQL:
> 
> **CRITERIA**
> ```none
> IF [ERI_Hispanic] = 1 THEN RETURN “Hispanic”
> ELSE IF SUM([ERI_AmerInd_AKNatv] + [ERI_Asian] + [ERI_Black_Afr.Amer] + [ERI_HI_PacIsl] + [ERI_White]) > 1 THEN RETURN “Two or More”
> ELSE IF [ERI_AmerInd_AKNatv] = 1 THEN RETURN “A/I AK Native”
> ELSE IF [ERI_Asian] = 1 THEN RETURN “Asian”
> ELSE IF [ERI_Black_Afr.Amer] = 1 THEN RETURN “Black/AA”
> ELSE IF [ERI_HI_PacIsl] = 1 THEN RETURN “Haw/Pac Isl.”
> ELSE IF [ERI_White] = 1 THEN RETURN “White”
> ```
> Comment: If the ERI Flag for Hispanic is True (1), the employee is classified as “Hispanic”
> 
> Comment: If more than 1 non-Hispanic ERI Flag is true, return “Two or More”
> 
> 
> **DATAFRAME**
> ```none
>      lname   fname  rno_cd  eri_afr_amer  eri_asian  eri_hawaiian  eri_hispanic  eri_nat_amer  eri_white  rno_defined
> 0     MOST    JEFF       E             0          0             0             0             0          1        White
> 1   CRUISE     TOM       E             0          0             0             1             0          0        White
> 2     DEPP  JOHNNY                     0          0             0             0             0          1      Unknown
> 3    DICAP     LEO                     0          0             0             0             0          1      Unknown
> 4   BRANDO  MARLON       E             0          0             0             0             0          0        White
> 5    HANKS     TOM                     0          0             0             0             0          1      Unknown
> 6   DENIRO  ROBERT       E             0          1             0             0             0          1        White
> 7   PACINO      AL       E             0          0             0             0             0          1        White
> 8 WILLIAMS   ROBIN       E             0          0             1             0             0          0        White
> 9 EASTWOOD   CLINT       E             0          0             0             0             0          1        White
> ```


If we inspect its [source code](https://github.com/pandas-dev/pandas/blob/main/pandas/core/apply.py), `apply()` is a syntactic sugar for a Python for-loop (via the `apply_series_generator()` method of the `FrameApply` class). Because it has the pandas overhead, it's generally *slower* than a Python loop.

Use optimized (vectorized) methods wherever possible. If you have to use a loop, use `@numba.jit` decorator.

## 1. Don't use `apply()` for an if-else ladder

`df.apply()` is just about the slowest way to do this in pandas. As shown in the answers of [user3483203](https://stackoverflow.com/a/53505512/19123103) and [Mohamed Thasin ah](https://stackoverflow.com/a/57410089/19123103), depending on the dataframe size, `np.select()` and `df.loc` may be 50-300 times faster than `df.apply()` to produce the same output.

As it happens, a loop implementation (not unlike `apply()`) with the `@jit` decorator from [`numba`](https://numba.pydata.org/numba-doc/latest/user/5minguide.html) module is (about 50-60%) faster than `df.loc` and `np.select`.<sup>1</sup>

Numba works on numpy arrays, so before using the `jit` decorator, you need to convert the dataframe into a numpy array. Then fill in values in a pre-initialized empty array by checking the conditions in a loop. Since numpy arrays don't have column names, you have to access the columns by their index in the loop. The most inconvenient part of the if-else ladder in the jitted function over the one in `apply()` is accessing the columns by their indices. Otherwise it's almost the same implementation.

```python
import numpy as np
import numba as nb
@nb.jit(nopython=True)
def conditional_assignment(arr, res):    
    length = len(arr)
    for i in range(length):
        if arr[i][3] == 1:
            res[i] = 'Hispanic'
        elif arr[i][0] + arr[i][1] + arr[i][2] + arr[i][4] + arr[i][5] > 1:
            res[i] = 'Two Or More'
        elif arr[i][0]  == 1:
            res[i] = 'Black/AA'
        elif arr[i][1] == 1:
            res[i] = 'Asian'
        elif arr[i][2] == 1:
            res[i] = 'Haw/Pac Isl.'
        elif arr[i][4] == 1:
            res[i] = 'A/I AK Native'
        elif arr[i][5] == 1:
            res[i] = 'White'
        else:
            res[i] = 'Other'
    return res

# the columns with the boolean data
cols = [c for c in df.columns if c.startswith('eri_')]
# initialize an empty array to be filled in a loop
# for string dtype arrays, we need to know the length of the longest string
# and use it to set the dtype
res = np.empty(len(df), dtype=f"<U{len('A/I AK Native')}")
# pass the underlying numpy array of `df[cols]` into the jitted function
df['rno_defined'] = conditional_assignment(df[cols].values, res)
```
---

## 2. Don't use `apply()` for numeric operations

If you need to add a new row by adding two columns, your first instinct may be to write
```python
df['c'] = df.apply(lambda row: row['a'] + row['b'], axis=1)
```
But instead of this, row-wise add using `sum(axis=1)` method (or `+` operator if there are only a couple of columns):
```python
df['c'] = df[['a','b']].sum(axis=1)
# equivalently
df['c'] = df['a'] + df['b']
```
Depending on the dataframe size, `sum(1)` may be 100s of times faster than `apply()`.

In fact, you will almost never need `apply()` for numeric operations on a pandas dataframe because it has optimized methods for most operations: addition (`sum(1)`), subtraction (`sub()` or `diff()`), multiplication (`prod(1)`), division (`div()` or `/`), power (`pow()`), `>`, `>=`, `==`, `%`, `//`, `&`, `|` etc. can all be performed on the entire dataframe without `apply()`.

For example, let's say you want to create a new column using the following rule:
```none
IF [colC] > 0 THEN RETURN [colA] * [colB]
ELSE RETURN [colA] / [colB]
```
Using the optimized pandas methods, this can be written as
```python
df['new'] = df[['colA','colB']].prod(1).where(df['colC']>0, df['colA'] / df['colB'])
```
the equivalent `apply()` solution is:
```python
df['new'] = df.apply(lambda row: row.colA * row.colB if row.colC > 0 else row.colA / row.colB, axis=1)
```
The approach using the optimized methods is 250 times faster than the equivalent `apply()` approach for dataframes with 20k rows. This gap only increases as the data size increases (for a dataframe with 1 mil rows, it's 365 times faster) and the time difference will become more and more noticeable.<sup>2</sup>

---

<br>
<sup>1</sup>: In the below result, I show the performance of the three approaches using a dataframe with 24 mil rows (this is the largest frame I can construct on my machine). For smaller frames, the numba-jitted function consistently runs at least 50% faster than the other two as well (you can check yourself).

```python
def pd_loc(df):
    df['rno_defined'] = 'Other'
    df.loc[df['eri_nat_amer'] == 1, 'rno_defined'] = 'A/I AK Native'
    df.loc[df['eri_asian'] == 1, 'rno_defined'] = 'Asian'
    df.loc[df['eri_afr_amer'] == 1, 'rno_defined'] = 'Black/AA'
    df.loc[df['eri_hawaiian'] == 1, 'rno_defined'] = 'Haw/Pac Isl.'
    df.loc[df['eri_white'] == 1, 'rno_defined'] = 'White'
    df.loc[df[['eri_afr_amer', 'eri_asian', 'eri_hawaiian', 'eri_nat_amer', 'eri_white']].sum(1) > 1, 'rno_defined'] = 'Two Or More'
    df.loc[df['eri_hispanic'] == 1, 'rno_defined'] = 'Hispanic'
    return df

def np_select(df):
    conditions = [df['eri_hispanic'] == 1,
                  df[['eri_afr_amer', 'eri_asian', 'eri_hawaiian', 'eri_nat_amer', 'eri_white']].sum(1).gt(1),
                  df['eri_nat_amer'] == 1,
                  df['eri_asian'] == 1,
                  df['eri_afr_amer'] == 1,
                  df['eri_hawaiian'] == 1,
                  df['eri_white'] == 1]
    outputs = ['Hispanic', 'Two Or More', 'A/I AK Native', 'Asian', 'Black/AA', 'Haw/Pac Isl.', 'White']
    df['rno_defined'] = np.select(conditions, outputs, 'Other')
    return df


@nb.jit(nopython=True)
def conditional_assignment(arr, res):
    
    length = len(arr)
    for i in range(length):
        if arr[i][3] == 1 :
            res[i] = 'Hispanic'
        elif arr[i][0] + arr[i][1] + arr[i][2] + arr[i][4] + arr[i][5] > 1 :
            res[i] = 'Two Or More'
        elif arr[i][0]  == 1:
            res[i] = 'Black/AA'
        elif arr[i][1] == 1:
            res[i] = 'Asian'
        elif arr[i][2] == 1:
            res[i] = 'Haw/Pac Isl.'
        elif arr[i][4] == 1 :
            res[i] = 'A/I AK Native'
        elif arr[i][5] == 1:
            res[i] = 'White'
        else:
            res[i] = 'Other'
            
    return res

def nb_loop(df):
    cols = [c for c in df.columns if c.startswith('eri_')]
    res = np.empty(len(df), dtype=f"<U{len('A/I AK Native')}")
    df['rno_defined'] = conditional_assignment(df[cols].values, res)
    return df

# df with 24mil rows
n = 4_000_000
df = pd.DataFrame({
    'eri_afr_amer': [0, 0, 0, 0, 0, 0]*n, 
    'eri_asian': [1, 0, 0, 0, 0, 0]*n, 
    'eri_hawaiian': [0, 0, 0, 1, 0, 0]*n, 
    'eri_hispanic': [0, 1, 0, 0, 1, 0]*n, 
    'eri_nat_amer': [0, 0, 0, 0, 1, 0]*n, 
    'eri_white': [0, 0, 1, 1, 0, 0]*n
}, dtype='int8')
df.insert(0, 'name', ['MOST', 'CRUISE', 'DEPP', 'DICAP', 'BRANDO', 'HANKS']*n)

%timeit nb_loop(df)
# 5.23 s ± 45.2 ms per loop (mean ± std. dev. of 10 runs, 10 loops each)

%timeit pd_loc(df)
# 7.97 s ± 28.8 ms per loop (mean ± std. dev. of 10 runs, 10 loops each)

%timeit np_select(df)
# 8.5 s ± 39.6 ms per loop (mean ± std. dev. of 10 runs, 10 loops each)
```

<sup>2</sup>: In the below result, I show the performance of the two approaches using a dataframe with 20k rows and again with 1 mil rows. For smaller frames, the gap is smaller because the optimized approach has an overhead while `apply()` is a loop. As the size of the frame increases, the vectorization overhead cost diminishes w.r.t. to the overall runtime of the code while `apply()` remains a loop over the frame.
```python
n = 20_000 # 1_000_000
df = pd.DataFrame(np.random.rand(n,3)-0.5, columns=['colA','colB','colC'])

%timeit df[['colA','colB']].prod(1).where(df['colC']>0, df['colA'] / df['colB'])
# n = 20000: 2.69 ms ± 23.5 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# n = 1000000: 86.2 ms ± 441 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit df.apply(lambda row: row.colA * row.colB if row.colC > 0 else row.colA / row.colB, axis=1)
# n = 20000: 679 ms ± 33.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# n = 1000000: 31.5 s ± 587 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```