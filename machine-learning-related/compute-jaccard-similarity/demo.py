import pandas as pd
from scipy.spatial.distance import pdist
import numpy as np
from sklearn.metrics import pairwise_distances

jaccard_similarity = pd.Series(1 - pdist(df.values.T, metric='jaccard'), index=pd.MultiIndex.from_tuples([(c1, c2) for i, c1 in enumerate(df) for c2 in df.columns[i+1:]]))



def jaccard_similarity_matrix(df):
    
    n = df.shape[1]
    scores = 1 - pdist(np.array(df).T, metric='jaccard')
    result = np.zeros((n,n))
    result[np.triu_indices(n, k=1)] = scores
    result += result.T
    np.fill_diagonal(result, 1)
    return pd.DataFrame(result, index=df.columns, columns=df.columns)

jaccard_similarity = jaccard_similarity_matrix(df)



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


# sanity check
df = pd.DataFrame(np.random.default_rng().binomial(1, 0.5, size=(100, 10))).add_prefix('col')
x = pd.DataFrame(1 - pairwise_distances(df.values.T.astype(bool), metric='jaccard'), index=df.columns, columns=df.columns)
y = jaccard_similarity_matrix(df)
z = jaccard_matrix(df)

np.allclose(x, y) and np.allclose(y, z)    # True