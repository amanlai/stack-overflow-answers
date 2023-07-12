## How to compute the Euclidean distance?

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/q/1401712/19123103).</sup>

First off, if the desire is to find the Euclidean distance between only two points, then scipy's `euclidean()` is the simplest.
```python
from scipy.spatial import distance
a, b = (1, 2, 3), (4, 5, 6)
x = distance.euclidean(a, b)
```
Yet another way is `numpy.linalg.norm` or even a straightforward computation coding its formula using vectorized numpy methods.
```python
y = np.linalg.norm(np.array(a) - b)
z = np.sqrt(np.sum((np.array(a) - b)**2))
```

---

#### 1. SciPy's vectorized `cdist()` for Euclidean distance matrix

[@Nico Schlömer][1]'s benchmarks show scipy's `euclidean()` function to be much slower than its numpy counterparts. The reason is that it's meant to work on a pair of points, not an array of points; thus not vectorized. Also, his benchmark uses code to find the Euclidean distances between arrays of equal length. 

If you need to compute the Euclidean distance matrix between each pair of points from two collections of inputs, then there is another SciPy function, `cdist()`, that is much faster than numpy.

Consider the following example where `a` contains 3 points and `b` contains 2 points. SciPy's `cdist()` computes the Euclidean distances between **every** point in `a` to **every** point in `b`, so in this example, it would return a 3x2 matrix.

```python
import numpy as np
from scipy.spatial import distance

a = [(1, 2, 3), (3, 4, 5), (2, 3, 6)]
b = [(1, 2, 3), (4, 5, 6)]

dsts1 = distance.cdist(a, b)

# array([[0.        , 5.19615242],
#        [3.46410162, 1.73205081],
#        [3.31662479, 2.82842712]])
```

It is especially useful if we have a collection of points and we want to find the closest distance to each point other than itself; a common use-case is in natural language processing. For example, to compute the Euclidean distances between every pair of points in a collection, `distance.cdist(a, a)` does the job. Since the distance from a point to itself is 0, the diagonals of this matrix will be all zero.

The same task can be performed with numpy-only methods using broadcasting. We simply need to add another dimension to one of the arrays.

```python
# using `linalg.norm`
dsts2 = np.linalg.norm(np.array(a)[:, None] - b, axis=-1)

# using a `sqrt` + `sum` + `square`
dsts3 = np.sqrt(np.sum((np.array(a)[:, None] - b)**2, axis=-1))

# equality check
np.allclose(dsts1, dsts2) and np.allclose(dsts1, dsts3)        # True
```

---

As mentioned earlier, `cdist()` is much faster than the numpy counterparts. The following perfplot shows as much.<sup>1</sup> 

[![result][2]][2]

---

#### 2. Scikit-learn's `euclidean_distances()`

Scikit-learn is a pretty big library so unless you're not using it for something else, it doesn't make much sense to import it only for Euclidean distance computation but for completeness, it also has `euclidean_distances()`, `paired_distances()` and `pairwise_distances()` methods that can be used to compute Euclidean distances. It has other convenient pairwise distance computation methods [worth checking out][3].

One useful thing about scikit-learn's methods is that it can handle sparse matrices as is, whereas scipy/numpy will need to have sparse matrices converted into arrays to perform computation so depending on the size of the data, scikit-learn's methods may be the only function that runs.

An example:

```python
from scipy import sparse
from sklearn.metrics import pairwise

A = sparse.random(1_000_000, 3)
b = [(1, 2, 3), (4, 5, 6)]

dsts = pairwise.euclidean_distances(A, b)
```

---

<sup>1</sup> The code used to produce the perfplot may be found on this repo [here](./perfplot_code.py).

  [1]: https://stackoverflow.com/a/47775357/19123103
  [2]: https://i.stack.imgur.com/iOoq5.png
  [3]: https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics.pairwise