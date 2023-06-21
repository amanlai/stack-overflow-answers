## How to implement R's `caret::findCorrelation` in Python

<sup> This post was originally posted as an answer to a Stack Overflow question that can be found [here](https://stackoverflow.com/a/75379515/19123103). </sup>


R's `caret::findCorrelation` looks at the mean absolute correlation of each variable and removes the variable with the largest mean absolute correlation for each pair of columns. The following function (named `findCorrelation`) implements the very same logic. 

Depending on the size of the correlation matrix, `caret::findCorrelation` calls one of two functions: the fully vectorized `findCorrelation_fast` or the loopy `findCorrelation_exact` (you can call either regardless of dataframe size by using the `exact=` argument appropriately). The function below does the very same.

The only behavior different from `caret::findCorrelation` is that it returns a list of column names whereas `caret::findCorrelation` returns the index of the columns. I believe it's more natural to return column names which we can pass to `drop` later on.


You can call `findCorrelation` to find the columns to drop and call `drop()` on the dataframe to drop those columns (exactly how you would use this function is R).

Using [piRSquared's setup][2], it returns the following output.

```python
from findcorrelation import findCorrelation
corr = df.corr()
hc = findCorrelation(corr, cutoff=0.5)
trimmed_df = df.drop(columns=hc)
```
[![res][1]][1]


  [1]: https://i.stack.imgur.com/Txq4w.png
  [2]: https://stackoverflow.com/a/44892279/19123103
  [3]: https://stackoverflow.com/questions/44889508#comment88778596_44892279
  [4]: https://www.rdocumentation.org/packages/caret/topics/findCorrelation