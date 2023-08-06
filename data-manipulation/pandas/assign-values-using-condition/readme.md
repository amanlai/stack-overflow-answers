## How to assign values based on a condition

<sup>This is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/73728391/19123103).</sup>


Suppose we want to assign a new column to a pandas DataFrame using the following condition on an existing column:
```none
IF gender==male AND pet1==pet2, THEN points = 5
ELSEIF gender==female AND (pet1=='cat' OR pet1=='dog'), THEN points = 5
ELSE points = 0
```

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

Writing the conditions as a string expression and evaluating it using `eval()` is another method to evaluate the condition and assign values to the column using `numpy.where()`. 
```python
# evaluate the condition 
condition = df.eval("gender=='male' and pet1==pet2 or gender=='female' and pet1==['cat','dog']")
# assign values
df['points'] = np.where(condition, 5, 0)
```
If you have a large dataframe (100k+ rows) and a lot of comparisons to evaluate, this method is probably the fastest pandas method to construct a boolean mask.<sup>1</sup>

Another advantage of this method over chained `&` and/or `|` operators (used in the other vectorized answers here) is better readability (arguably).

---

<sup>1</sup>: For a dataframe with 105k rows, if you evaluate 4 conditions where each chain two comparisons, `eval()` creates a boolean mask substantially faster than chaining bitwise operators. The supporting timeit test may be found [here](./timeit_test.py) on this repo.