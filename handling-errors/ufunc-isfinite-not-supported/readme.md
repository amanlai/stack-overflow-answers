## How to solve the error: `ufunc 'isfinite' not supported for the input types`

<sup>This post is based on my answer to a Stack Overflow question that may be found [1](https://stackoverflow.com/a/75319814/19123103) and [2](https://stackoverflow.com/a/75551268/19123103).</sup>

If you got this error, that means the function you called used `np.isfinite` under the hood. Common functions that do so are `np.allclose`, `np.isclose` and `linalg` methods (as in the OP). It usually means the dtype of your array is `object`.

A common fix is to cast the array to `float` dtype.
```python
covMat = covMat.astype(float)
```
Another common case is when concatenation / stack goes wrong or when the array comes from another datatype (e.g. pandas dataframes). In that case, try converting to a list first and then cast to `np.ndarray`.
```python
arr = np.array(arr.tolist())
```
For example, for the following case, straightforward recasting won't work but converting to a list and then into an ndarray works.
```python
arr = pd.Series([np.array([1,2]), np.array([3,4]), np.array([5,6])]).values
# array([array([1, 2]), array([3, 4]), array([5, 6])], dtype=object)

np.array(arr, dtype=float)                  # <---- error
np.array(arr.tolist(), dtype=float)         # <---- no error
```