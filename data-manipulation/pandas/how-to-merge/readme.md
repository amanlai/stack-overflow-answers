## How to merge two dataframes

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75190030/19123103).</sup>

To merge two dataframes on columns with common keys, simply pass the relevant column(s) from each dataframe as follows:
```python
merged_df = df1.merge(df2, left_on='common_column_1', right_on='common_column_2')
```
If the column to match on each dataframe has the same label, it's even easier:
```python
merged_df = df1.merge(df2, on='common_column')
```

To merge on **multiple columns**, pass the columns as a list.
```python
merged_df = df1.merge(df2, on=['common_column_1', 'common_column_2'])
```


### Some common questions about merging on multiple columns

1. It merges according to the ordering of `left_on` and `right_on`, i.e., the i-th element of `left_on` will match with the i-th of `right_on`.

   In the example below, the code on the top matches `A_col1` with `B_col1` and `A_col2` with `B_col2`, while the code on the bottom matches `A_col1` with `B_col2` and `A_col2` with `B_col1`. Evidently, the results are different.

   [![res1][1]][1]

2. As can be seen from the above example, if the merge keys have different names, all keys will show up as their individual columns in the merged dataframe. In the example above, in the top dataframe, `A_col1` and `B_col1` are identical and `A_col2` and `B_col2` are identical. In the bottom dataframe, `A_col1` and `B_col2` are identical and `A_col2` and `B_col1` are identical. Since these are duplicate columns, they are most likely not needed. One way to not have this problem from the beginning is to make the merge keys identical from the beginning. See bullet point #3 below.

3. If `left_on` and `right_on` are the same `col1` and `col2`, we can use `on=['col1', 'col2']`. In this case, no merge keys are duplicated.
   ```python
   df1.merge(df2, on=['col1', 'col2'])
   ```
   [![res3][2]][2]

4. You can also merge one side on column names and the other side on index too. For example, in the example below, `df1`'s columns are matched with `df2`'s indices. If the indices are named, as in the example below, you can reference them by name but if not, you can also use `right_index=True` (or `left_index=True` if the left dataframe is the one being merged on index).

   ```python
   df1.merge(df2, left_on=['A_col1', 'A_col2'], right_index=True)
   # or
   df1.merge(df2, left_on=['A_col1', 'A_col2'], right_on=['B_col1', 'B_col2'])
   ```
   [![res3][3]][3]

5. By using the `how=` parameter, you can perform `LEFT JOIN` (`how='left'`), `FULL OUTER JOIN` (`how='outer'`) and `RIGHT JOIN` (`how='right'`) as well. The default is `INNER JOIN` (`how='inner'`) as in the examples above.

6. If you have more than 2 dataframes to merge and the merge keys are the same across all of them, then `join` method is more efficient than `merge` because you can pass a list of dataframes and join on indices. Note that the index names are the same across all dataframes in the example below (`col1` and `col2`). Note that the indices don't have to have names; if the indices don't have names, then the number of the multi-indices must match (in the case below there are 2 multi-indices). Again, as in bullet point #1, the match occurs according to the ordering of the indices.

   ```python
   df1.join([df2, df3], how='inner').reset_index()
   ```
   [![res4][4]][4]


  [1]: https://i.stack.imgur.com/RBTQy.png
  [2]: https://i.stack.imgur.com/VIZue.png
  [3]: https://i.stack.imgur.com/ilaff.png
  [4]: https://i.stack.imgur.com/SbDyF.png