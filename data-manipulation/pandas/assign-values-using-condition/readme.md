## How to assign values based on a condition

<sup>This is based on my answers to Stack Overflow questions that may be found at 
[1](https://stackoverflow.com/a/73728391/19123103), 
[2](https://stackoverflow.com/a/73687100/19123103), 
[3](https://stackoverflow.com/a/73669816/19123103), 
[4](https://stackoverflow.com/a/73664277/19123103).
[5](https://stackoverflow.com/a/75238820/19123103)
</sup>


Suppose we want to assign a new column to a pandas DataFrame using the following condition on an existing column:
```none
IF gender==male AND pet1==pet2, THEN points = 5
ELSEIF gender==female AND (pet1=='cat' OR pet1=='dog'), THEN points = 5
ELSE points = 0
```


#### `np.select()`/`np.where()`

The canonical way to perform this task via `numpy.select()` method. 

```python
conditions = [
    df['gender'].eq('male') & df['pet1'].eq(df['pet2']),
    df['gender'].eq('female') & df['pet1'].isin(['cat', 'dog'])
]

choices = [5, 5]

df['points'] = np.select(conditions, choices, default=0)
```

Another, a bit more convoluted way is via `numpy.where()`. It is designed for two conditional (IF-ELSE), so for the specific case, we can reduce the first two conditions into a single one using a logical OR.
```python
df['points'] = np.where( ( (df['gender'] == 'male') & (df['pet1'] == df['pet2'] ) ) | ( (df['gender'] == 'female') & (df['pet1'].isin(['cat','dog'] ) ) ), 5, 0)
```

#### `np.where()` and `.eval()`

Writing the conditions as a string expression and evaluating it using `eval()` is another method to evaluate the condition. Then using its outcome as a `numpy.where()` condition, you can assign values  as follows.
```python
# evaluate the condition 
condition = df.eval("gender=='male' and pet1==pet2 or gender=='female' and pet1==['cat','dog']")
# assign values
df['points'] = np.where(condition, 5, 0)
```
If you have a large dataframe (100k+ rows) and a lot of comparisons to evaluate, this method is probably the fastest pandas method to construct a boolean mask.<sup>1</sup>

If you installed numexpr (`pip install numexpr`) as [recommended](https://pandas.pydata.org/docs/getting_started/install.html#install-recommended-dependencies) in the pandas documentation, this method should perform as well (and better if you have a lot of conditions to reduce) as chaining via `&`. The advantage is that (i) it's much more readable (imo) and (ii) you don't need to worry about brackets `()`, `and`/`&` etc. anymore because the order of precedence inside the string expression is the same as [that in Python](https://docs.python.org/3/reference/expressions.html#operator-precedence).


#### `loc`

Another method is use `loc` iteratively.
```
df = pd.DataFrame({
    'age' : [21, 45, 45, 5],
    'salary' : [20, 40, 10, 100]
})

df['is_rich_method3'] = 'no'
df.loc[df['salary'] > 50, 'is_rich_method3'] = 'yes'
```

#### `mask()`

Another method is by using the pandas [`mask`](https://pandas.pydata.org/docs/reference/api/pandas.Series.mask.html) (depending on the use-case [`where`](https://pandas.pydata.org/docs/reference/api/pandas.Series.where.html)) method. First initialize a Series with a default value (chosen as `"no"`) and replace some of them depending on a condition (a little like a mix between `loc[]` and `numpy.where()`).
```python
df = pd.DataFrame({
    'age' : [21, 45, 45, 5],
    'salary' : [20, 40, 10, 100]
})
df['is_rich'] = pd.Series('no', index=df.index).mask(df['salary']>50, 'yes')
```
It is probably the fastest option. For example, for a frame with 10 mil rows, `mask()` option is 40% faster than `loc` option.<sup>2</sup>


[![res][1]][1]



### Insert several columns at a specific position

On a completely different topic, say, we want to insert several columns in a specific column position in a dataframe, how do we go about it?

For example, if we have a dataframe with 2 columns and we want to insert a dataframe with 3 columns between columns A and B? In other words, we want to make the following transformation:
```none
A B        A x y z B
0 a   ->   0 0 0 0 a
1 b        1 0 0 0 b
2 c        2 0 0 0 c
```


One way is to assign values to the original dataframe and reorder the columns using column selection.

```python
df[['x', 'y', 'z']] = 0
df[[*df.columns[:1], 'x', 'y', 'z', *df.columns[1]]]
```

or for an entirely new copy, use `assign`:

cols = ['x', 'y', 'z']
new_df = (
    df
    .assign(**dict.fromkeys(cols, 0))
    .reindex(columns=[*df.columns[:], *cols, *df.columns[1:]])
)

A more robust version is to split the dataframe into two and concatenate back with the new dataframe sandwiched between.
```python
tmp = pd.DataFrame(0, index=df.index, columns=range(1, 32))

new_df = pd.concat([df.iloc[:,:1], df, df.iloc[:, 1:]], axis=1)
```



---

<sup>1</sup>: For a dataframe with 105k rows, if you evaluate 4 conditions where each chain two comparisons, `eval()` creates a boolean mask substantially faster than chaining bitwise operators. The supporting timeit test may be found [here](./timeit_test.py) on this repo.

<sup>2</sup>: The benchmark result that compares `mask` with `loc` may be found on the current repo [here](./mask_vs_loc.py)


  [1]: https://i.stack.imgur.com/AR3eJ.png