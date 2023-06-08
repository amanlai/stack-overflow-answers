## Delete a column from a Pandas DataFrame

<sup> It's a post that was first posted as an answer to the following Stack Overflow question and can be found [here](https://stackoverflow.com/a/76428891/19123103). </sup>


> I have a pandas DataFrame. How do I remove a column from it? Can I use
> ```python
> del df.column_name
> ```


Deleting a column using `del` is not only problematic (as explained by [@firelynx][1]) but also very slow. For example, it's ~37 times slower than `drop()`. Code used to make this assertion can be found on the current repo [here](./timeit_test.py).

---

On the topic of performance, if a single column needs to be dropped, boolean indexing (create a boolean Series of _wanted_ columns and `loc`-index them) is actually the fastest method for the job. However, if multiple columns need to be dropped, `drop()` is the fastest method. 

As a refresher, the methods in question are as follows (all of the methods given on this page where tested but these two were the fastest).
```python
import pandas as pd
df = pd.DataFrame([range(10)]*5).add_prefix('col')

# drop a single column (the performance comparison is shown in LHS subplot)
df1 = df.loc[:, df.columns != 'col2']                # boolean indexing
df2 = df.drop(columns='col2')                        # drop

# drop multiple columns (the performance comparison is shown in RHS subplot)
df1 = df.loc[:, ~df.columns.isin(['col2', 'col4'])]  # boolean indexing
df2 = df.drop(columns=['col2', 'col4'])              # drop
```

The following performance comparison graph was created using the perfplot library (which performs `timeit` tests under the hood). This supports the claim made above. The main takeaway is when dropping single column, boolean indexing is faster; however, when dropping multiple columns for very wide dataframes, `drop()` is faster.

[![performance][2]][2]

Code used to produce the performance plots can be found on the current repo [here](./perfplot_test.py).

  [1]: https://stackoverflow.com/a/37000877/19123103
  [2]: https://i.stack.imgur.com/6V76x.png