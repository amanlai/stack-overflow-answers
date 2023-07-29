## Case when & default logic in pandas

<sup>This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/73618660/19123103), [2](https://stackoverflow.com/a/73619829/19123103). </sup>

If you need to create a new column in a pandas DataFrame conditional on values in another column, then there are multiple ways to do it efficiently.

Suppose we have the following dataframe,
```python
df = pd.DataFrame({'Time': range(0, 100, 20)})
```
and we want to create another column `"Difficulty"` using the following logic:
```none
IF      0 <  Time <  30, THEN 'Easy'
ELSEIF 30 <= Time <= 60, THEN 'Medium'
ELSEIF 60 <  Time,       THEN 'Hard'
ELSE 'Unknown'
```

#### `numpy.select()`

First method is to use `numpy.select()`.

```python
df['difficulty'] = np.select(
    [
        df['Time'].between(0, 30, inclusive='neither'), 
        df['Time'].between(30, 60, inclusive='both'), 
        df['Time'] > 60
    ], 
    [
        'Easy', 
        'Medium', 
        'Hard'
    ], 
    'Unknown'
)
```

#### `loc[]`

Another method is use `loc[]` iteratively. The basic idea of this approach is to initialize a column with some default value (e.g. `"Unknown"`) and update rows depending on conditions (e.g. `"Easy"` if `0<Time<30`), etc.

When we time the options, for large frames, `loc` approach is the fastest (4-5 times faster than `np.select` and nested `np.where`).<sup>1</sup>.

```python
df['difficulty'] = 'Unknown'
df.loc[(df['Time']<30) & (df['Time']>0), 'difficulty'] = 'Easy'
df.loc[(df['Time']>=30) & (df['Time']<=60), 'difficulty'] = 'Medium'
df.loc[df['Time']>60, 'difficulty'] = 'Hard'
```


---

<sup>1</sup>: Code used for benchmark may be found [here](./timeit_test.py) on the current repo.