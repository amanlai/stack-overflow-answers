## How to handle the error: `Must have equal len keys and value when setting with an iterable`

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/74651544/19123103).</sup>


The [source code][1] shows that this error occurs when you try to broadcast a list-like object (numpy array, list, set, tuple etc.) to multiple columns or rows but didn't specify the index correctly. Of course, list-like objects don't have custom indices like pandas objects, so it usually causes this error.

Solutions to common cases:

1. **You want to assign the same values across multiple columns at once.** In other words, you want to change the values of certain columns using a list-like object whose (a) length doesn't match the number of columns or rows and (b) dtype doesn't match the dtype of the columns they are being assigned to.<sup>1</sup> An illustration may make it clearer. If you try to make the transformation below:

   [![first][2]][2]

   using a code similar to the one below, this error occurs:

   ```python
   df = pd.DataFrame({'A': [1, 5, 9], 'B': [2, 6, 10], 'C': [3, 7, 11], 'D': [4, 8, 12]})
   df.loc[:2, ['C','D']] = [100, 200.2, 300]
   ```

   **Solution:** Duplicate the list/array/tuple, transpose it (either using `T` or `zip()`) and assign to the relevant rows/columns.<sup>2</sup>

   ```python
   df.loc[:2, ['C','D']] = np.tile([100, 200.2, 300], (len(['C','D']), 1)).T 
   # if you don't fancy numpy, use zip() on a list
   # df.loc[:2, ['C','D']] = list(zip(*[[100, 200.2, 300]]*len(['C','D'])))
   ```
<br>

2. **You want to assign the same values to multiple rows at once.** If you try to make the following transformation

   [![second][3]][3]

   using a code similar to the following:

   ```python
   df = pd.DataFrame({'A': [1, 5, 9], 'B': [2, 6, 10], 'C': [3, 7, 11], 'D': [4, 8, 12]})
   df.loc[[0, 1], ['A', 'B', 'C']] = [100, 200.2]
   ```

   **Solution:** To make it work as expected, we must convert the list/array into a Series with the correct index:
   ```python
   df.loc[[0, 1], ['A', 'B', 'C']] = pd.Series([100, 200.2], index=[0, 1])
   ```
   <br>

   A common sub-case is if the row indices come from using a boolean mask. N.B. This is the case in the OP. In that case, just use the mask to filter `df.index`:

   ```python
   msk = df.index < 2
   df.loc[msk, ['A', 'B', 'C']] = [100, 200.2]                                 # <--- error
   df.loc[msk, ['A', 'B', 'C']] = pd.Series([100, 200.2], index=df.index[msk]) # <--- OK
   ```
<br>

3. **You want to store the same list in some rows of a column.** An illustration of this case is:

   [![third][4]][4]

   **Solution:** Explicitly construct a Series with the correct indices.
   ```python
   # for the case on the left in the image above
   df['D'] = pd.Series([[100, 200.2]]*len(df), index=df.index)

   # latter case
   df.loc[[1], 'D'] = pd.Series([[100, 200.2]], index=df.index[[1]])
   ```

   
---

<sup>1: Here, we tried to assign a list containing a float to int dtype columns, which contributed to this error being raised. If we tried to assign a list of ints (so that the dtypes match), we'd get a different error: `ValueError: shape mismatch: value array of shape (2,) could not be broadcast to indexing result of shape (2,3)` which can also be solved by the same method as above.</sup>

<sup>2: An error related to this one `ValueError: Must have equal len keys and value when setting with an ndarray` occurs if the object being assigned is a numpy array and there's a shape mismatch. That one is often solved either using `np.tile` or simply transposing the array.</sup>


  [1]: https://github.com/pandas-dev/pandas/blob/v1.5.2/pandas/core/indexing.py#L1828-L1882
  [2]: https://i.stack.imgur.com/kAyhC.png
  [3]: https://i.stack.imgur.com/p56EI.png
  [4]: https://i.stack.imgur.com/Jk8zJ.png