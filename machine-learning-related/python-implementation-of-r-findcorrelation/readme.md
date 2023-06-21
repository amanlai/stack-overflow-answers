## How to implement R's `caret::findCorrelation` in Python

<sup> This post was originally posted as an answer to a Stack Overflow question that can be found [here](https://stackoverflow.com/a/75379515/19123103). </sup>

> #### Remove highly correlated columns from a pandas dataframe
>
> I have a dataframe name `data` whose correlation matrix I computed by using ```python corr = data.corr() ``` If the correlation between two
> columns is greater than 0.75, I want to remove one of them from dataframe `data`. I tried some options  
> ```python 
> raw =corr[(corr.abs()>0.75) & (corr.abs() < 1.0)] 
> ``` 
> but it did not help; I need column number from raw for which value is nonzero. Basically some python equivalent of the following R command (which uses the function `findCorrelation`). 
> ```r 
> {hc=findCorrelation(corr,cutoff = 0.75)
> hc = sort(hc)
> data <- data[,-c(hc)]} 
> ``` 
> If anyone can help me to get command similar to above mention R command in python pandas, that would be helpful.


###### Python implementation of R's [`caret::findCorrelation`][4]

R's `caret::findCorrelation` looks at the mean absolute correlation of each variable and removes the variable with the largest mean absolute correlation for each pair of columns. The following function (named `findCorrelation`) implements the very same logic. 

Depending on the size of the correlation matrix, `caret::findCorrelation` calls one of two functions: the fully vectorized `findCorrelation_fast` or the loopy `findCorrelation_exact` (you can call either regardless of dataframe size by using the `exact=` argument appropriately). The function below does the very same.

The only behavior different from `caret::findCorrelation` is that it returns a list of column names whereas `caret::findCorrelation` returns the index of the columns. I believe it's more natural to return column names which we can pass to `drop` later on.

```python
import numpy as np
import pandas as pd

def findCorrelation(corr, cutoff=0.9, exact=None):
    """
    This function is the Python implementation of the R function 
    `findCorrelation()`.
    
    Relies on numpy and pandas, so must have them pre-installed.
    
    It searches through a correlation matrix and returns a list of column names 
    to remove to reduce pairwise correlations.
    
    For the documentation of the R function, see 
    https://www.rdocumentation.org/packages/caret/topics/findCorrelation
    and for the source code of `findCorrelation()`, see
    https://github.com/topepo/caret/blob/master/pkg/caret/R/findCorrelation.R
    
    -----------------------------------------------------------------------------

    Parameters:
    -----------
    corr: pandas dataframe.
        A correlation matrix as a pandas dataframe.
    cutoff: float, default: 0.9.
        A numeric value for the pairwise absolute correlation cutoff
    exact: bool, default: None
        A boolean value that determines whether the average correlations be 
        recomputed at each step
    -----------------------------------------------------------------------------
    Returns:
    --------
    list of column names
    -----------------------------------------------------------------------------
    Example:
    --------
    R1 = pd.DataFrame({
        'x1': [1.0, 0.86, 0.56, 0.32, 0.85],
        'x2': [0.86, 1.0, 0.01, 0.74, 0.32],
        'x3': [0.56, 0.01, 1.0, 0.65, 0.91],
        'x4': [0.32, 0.74, 0.65, 1.0, 0.36],
        'x5': [0.85, 0.32, 0.91, 0.36, 1.0]
    }, index=['x1', 'x2', 'x3', 'x4', 'x5'])

    findCorrelation(R1, cutoff=0.6, exact=False)  # ['x4', 'x5', 'x1', 'x3']
    findCorrelation(R1, cutoff=0.6, exact=True)   # ['x1', 'x5', 'x4'] 
    """
    
    def _findCorrelation_fast(corr, avg, cutoff):

        combsAboveCutoff = corr.where(lambda x: (np.tril(x)==0) & (x > cutoff)).stack().index

        rowsToCheck = combsAboveCutoff.get_level_values(0)
        colsToCheck = combsAboveCutoff.get_level_values(1)

        msk = avg[colsToCheck] > avg[rowsToCheck].values
        deletecol = pd.unique(np.r_[colsToCheck[msk], rowsToCheck[~msk]]).tolist()

        return deletecol


    def _findCorrelation_exact(corr, avg, cutoff):

        x = corr.loc[(*[avg.sort_values(ascending=False).index]*2,)]

        if (x.dtypes.values[:, None] == ['int64', 'int32', 'int16', 'int8']).any():
            x = x.astype(float)

        x.values[(*[np.arange(len(x))]*2,)] = np.nan

        deletecol = []
        for ix, i in enumerate(x.columns[:-1]):
            for j in x.columns[ix+1:]:
                if x.loc[i, j] > cutoff:
                    if x[i].mean() > np.nanmean(x.drop(j)):
                        deletecol.append(i)
                        x.loc[i] = x[i] = np.nan
                    else:
                        deletecol.append(j)
                        x.loc[j] = x[j] = np.nan
        return deletecol

    
    if not np.allclose(corr, corr.T) or any(corr.columns!=corr.index):
        raise ValueError("correlation matrix is not symmetric.")
        
    acorr = corr.abs()
    avg = acorr.mean()
        
    if exact or exact is None and corr.shape[1]<100:
        return _findCorrelation_exact(acorr, avg, cutoff)
    else:
        return _findCorrelation_fast(acorr, avg, cutoff)
```
You can call `findCorrelation` to find the columns to drop and call `drop()` on the dataframe to drop those columns (exactly how you would use this function is R).

Using [piRSquared's setup][2], it returns the following output.

```python
corr = df.corr()
hc = findCorrelation(corr, cutoff=0.5)
trimmed_df = df.drop(columns=hc)
```
[![res][1]][1]


  [1]: https://i.stack.imgur.com/Txq4w.png
  [2]: https://stackoverflow.com/a/44892279/19123103
  [3]: https://stackoverflow.com/questions/44889508#comment88778596_44892279
  [4]: https://www.rdocumentation.org/packages/caret/topics/findCorrelation