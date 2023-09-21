## Slicing a numpy array

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75585695/19123103).</sup>

#### Slicing a multi-dimensional array


To slice a multi-dimensional array, the dimension (i.e. axis) must be specified. As OP noted, `arr[i:j][i:j]` is exactly the same as `arr[i:j]` because `arr[i:j]` sliced along the first axis (rows) and has the same number of dimensions as `arr` (you can confirm by `arr[i:j].ndim == arr.ndim`); so the second slice is still slicing along the first dimension (which was already done by the first slice). To slice along the second dimension, it must be explicitly specified, e.g.:
```python
arr[:2][:, :2]                   # its output is the same as `arr[:2, :2]`
```
A bare `:` means slice everything in that axis, so there's an implicit `:` for the second axis in the above code (i.e. `arr[:2, :][:, :2]`). What the above code is doing is slicing the first two rows (or first two arrays along the first axis) and then slice the first two columns (or the first two arrays along the second axis) from the resulting array.

An `...` can be used instead of multiple colons (`:`), so for a general n-dimensional array, the following produce the same output:
```python
w = arr[i:j, m:n]
x = arr[i:j, m:n, ...]
y = arr[i:j][:, m:n]
z = arr[i:j, ...][:, m:n, ...]
```

That said, `arr[:2, :2]` is the canonical way because in the case of `arr[i:j][:, i:j]`, `arr[i:j]` creates a temporary array which is indexed by `[:, i:j]`, so it's comparatively inefficient.

However, there are cases where chained indexing makes sense (or readable), e.g., if you want to index a multi-dimensional array using a list of indices. For example, if you want to slice the top-left quarter of a 4x4 array using a list of indices, then chained indexing gives the correct result whereas a single indexing gives a different result (it's because of [numpy advanced indexing][1]) where the values correspond to the index pair for each position in the index lists.
```python
arr = np.arange(1,17).reshape(4,4)
rows = cols = [0,1]
arr[rows][:, cols]               # <--- correct output
arr[rows, cols]                  # <--- wrong output
arr[[[e] for e in rows], cols]   # <--- correct output
arr[np.ix_(rows, cols)]          # <--- correct output
```

  [1]: https://numpy.org/doc/stable/user/basics.indexing.html#advanced-indexing