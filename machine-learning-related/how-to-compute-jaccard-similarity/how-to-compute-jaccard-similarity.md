It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/75830840/19123103.

## How to compute jaccard similarity from a pandas dataframe

> I have a dataframe as follows: the shape of the frame is (1510, 1399). The columns represent products, the rows represent values (0 or 1) assigned by a user for a given product. How can I can compute `jaccard_similarity_score`s?
> 
> 
> [![img][0]][0]
> 
> 
> 
> I created a placeholder dataframe listing product vs. product 
> ```python
> data_ibs = pd.DataFrame(index=data_g.columns,columns=data_g.columns)
> ```
> I am not sure how to iterate though data_ibs to compute similarities.
> ```python
> for i in range(0,len(data_ibs.columns)) :
>     # Loop through the columns for each column
>     for j in range(0,len(data_ibs.columns)) :
>         .........
> ```



Jaccard similarity scores can also be calculated using [`scipy.spatial.distance.pdist`][1]. One of its metrics is `'jaccard'` which computes jaccard dissimilarity (so that the score has to be subtracted from 1 to get jaccard similarity). It returns a 1D array where each value corresponds to the jaccard similarity between two columns. 

One could construct a Series from the scores by constructing a MultiIndex.

```python
from scipy.spatial.distance import pdist
jaccard_similarity = pd.Series(1 - pdist(df.values.T, metric='jaccard'), index=pd.MultiIndex.from_tuples([(c1, c2) for i, c1 in enumerate(df) for c2 in df.columns[i+1:]]))
```
Using [ayhan][2]'s setup, it produces the following:
```python
A  B    0.300000
   C    0.457143
   D    0.342857
   E    0.466667
B  C    0.294118
   D    0.333333
   E    0.233333
C  D    0.405405
   E    0.441176
D  E    0.363636
dtype: float64
```

If a matrix is desired, it can be constructed from `pdist` as well. Just construct an empty matrix and fill the off-diagonals by these values (and the diagonal by 1).
```python
from scipy.spatial.distance import pdist

def jaccard_similarity_matrix(df):
    
    n = df.shape[1]
    scores = 1 - pdist(np.array(df).T, metric='jaccard')
    result = np.zeros((n,n))
    result[np.triu_indices(n, k=1)] = scores
    result += result.T
    np.fill_diagonal(result, 1)
    return pd.DataFrame(result, index=df.columns, columns=df.columns)

jaccard_similarity = jaccard_similarity_matrix(df)
```
[![result][3]][3]


---

In fact, by using the [source code][4] of `pdist`, an entirely custom function that only uses numpy and basic python may be written as well.
```python
def jaccard_matrix(df):

    def jaccard(x, y):
        nonzero = (x != 0) | (y != 0)
        a = ((x != y) & nonzero).sum()
        b = nonzero.sum()
        return 1 - a / b if b != 0 else 1
    
    arr = df.values
    n = arr.shape[1]
    scores = [jaccard(arr[:, i], arr[:, j]) for i in range(n-1) for j in range(i+1, n)]
    result = np.zeros((n, n))
    result[np.triu_indices(n, k=1)] = scores
    result += result.T
    np.fill_diagonal(result, 1)
    return pd.DataFrame(result, index=df.columns, columns=df.columns)
```

All of these functions return the same output which can be verified as follows:
```python
df = pd.DataFrame(np.random.default_rng().binomial(1, 0.5, size=(100, 10))).add_prefix('col')
x = pd.DataFrame(1 - pairwise_distances(df.values.T.astype(bool), metric='jaccard'), index=df.columns, columns=df.columns)
y = jaccard_similarity_matrix(df)
z = jaccard_matrix(df)

np.allclose(x, y) and np.allclose(y, z)    # True
```

  [0]: http://i.stack.imgur.com/8newK.png
  [1]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
  [2]: https://stackoverflow.com/a/37004489/19123103
  [3]: https://i.stack.imgur.com/Shv10.png
  [4]: https://github.com/scipy/scipy/blob/v1.10.1/scipy/spatial/distance.py#L1952-L2255