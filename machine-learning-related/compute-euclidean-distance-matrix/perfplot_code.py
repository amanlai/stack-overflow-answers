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