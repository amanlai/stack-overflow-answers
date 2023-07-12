import numpy as np
from scipy.spatial import distance
from scipy import sparse
from sklearn.metrics import pairwise

a = [(1, 2, 3), (3, 4, 5), (2, 3, 6)]
b = [(1, 2, 3), (4, 5, 6)]

dsts1 = distance.cdist(a, b)
print(dsts1)

# array([[0.        , 5.19615242],
#        [3.46410162, 1.73205081],
#        [3.31662479, 2.82842712]])




###################################################


# using `linalg.norm`
dsts2 = np.linalg.norm(np.array(a)[:, None] - b, axis=-1)
print(dsts2)

# using a `sqrt` + `sum` + `square`
dsts3 = np.sqrt(np.sum((np.array(a)[:, None] - b)**2, axis=-1))
print(dsts3)

# equality check
np.allclose(dsts1, dsts2) and np.allclose(dsts1, dsts3)        # True



###################################################


A = sparse.random(1_000_000, 3)
b = [(1, 2, 3), (4, 5, 6)]

dsts = pairwise.euclidean_distances(A, b)
print(dsts)