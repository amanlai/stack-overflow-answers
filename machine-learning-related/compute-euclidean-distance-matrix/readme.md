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

#### 2. Scikit-learn's `euclidean_distances()` for sparse matrix data



---

<sup>1</sup> The code used to produce the perfplot
```python
import numpy as np
from scipy.spatial import distance
import perfplot
import matplotlib.pyplot as plt

def sqrt_sum(arr):
    return np.sqrt(np.sum((arr[:, None] - arr) ** 2, axis=-1))

def linalg_norm(arr):
    return np.linalg.norm(arr[:, None] - arr, axis=-1)

def scipy_cdist(arr):
    return distance.cdist(arr, arr)

perfplot.plot(
    setup=lambda n: np.random.rand(n, 3),
    n_range=[2 ** k for k in range(14)],
    kernels=[sqrt_sum, scipy_cdist, linalg_norm],
    title="Euclidean distance between arrays of 3-D points",
    xlabel="len(x), len(y)",
    equality_check=np.allclose
)
plt.gcf().set_facecolor('white');
```

  [1]: https://stackoverflow.com/a/47775357/19123103
  [2]: https://i.stack.imgur.com/iOoq5.png
