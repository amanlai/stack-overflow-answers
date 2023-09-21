## Remove rows from an array

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75666001/19123103).</sup>


The most cases boolean indexing will do the job. For example, to remove the rows that contains any NaNs, we can use the following.
```python
arr[~np.isnan(arr).any(axis=1)]
```

You can also use a masked array via `np.ma.fix_invalid` to create a mask and filter out "bad" values (such as NaN, inf).
```python
arr = np.array([
    [0, 1, np.inf],
    [2.2, 3.3, 4.],
    [np.nan, 5.5, 6],
    [7.8, -np.inf, 9.9],
    [10, 11, 12]
])

new_arr = arr[~np.ma.fix_invalid(arr).mask.any(axis=1)]

# array([[ 2.2,  3.3,  4. ],
#        [10. , 11. , 12. ]])
```

If the array contains strings such as `'NA'`, then `np.where` may be useful to "mask" these values and then filter them out.
```python
arr = np.array([
    [0, 1, 'N/A'],
    [2.2, 3.3, 4.],
    [np.nan, 5.5, 6],
    [7.8, 'NA', 9.9],
    [10, 11, 12]
], dtype=object)

tmp = np.where(np.isin(arr, ['NA', 'N/A']), np.nan, arr).astype(float)
new_arr = tmp[~np.isnan(tmp).any(axis=1)]

# array([[ 2.2,  3.3,  4. ],
#        [10. , 11. , 12. ]])
```